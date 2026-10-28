"""Run: uv run python -m eval.run_eval"""

import asyncio

from dotenv import load_dotenv
from openai import AsyncOpenAI
from ragas.embeddings import OpenAIEmbeddings
from ragas.llms import llm_factory
from ragas.metrics.collections import AnswerRelevancy, ContextRecall, Faithfulness

load_dotenv()

from app.agent.graph import graph, thread_config
from app.generation.citations import NOT_FOUND

from eval.checks import doc_text, is_refusal, page_hit
from eval.dataset import OFF_TOPIC_SET, QA_SET, ROUTER_SET

client = AsyncOpenAI()
judge = llm_factory("gpt-4o-mini", client=client)
embeddings = OpenAIEmbeddings(client=client, model="text-embedding-3-small")

faithfulness = Faithfulness(llm=judge)
relevancy = AnswerRelevancy(llm=judge, embeddings=embeddings)
recall = ContextRecall(llm=judge)


async def score_qa(item: dict) -> dict:
    result = graph.invoke({"question": item["question"]}, config=thread_config())
    docs = result.get("docs", [])
    contexts = [doc_text(d) for d in docs]
    answer = result.get("answer", "")

    if not contexts:
        return {
            "q": item["question"],
            "hit": False,
            "faith": 0.0,
            "rel": 0.0,
            "recall": 0.0,
        }

    f, r, c = await asyncio.gather(
        faithfulness.ascore(
            user_input=item["question"], response=answer, retrieved_contexts=contexts
        ),
        relevancy.ascore(user_input=item["question"], response=answer),
        recall.ascore(
            user_input=item["question"],
            retrieved_contexts=contexts,
            reference=item["reference"],
        ),
    )
    return {
        "q": item["question"],
        "hit": page_hit(docs, item["pages"]),
        "faith": f.value,
        "rel": r.value,
        "recall": c.value,
    }


def avg(rows: list[dict], key: str) -> float:
    return sum(float(r[key]) for r in rows) / len(rows)


async def main() -> None:
    # 1. RAG quality on the golden set
    print("\n=== RAG quality ===")
    print(f"{'question':55} {'hit':>4} {'faith':>6} {'rel':>6} {'recall':>6}")
    rows = []
    for item in QA_SET:
        row = await score_qa(item)
        rows.append(row)
        print(
            f"{row['q'][:55]:55} {('Y' if row['hit'] else 'N'):>4} "
            f"{row['faith']:6.2f} {row['rel']:6.2f} {row['recall']:6.2f}"
        )
    print(f"\nPage hit rate     : {avg(rows, 'hit'):.2f}")
    print(f"Faithfulness      : {avg(rows, 'faith'):.2f}")
    print(f"Answer relevancy  : {avg(rows, 'rel'):.2f}")
    print(f"Context recall    : {avg(rows, 'recall'):.2f}")

    # 2. Off-topic questions should be refused
    print("\n=== Off-topic refusal ===")
    refused = 0
    for q in OFF_TOPIC_SET:
        ok = is_refusal(
            graph.invoke({"question": q}, config=thread_config()), NOT_FOUND
        )
        refused += ok
        print(f"{'PASS' if ok else 'FAIL'}  {q}")

    # 3. Router picks the right path (only runs the router, not the whole graph)
    print("\n=== Router accuracy ===")
    from app.agent.nodes.router import router_node

    correct = 0
    for item in ROUTER_SET:
        got = router_node({"question": item["question"]})["intent"]
        ok = got == item["intent"]
        correct += ok
        print(
            f"{'PASS' if ok else 'FAIL'}  expected={item['intent']:8} got={got:8} {item['question']}"
        )

    print(
        f"\nRefusal rate: {refused}/{len(OFF_TOPIC_SET)} | Router accuracy: {correct}/{len(ROUTER_SET)}"
    )


if __name__ == "__main__":
    asyncio.run(main())

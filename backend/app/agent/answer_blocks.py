from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from app.agent.blocks import Block
from app.agent.llm import llm


class AnswerBlocks(BaseModel):
    blocks: list[Block] = Field(
        default=[],
        description="0-2 UI blocks that add visual value to the answer. Empty list if none fit.",
    )


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You add small visual blocks under a chat answer about an insurance policy.\n"
            "Use ONLY facts already in the answer. Never invent numbers.\n"
            "- NOT covered / exclusion / gotcha -> callout tone=warning\n"
            "- covered with a condition -> callout tone=info\n"
            "- several items covered/not covered -> checklist\n"
            "- waiting periods -> timeline\n"
            "- 2+ key numbers (limits, amounts) -> stat\n"
            "Return an EMPTY list for simple, short or conversational answers. "
            "Max 2 blocks, and don't just restate the answer word for word. "
            "Copy page numbers from [Page N] markers into `pages`."
            "Keep block text SHORT (max 12 words), like a headline, e.g. title 'Maternity', text 'Excluded - listed under exclusions'. ",
        ),
        ("human", "Question: {question}\n\nAnswer: {answer}"),
    ]
)

blocks_chain = prompt | llm.with_structured_output(
    AnswerBlocks, method="function_calling"
)


def pick_blocks(question: str, answer: str) -> list[dict]:
    try:
        result: AnswerBlocks = blocks_chain.invoke(
            {"question": question, "answer": answer}
        )
        return [b.model_dump() for b in result.blocks[:2]]
    except Exception as e:  # blocks are a bonus - never break the answer
        print("BLOCKS failed:", e, flush=True)
        return []

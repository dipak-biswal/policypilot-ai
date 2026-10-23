import re
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.vector_store import search

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are PolicyPilot, an assistant that answers questions about insurance policies. "
            "Answer ONLY from the context below. If the answer is not in the context, say you don't know. "
            "Cite pages inline like [Page 12].\n\nContext:\n{context}",
        ),
        ("human", "{question}"),
    ]
)

chain = prompt | llm


def answer_question(question: str) -> dict:
    docs = search(question, k=4)

    if not docs:
        return {
            "answer": "I couldn't find this in the uploaded policy",
            "citations": [],
        }

    context = "\n\n".join(f"[Page {d.metadata['page']}] {d.page_content}" for d in docs)

    response = chain.invoke({"context": context, "question": question})
    answer = response.content
    citated_pages = {int(p) for p in re.findall(r"\[Page (\d+)\]", answer)}

    citations = [
        {
            "source": d.metadata["source"],
            "page": d.metadata["page"],
            "snippet": d.page_content[:200],
        }
        for d in docs
        if d.metadata["page"] in citated_pages
    ]

    return {"answer": response.content, "citations": citations}

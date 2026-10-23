from langchain_core.prompts import ChatPromptTemplate

from app.agent.llm import llm
from app.agent.state import AgentState
from app.rag import build_context, extract_citations

summary_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Summarise this insurance policy for a customer in plain English, in 5-8 bullet points: "
            "what it covers, key limits, waiting periods, major exclusions, and how to claim. "
            "Use ONLY the content and cite pages like [Page 3].\n\nContext:\n{context}",
        ),
        ("human", "{question}"),
    ]
)

summary_chain = summary_prompt | llm


def summarizer_node(state: AgentState) -> AgentState:
    docs = state["docs"]

    response = summary_chain.invoke(
        {"context": build_context(docs), "question": state["question"]}
    )

    return {
        "answer": response.content,
        "citations": extract_citations(response.content, docs),
    }

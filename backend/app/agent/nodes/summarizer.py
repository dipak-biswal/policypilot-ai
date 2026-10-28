from langchain_core.prompts import ChatPromptTemplate

from app.agent.llm import llm
from app.agent.state import AgentState
from app.generation.citations import build_context, extract_citations
from app.prompts.loader import load_prompt

summary_prompt = ChatPromptTemplate.from_messages(
    [
        load_prompt("summarizer"),
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

from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from app.agent.llm import llm
from app.agent.state import AgentState

REWRITE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Rewrite the user's latest question as a standalone question about the "
            "insurance policy, using the chat history to resolve words like 'it', "
            "'that' or 'what about'. If it is already standalone, return it unchanged. "
            "Return only the question.",
        ),
        MessagesPlaceholder("history"),
        ("human", "{question}"),
    ]
)

chain = REWRITE_PROMPT | llm


def rewriter_node(state: AgentState) -> dict:
    question = state["question"]
    history = state.get("messages", [])[-6:]  # last 3 Q&A pairs

    standalone = question
    if history:
        standalone = chain.invoke(
            {"history": history, "question": question}
        ).content.strip()

    return {
        "standalone_question": standalone,
        "messages": [HumanMessage(content=question)],
    }

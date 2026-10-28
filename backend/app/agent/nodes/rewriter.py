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
    print(f"REWRITER history={len(state.get('messages', []))}", flush=True)
    question = state["question"]
    history = state.get("messages", [])[-6:]

    if not history:  # first question in the thread: nothing to resolve
        return {"standalone_question": question, "messages": [HumanMessage(question)]}

    result = chain.invoke({"history": history, "question": question})
    return {
        "standalone_question": result.content.strip(),
        "messages": [HumanMessage(question)],
    }

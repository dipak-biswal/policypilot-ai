from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from app.agent.llm import llm
from app.agent.state import AgentState
from app.prompts.loader import load_prompt

REWRITE_PROMPT = ChatPromptTemplate.from_messages(
    [
        load_prompt("rewriter"),
        MessagesPlaceholder("history"),
        ("human", "{question}"),
    ]
)

chain = REWRITE_PROMPT | llm


def rewriter_node(state: AgentState) -> dict:
    question = state["question"]
    history = state.get("messages", [])[-6:]

    if not history:  # first question in the thread: nothing to resolve
        return {"standalone_question": question, "messages": [HumanMessage(question)]}

    result = chain.invoke({"history": history, "question": question})
    return {
        "standalone_question": result.content.strip(),
        "messages": [HumanMessage(question)],
    }

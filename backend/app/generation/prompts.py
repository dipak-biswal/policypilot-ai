from langchain_core.prompts import ChatPromptTemplate
from app.prompts.loader import load_prompt

QA_SYSTEM = load_prompt("qa")

QA_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            QA_SYSTEM,
        ),
        ("human", "{question}"),
    ]
)

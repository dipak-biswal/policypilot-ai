from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from app.agent.blocks import Block
from app.agent.llm import llm
from app.prompts.loader import load_prompt


class AnswerBlocks(BaseModel):
    blocks: list[Block] = Field(
        default=[],
        description="0-2 UI blocks that add visual value to the answer. Empty list if none fit.",
    )


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", load_prompt("answer_blocks")),
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

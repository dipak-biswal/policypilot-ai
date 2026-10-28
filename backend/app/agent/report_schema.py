from typing import Literal

from pydantic import BaseModel, Field

from app.agent.blocks import Block


class TableData(BaseModel):
    columns: list[str]
    rows: list[list[str]]


class KeyValue(BaseModel):
    label: str
    value: str


class ReportSection(BaseModel):
    title: str
    layout: Literal["bullets", "table", "keyValue"] = Field(
        description="bullets for lists, table for comparisons/limits, keyValue for short facts"
    )
    bullets: list[str] = []
    table: TableData | None = None
    items: list[KeyValue] = []
    pages: list[int] = Field(default=[], description="Source pages for this section")


class Report(BaseModel):
    title: str
    summary: str
    blocks: list[Block] = Field(
        description=(
            "4-8 UI blocks chosen to fit the content. Use stat for key numbers, "
            "callout(warning) for exclusions or gotchas, checklist for covered/not covered, "
            "timeline for waiting periods, table for limits/comparisons, progress for "
            "percentages (co-pay, caps), accordion for long detail like claim steps, "
            "bullets for anything else."
        )
    )
    follow_up_questions: list[str] = Field(description="3 useful follow-up questions")

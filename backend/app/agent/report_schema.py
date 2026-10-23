from typing import Literal

from pydantic import BaseModel, Field


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
    sections: list[ReportSection]
    follow_up_questions: list[str] = Field(description="3 useful follow-up questions")

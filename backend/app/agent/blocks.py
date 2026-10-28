from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field


class StatItem(BaseModel):
    label: str
    value: str
    hint: str = ""


class StatBlock(BaseModel):
    type: Literal["stat"] = "stat"
    items: list[StatItem] = Field(
        description="2-4 key numbers, e.g. sum insured, co-pay"
    )
    pages: list[int] = []


class CalloutBlock(BaseModel):
    type: Literal["callout"] = "callout"
    tone: Literal["info", "warning", "success"]
    title: str
    text: str
    pages: list[int] = []


class ChecklistItem(BaseModel):
    text: str
    covered: bool


class ChecklistBlock(BaseModel):
    type: Literal["checklist"] = "checklist"
    title: str
    items: list[ChecklistItem]
    pages: list[int] = []


class TimelineItem(BaseModel):
    when: str = Field(description="e.g. '30 days', '2 years'")
    what: str


class TimelineBlock(BaseModel):
    type: Literal["timeline"] = "timeline"
    title: str
    items: list[TimelineItem]
    pages: list[int] = []


class TableBlock(BaseModel):
    type: Literal["table"] = "table"
    title: str
    columns: list[str]
    rows: list[list[str]]
    pages: list[int] = []


class ProgressItem(BaseModel):
    label: str
    percent: int = Field(ge=0, le=100)
    caption: str = ""


class ProgressBlock(BaseModel):
    type: Literal["progress"] = "progress"
    title: str
    items: list[ProgressItem]
    pages: list[int] = []


class AccordionItem(BaseModel):
    title: str
    bullets: list[str]


class AccordionBlock(BaseModel):
    type: Literal["accordion"] = "accordion"
    title: str
    items: list[AccordionItem]
    pages: list[int] = []


class BulletsBlock(BaseModel):
    type: Literal["bullets"] = "bullets"
    title: str
    bullets: list[str]
    pages: list[int] = []


Block = Annotated[
    Union[
        StatBlock,
        CalloutBlock,
        ChecklistBlock,
        TimelineBlock,
        TableBlock,
        ProgressBlock,
        AccordionBlock,
        BulletsBlock,
    ],
    Field(discriminator="type"),
]

type Base = { pages: number[] };

export type StatBlock = Base & {
  type: "stat";
  items: { label: string; value: string; hint: string }[];
};
export type CalloutBlock = Base & {
  type: "callout";
  tone: "info" | "warning" | "success";
  title: string;
  text: string;
};
export type ChecklistBlock = Base & {
  type: "checklist";
  title: string;
  items: { text: string; covered: boolean }[];
};
export type TimelineBlock = Base & {
  type: "timeline";
  title: string;
  items: { when: string; what: string }[];
};
export type TableBlock = Base & {
  type: "table";
  title: string;
  columns: string[];
  rows: string[][];
};
export type ProgressBlock = Base & {
  type: "progress";
  title: string;
  items: { label: string; percent: number; caption: string }[];
};
export type AccordionBlock = Base & {
  type: "accordion";
  title: string;
  items: { title: string; bullets: string[] }[];
};
export type BulletsBlock = Base & {
  type: "bullets";
  title: string;
  bullets: string[];
};

export type Block =
  | StatBlock
  | CalloutBlock
  | ChecklistBlock
  | TimelineBlock
  | TableBlock
  | ProgressBlock
  | AccordionBlock
  | BulletsBlock;

export type BlockType = Block["type"];

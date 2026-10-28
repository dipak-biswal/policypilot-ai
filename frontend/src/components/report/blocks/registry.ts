import type { ComponentType } from "react";
import type { Block, BlockType } from "@/types";
import { StatBlockView } from "./StatBlockView";
import { CalloutBlockView } from "./CalloutBlockView";
import { ChecklistBlockView } from "./ChecklistBlockView";
import { TimelineBlockView } from "./TimelineBlockView";
import { TableBlockView } from "./TableBlockView";
import { ProgressBlockView } from "./ProgressBlockView";
import { AccordionBlockView } from "./AccordionBlockView";
import { BulletsBlockView } from "./BulletsBlockView";

type BlockOf<T extends BlockType> = Extract<Block, { type: T }>;

type Registry = { [T in BlockType]?: ComponentType<{ block: BlockOf<T> }> };

export const BLOCKS: Registry = {
  stat: StatBlockView,
  callout: CalloutBlockView,
  checklist: ChecklistBlockView,
  timeline: TimelineBlockView,
  table: TableBlockView,
  progress: ProgressBlockView,
  accordion: AccordionBlockView,
  bullets: BulletsBlockView,
};

// blocks that should take the full width of the grid
export const WIDE: BlockType[] = ["stat", "table", "timeline", "accordion"];

export const TAB_GROUPS: { id: string; label: string; types: BlockType[] }[] = [
  { id: "overview", label: "📊 Overview", types: ["stat", "callout"] },
  {
    id: "coverage",
    label: "✅ Coverage",
    types: ["checklist", "table", "progress", "bullets"],
  },
  { id: "waiting", label: "⏳ Waiting periods", types: ["timeline"] },
  { id: "details", label: "📖 Details", types: ["accordion"] },
];
// reports with this many blocks or fewer skip tabs
export const TABS_MIN_BLOCKS = 4;

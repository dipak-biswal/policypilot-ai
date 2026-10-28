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

import type { ComponentType } from "react";
import type { Block, BlockType } from "@/types";
import { StatBlockView } from "./StatBlockView";
import { CalloutBlockView } from "./CalloutBlockView";
import { ChecklistBlockView } from "./ChecklistBlockView";
import { TimelineBlockView } from "./TimelineBlockView";
import { TableBlockView } from "./TableBlockView";

type BlockOf<T extends BlockType> = Extract<Block, { type: T }>;

type Registry = { [T in BlockType]?: ComponentType<{ block: BlockOf<T> }> };

export const BLOCKS: Registry = {
  stat: StatBlockView,
  callout: CalloutBlockView,
  checklist: ChecklistBlockView,
  timeline: TimelineBlockView,
  table: TableBlockView,
};

// blocks that should take the full width of the grid
export const WIDE: BlockType[] = ["stat", "table", "timeline", "accordion"];

import type { ComponentType } from "react";
import type { Block } from "@/types";
import { BLOCKS } from "./registry";

export function BlockRenderer({ block }: { block: Block }) {
  const Comp = BLOCKS[block.type] as
    | ComponentType<{ block: Block }>
    | undefined;
  if (!Comp) {
    // fallback for block types we haven't built yet
    return (
      <pre className="overflow-auto rounded-lg border p-3 text-xs text-muted-foreground">
        {block.type}: {JSON.stringify(block, null, 2)}
      </pre>
    );
  }
  return <Comp block={block} />;
}

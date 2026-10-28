import type { Block } from "@/types";
import { BlockRenderer } from "./BlockRenderer";
import { WIDE } from "./registry";

export function BlockGrid({ blocks }: { blocks: Block[] }) {
  return (
    <div className="grid gap-3 md:grid-cols-2">
      {blocks.map((b, i) => (
        <div
          key={`${b.type}-${i}`}
          className={WIDE.includes(b.type) ? "md:col-span-2" : ""}
        >
          <BlockRenderer block={b} />
        </div>
      ))}
    </div>
  );
}

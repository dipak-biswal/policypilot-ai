import type { Block } from "@/types";
import { BlockRenderer } from "./BlockRenderer";
import { WIDE } from "./registry";

export function BlockGrid({ blocks }: { blocks: Block[] }) {
  // decide which blocks span both columns
  const wide: boolean[] = [];
  let col = 0; // 0 = start of row, 1 = right column
  blocks.forEach((b, i) => {
    const next = blocks[i + 1];
    const alone = col === 0 && (!next || WIDE.includes(next.type));
    const isWide = WIDE.includes(b.type) || alone;
    wide.push(isWide);
    col = isWide ? 0 : col === 0 ? 1 : 0;
  });
  return (
    <div className="grid gap-3 md:grid-cols-2">
      {blocks.map((b, i) => (
        <div key={`${b.type}-${i}`} className={wide[i] ? "md:col-span-2" : ""}>
          <BlockRenderer block={b} />
        </div>
      ))}
    </div>
  );
}

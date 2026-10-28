import type { StatBlock } from "@/types";
import { Card, CardContent } from "@/components/ui/card";
import { PageBadges } from "./PageBadges";

export function StatBlockView({ block }: { block: StatBlock }) {
  return (
    <div
      className="grid gap-3 grid-cols-2"
      style={{
        gridTemplateColumns: `repeat(${Math.min(block.items.length, 4)}, minmax(0, 1fr))`,
      }}
    >
      {block.items.map((s) => (
        <Card key={s.label} className="py-4">
          <CardContent className="px-4">
            <p className="text-xs text-muted-foreground">{s.label}</p>
            <p className="mt-1 text-base font-bold leading-snug text-indigo-600 dark:text-indigo-400 sm:text-lg">
              {s.value}
            </p>

            {s.hint && (
              <p className="mt-1 text-xs text-muted-foreground">{s.hint}</p>
            )}
          </CardContent>
        </Card>
      ))}
      <div className="col-span-full">
        <PageBadges pages={block.pages} />
      </div>
    </div>
  );
}

import type { BulletsBlock } from "@/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { PageBadges } from "./PageBadges";

export function BulletsBlockView({ block }: { block: BulletsBlock }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base">{block.title}</CardTitle>
      </CardHeader>
      <CardContent>
        <ul className="list-disc space-y-1 pl-5 text-sm">
          {block.bullets.map((b) => (
            <li key={b}>{b}</li>
          ))}
        </ul>
        <PageBadges pages={block.pages} />
      </CardContent>
    </Card>
  );
}

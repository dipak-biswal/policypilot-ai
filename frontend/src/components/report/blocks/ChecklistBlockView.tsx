import type { ChecklistBlock } from "@/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { PageBadges } from "./PageBadges";

export function ChecklistBlockView({ block }: { block: ChecklistBlock }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base">{block.title}</CardTitle>
      </CardHeader>
      <CardContent className="space-y-2">
        {block.items.map((i) => (
          <div key={i.text} className="flex items-start gap-2 text-sm">
            <span>{i.covered ? "✅" : "❌"}</span>
            <span className={i.covered ? "" : "text-muted-foreground"}>
              {i.text}
            </span>
          </div>
        ))}
        <PageBadges pages={block.pages} />
      </CardContent>
    </Card>
  );
}

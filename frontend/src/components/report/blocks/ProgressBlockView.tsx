import type { ProgressBlock } from "@/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { PageBadges } from "./PageBadges";

export function ProgressBlockView({ block }: { block: ProgressBlock }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base">{block.title}</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {block.items.map((i) => (
          <div key={i.label}>
            <div className="mb-1 flex justify-between text-sm">
              <span>{i.label}</span>
              <span className="font-semibold text-indigo-600 dark:text-indigo-400">
                {i.percent}%
              </span>
            </div>
            <Progress value={i.percent} />
            {i.caption && (
              <p className="mt-1 text-xs text-muted-foreground">{i.caption}</p>
            )}
          </div>
        ))}
        <PageBadges pages={block.pages} />
      </CardContent>
    </Card>
  );
}

import type { TimelineBlock } from "@/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { PageBadges } from "./PageBadges";

export function TimelineBlockView({ block }: { block: TimelineBlock }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base">⏳ {block.title}</CardTitle>
      </CardHeader>
      <CardContent>
        <ol className="relative ml-2 border-l-2 border-indigo-200 dark:border-indigo-800">
          {block.items.map((i) => (
            <li key={i.when + i.what} className="mb-4 ml-5 last:mb-0">
              <span className="absolute -left-1.75 mt-1.5 h-3 w-3 rounded-full bg-indigo-600" />
              <p className="text-sm font-semibold text-indigo-600 dark:text-indigo-400">
                {i.when}
              </p>
              <p className="text-sm text-muted-foreground">{i.what}</p>
            </li>
          ))}
        </ol>
        <PageBadges pages={block.pages.filter((p) => p > 0)} />
      </CardContent>
    </Card>
  );
}

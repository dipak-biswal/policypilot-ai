import type { Block } from "@/types";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { BlockGrid } from "./BlockGrid";
import { TAB_GROUPS, TABS_MIN_BLOCKS } from "./registry";

export function BlockTabs({ blocks }: { blocks: Block[] }) {
  const groups = TAB_GROUPS.map((g) => ({
    ...g,
    blocks: blocks.filter((b) => g.types.includes(b.type)),
  })).filter((g) => g.blocks.length > 0);

  if (blocks.length <= TABS_MIN_BLOCKS || groups.length < 2) {
    return <BlockGrid blocks={blocks} />;
  }

  return (
    <Tabs defaultValue={groups[0].id}>
      <TabsList className="mb-3 w-full justify-start overflow-x-auto">
        {groups.map((g) => (
          <TabsTrigger key={g.id} value={g.id}>
            {g.label}{" "}
            <span className="ml-1 text-xs text-muted-foreground">
              {g.blocks.length}
            </span>
          </TabsTrigger>
        ))}
      </TabsList>
      {groups.map((g) => (
        <TabsContent key={g.id} value={g.id}>
          <BlockGrid blocks={g.blocks} />
        </TabsContent>
      ))}
    </Tabs>
  );
}

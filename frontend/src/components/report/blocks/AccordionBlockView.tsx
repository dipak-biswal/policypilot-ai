import type { AccordionBlock } from "@/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { PageBadges } from "./PageBadges";

export function AccordionBlockView({ block }: { block: AccordionBlock }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base">{block.title}</CardTitle>
      </CardHeader>
      <CardContent>
        <Accordion>
          {block.items.map((i) => (
            <AccordionItem key={i.title} value={i.title}>
              <AccordionTrigger>{i.title}</AccordionTrigger>
              <AccordionContent>
                <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
                  {i.bullets.map((b) => (
                    <li key={b}>{b}</li>
                  ))}
                </ul>
              </AccordionContent>
            </AccordionItem>
          ))}
        </Accordion>
        <PageBadges pages={block.pages} />
      </CardContent>
    </Card>
  );
}

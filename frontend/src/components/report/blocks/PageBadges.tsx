import { Badge } from "@/components/ui/badge";

export function PageBadges({ pages }: { pages: number[] }) {
  if (!pages?.length) return null;
  return (
    <div className="mt-2 flex flex-wrap gap-1">
      {pages.map((p) => <Badge key={p} variant="secondary">Page {p}</Badge>)}
    </div>
  );
}
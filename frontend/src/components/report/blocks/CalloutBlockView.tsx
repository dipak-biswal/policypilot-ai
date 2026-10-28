import type { CalloutBlock } from "@/types";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { PageBadges } from "./PageBadges";

const TONE = {
  warning: {
    icon: "⚠️",
    cls: "border-amber-300 bg-amber-50 dark:bg-amber-950/40",
  },
  info: { icon: "ℹ️", cls: "border-sky-300 bg-sky-50 dark:bg-sky-950/40" },
  success: {
    icon: "✅",
    cls: "border-emerald-300 bg-emerald-50 dark:bg-emerald-950/40",
  },
};

export function CalloutBlockView({ block }: { block: CalloutBlock }) {
  const t = TONE[block.tone];
  return (
    <Alert className={t.cls}>
      <AlertTitle>
        {t.icon} {block.title}
      </AlertTitle>
      <AlertDescription>
        {block.text}
        <PageBadges pages={block.pages} />
      </AlertDescription>
    </Alert>
  );
}

import type { AgentStep } from "@/types";

export function AgentSteps({
  steps,
  done,
}: {
  steps: AgentStep[];
  done: boolean;
}) {
  if (!steps.length) return null;
  return (
    <ul className="mb-2 space-y-1 text-xs text-slate-500 dark:text-slate-400">
      {steps.map((s, i) => {
        const active = !done && i === steps.length - 1;
        return (
          <li key={i} className="flex items-center gap-2 animate-in fade-in">
            <span className={active ? "animate-pulse" : ""}>{s.step}</span>
            {s.detail && (
              <code className="truncate rounded bg-slate-100 px-1 dark:bg-slate-800">
                {s.detail}
              </code>
            )}
            {!active && <span className="text-emerald-500">✓</span>}
          </li>
        );
      })}
    </ul>
  );
}

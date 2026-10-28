export function AnswerSkeleton() {
  return (
    <div className="flex items-start gap-3" aria-label="Loading answer">
      <div className="h-7 w-7 shrink-0 animate-pulse rounded-full bg-indigo-100 dark:bg-indigo-900/40" />
      <div className="w-full max-w-md space-y-2.5 rounded-2xl border border-slate-200 bg-white p-4 dark:border-slate-700 dark:bg-slate-900">
        <div className="h-3 w-11/12 animate-pulse rounded bg-slate-200 dark:bg-slate-700" />
        <div className="h-3 w-full animate-pulse rounded bg-slate-200 dark:bg-slate-700" />
        <div className="h-3 w-3/4 animate-pulse rounded bg-slate-200 dark:bg-slate-700" />
        <div className="h-3 w-1/2 animate-pulse rounded bg-slate-200 dark:bg-slate-700" />
      </div>
    </div>
  );
}

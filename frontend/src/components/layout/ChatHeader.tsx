import { ThemeToggle } from "./ThemeToggle";

type Props = {
  document: string | null;
  onNewChat: () => void;
  canClear: boolean;
};

export function ChatHeader({ document, onNewChat, canClear }: Props) {
  return (
    <header className="flex items-center justify-between gap-3 border-b border-slate-200 bg-white/80 px-5 py-3 backdrop-blur dark:border-slate-800 dark:bg-slate-900/80">
      {document ? (
        <div className="flex min-w-0 items-center gap-2 rounded-full border border-slate-200 bg-slate-50 py-1 pl-1 pr-3 dark:border-slate-700 dark:bg-slate-800">
          <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-red-50 text-[9px] font-bold text-red-600 dark:bg-red-500/10 dark:text-red-400">
            PDF
          </span>
          <span
            className="truncate text-sm font-medium text-slate-800 dark:text-slate-100"
            title={document}
          >
            {document}
          </span>
          <span className="flex shrink-0 items-center gap-1 text-xs text-emerald-600 dark:text-emerald-400">
            <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
            Ready
          </span>
        </div>
      ) : (
        <p className="text-sm text-slate-400">No document selected</p>
      )}

      <div className="hidden shrink-0 items-center gap-2 md:flex">
        <ThemeToggle />
        <button
          type="button"
          onClick={onNewChat}
          disabled={!canClear}
          className="inline-flex items-center gap-1.5 rounded-lg bg-indigo-600 px-3 py-1.5 text-sm font-medium text-white shadow-sm transition hover:bg-indigo-700 disabled:cursor-not-allowed disabled:bg-slate-200 disabled:text-slate-400 disabled:shadow-none dark:disabled:bg-slate-800 dark:disabled:text-slate-500"
        >
          <svg
            viewBox="0 0 24 24"
            className="h-4 w-4"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
          >
            <path d="M12 5v14M5 12h14" />
          </svg>
          New chat
        </button>
      </div>
    </header>
  );
}

import { ThemeToggle } from "./ThemeToggle";

type Props = {
  document: string | null;
  onNewChat: () => void;
  canClear: boolean;
};

export function ChatHeader({ document, onNewChat, canClear }: Props) {
  return (
    <header className="flex items-center justify-between gap-3 border-b border-slate-200 bg-white px-5 py-3 dark:border-slate-800 dark:bg-slate-900">
      <p className="truncate text-sm text-slate-500 dark:text-slate-400">
        {document ? (
          <>
            Chatting with{" "}
            <span className="font-medium text-slate-800 dark:text-slate-100">
              {document}
            </span>
          </>
        ) : (
          "No document selected"
        )}
      </p>

      <div className="flex shrink-0 gap-2">
        <ThemeToggle />
        <button
          type="button"
          onClick={onNewChat}
          disabled={!canClear}
          className="rounded-lg border border-slate-200 px-3 py-1.5 text-xs font-medium text-slate-600 hover:bg-slate-50 disabled:opacity-40 dark:border-slate-700 dark:text-slate-300 dark:hover:bg-slate-800"
        >
          ＋ New chat
        </button>
      </div>
    </header>
  );
}

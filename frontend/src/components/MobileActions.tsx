import { ThemeToggle } from "./ThemeToggle";

type Props = { onNewChat: () => void; canClear: boolean };

export function MobileActions({ onNewChat, canClear }: Props) {
  return (
    <>
      <ThemeToggle />
      <button
        type="button"
        onClick={onNewChat}
        disabled={!canClear}
        aria-label="New chat"
        className="flex h-9 w-9 items-center justify-center rounded-lg bg-indigo-600 text-white disabled:bg-slate-200 disabled:text-slate-400 dark:disabled:bg-slate-800"
      >
        <svg
          viewBox="0 0 24 24"
          className="h-5 w-5"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
        >
          <path d="M12 5v14M5 12h14" />
        </svg>
      </button>
    </>
  );
}

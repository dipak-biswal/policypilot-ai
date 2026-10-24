interface Props {
  documents: string[];
  selected: string | null;
  onSelect: (name: string) => void;
  onDelete: (name: string) => void;
  deleting: string | null;
}

export function DocumentPicker({
  documents,
  selected,
  onSelect,
  onDelete,
  deleting,
}: Props) {
  if (documents.length === 0) return null;

  return (
    <div className="flex flex-col gap-2 min-h-0">
      <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">
        Your documents
      </p>
      <ul className="flex flex-col gap-1 overflow-y-auto">
        {documents.map((d) => {
          const active = d === selected;
          const busy = deleting === d;
          return (
            <li key={d} className="group flex items-center gap-1">
              <button
                type="button"
                onClick={() => onSelect(d)}
                title={d}
                className={`min-w-0 flex-1 flex items-center gap-2 rounded-lg px-3 py-2 text-left text-sm transition ${
                  active
                    ? "bg-indigo-50 text-indigo-700 font-medium ring-1 ring-indigo-200 dark:bg-indigo-500/10 dark:text-indigo-300 dark:ring-indigo-500/30"
                    : "text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800"
                } ${busy ? "opacity-50" : ""}`}
              >
                <span>📄</span>
                <span className="truncate">{d}</span>
                {active && (
                  <span className="ml-auto h-2 w-2 shrink-0 rounded-full bg-indigo-500" />
                )}
              </button>
              <button
                type="button"
                onClick={() => onDelete(d)}
                disabled={busy}
                title={`Delete ${d}`}
                aria-label={`Delete ${d}`}
                className="shrink-0 rounded-lg p-2 text-slate-400 transition hover:bg-red-50 hover:text-red-600 disabled:cursor-wait disabled:opacity-50 dark:text-slate-500 dark:hover:bg-red-500/10 dark:hover:text-red-400"
              >
                {busy ? (
                  <span className="block h-4 w-4 animate-spin rounded-full border-2 border-red-400 border-t-transparent" />
                ) : (
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth={2}
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    className="h-4 w-4"
                  >
                    <path d="M3 6h18" />
                    <path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
                    <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6" />
                    <path d="M10 11v6M14 11v6" />
                  </svg>
                )}
              </button>
            </li>
          );
        })}
      </ul>
    </div>
  );
}

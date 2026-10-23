interface Props {
  documents: string[];
  selected: string | null;
  onSelect: (name: string) => void;
}

export function DocumentPicker({ documents, selected, onSelect }: Props) {
  if (documents.length === 0) return null;

  return (
    <div className="flex flex-col gap-2 min-h-0">
      <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">
        Your documents
      </p>
      <ul className="flex flex-col gap-1 overflow-y-auto">
        {documents.map((d) => {
          const active = d === selected;
          return (
            <li key={d}>
              <button
                type="button"
                onClick={() => onSelect(d)}
                title={d}
                className={`w-full flex items-center gap-2 rounded-lg px-3 py-2 text-left text-sm transition ${
                  active
                    ? "bg-indigo-50 text-indigo-700 font-medium ring-1 ring-indigo-200"
                    : "text-slate-600 hover:bg-slate-100"
                }`}
              >
                <span>📄</span>
                <span className="truncate">{d}</span>
                {active && (
                  <span className="ml-auto h-2 w-2 shrink-0 rounded-full bg-indigo-500" />
                )}
              </button>
            </li>
          );
        })}
      </ul>
    </div>
  );
}

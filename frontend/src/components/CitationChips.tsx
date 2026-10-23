import type { Citation } from "../types";

export function CitationChips({ citations }: { citations: Citation[] }) {
  if (citations.length === 0) return null;

  return (
    <div className="flex flex-wrap gap-1.5">
      {citations.map((c) => (
        <span
          key={`${c.source}-${c.page}`}
          className="group relative inline-flex items-center gap-1 rounded-full border border-indigo-200 bg-indigo-50 px-2.5 py-0.5 text-xs font-medium text-indigo-700 cursor-help hover:bg-indigo-100"
        >
          📄 Page {c.page}
          {c.snippet && (
            <span className="pointer-events-none absolute bottom-full left-0 z-10 mb-2 hidden w-72 rounded-lg bg-slate-800 p-3 text-xs font-normal leading-snug text-slate-100 shadow-lg group-hover:block">
              <span className="block mb-1 text-slate-400">
                {c.source}, p.{c.page}
              </span>
              {c.snippet.length > 220
                ? c.snippet.slice(0, 220) + "..."
                : c.snippet}
            </span>
          )}
        </span>
      ))}
    </div>
  );
}

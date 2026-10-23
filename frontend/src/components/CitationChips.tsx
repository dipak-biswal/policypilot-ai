import type { Citation } from "../types";

export function CitationChips({ citations }: { citations: Citation[] }) {
  if (citations.length === 0) return null;
  return (
    <div style={{ marginTop: 6, display: "flex", gap: 6, flexWrap: "wrap" }}>
      {citations.map((c) => {
        return (
          <span
            key={`${c.source}-${c.page}`}
            title={c.snippet}
            style={{
              fontSize: 12,
              padding: "2px 8px",
              borderRadius: 12,
              background: "#e0e7ff",
            }}
          >
            📄 {c.source}, p.{c.page}
          </span>
        );
      })}
    </div>
  );
}

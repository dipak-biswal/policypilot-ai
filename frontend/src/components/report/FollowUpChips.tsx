export function FollowUpChips({
  questions,
  onPick,
}: {
  questions: string[];
  onPick: (q: string) => void;
}) {
  return (
    <div
      style={{ display: "flex", flexDirection: "column", gap: 6, marginTop: 8 }}
    >
      {questions.map((q) => (
        <button
          key={q}
          onClick={() => onPick(q)}
          style={{
            textAlign: "left",
            padding: "6px 10px",
            borderRadius: 8,
            border: "1px solid #c7d2fe",
            background: "#eef2ff",
            cursor: "pointer",
          }}
        >
          💡 {q}
        </button>
      ))}
    </div>
  );
}

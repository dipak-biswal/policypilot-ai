interface Props {
  documents: string[];
  selected: string | null;
  onSelect: (name: string) => void;
}

export function DocumentPicker({ documents, selected, onSelect }: Props) {
  if (documents.length === 0) return null;
  return (
    <label
      style={{ display: "flex", gap: 8, alignItems: "center", margin: "8px 0" }}
    >
      Ask about:
      <select value={selected ?? ""} onChange={(e) => onSelect(e.target.value)}>
        {documents.map((d) => (
          <option key={d} value={d}>
            {d}
          </option>
        ))}
      </select>
    </label>
  );
}

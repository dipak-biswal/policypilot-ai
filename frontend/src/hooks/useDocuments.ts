import { useEffect, useState } from "react";

const KEY = "policypilot.documents";

export function useDocuments() {
  const [documents, setDocuments] = useState<string[]>(() =>
    JSON.parse(localStorage.getItem(KEY) ?? "[]"),
  );
  const [selected, setSelected] = useState<string | null>(documents[0] ?? null);

  useEffect(
    () => localStorage.setItem(KEY, JSON.stringify(documents)),
    [documents],
  );

  const addDocument = (name: string) => {
    setDocuments((prev) => (prev.includes(name) ? prev : [...prev, name]));
    setSelected(name);
  };

  return { documents, selected, setSelected, addDocument };
}

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

  const removeDocument = (name: string) => {
    setDocuments((prev) => {
      const next = prev.filter((d) => d !== name);
      setSelected((sel) => (sel === name ? (next[0] ?? null) : sel));
      return next;
    });
  };

  return { documents, selected, setSelected, addDocument, removeDocument };
}

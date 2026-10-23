import { useState, type FormEvent } from "react";

type Props = { onSend: (text: string) => void; disabled?: boolean };

export function ChatInput({ onSend, disabled }: Props) {
  const [text, setText] = useState("");

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    const q = text.trim();
    if (!q || disabled) return;
    onSend(q);
    setText("");
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="border-t border-slate-200 bg-white p-4"
    >
      <div className="mx-auto max-w-3xl flex gap-2">
        <input
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder={
            disabled
              ? "Upload or pick a document to start..."
              : "Ask about your policy..."
          }
          disabled={disabled}
          className="flex-1 rounded-xl border border-slate-300 px-4 py-3 text-sm outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 disabled:bg-slate-100"
        />
        <button
          type="submit"
          disabled={disabled || !text.trim()}
          className="rounded-xl bg-indigo-600 px-5 py-3 text-sm font-medium text-white hover:bg-indigo-700 disabled:opacity-40"
        >
          Send
        </button>
      </div>
    </form>
  );
}

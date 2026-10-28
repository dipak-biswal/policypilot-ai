import {
  useEffect,
  useRef,
  useState,
  type FormEvent,
  type KeyboardEvent,
} from "react";

type Props = { onSend: (text: string) => void; disabled?: boolean };

export function ChatInput({ onSend, disabled }: Props) {
  const [text, setText] = useState("");
  const ref = useRef<HTMLTextAreaElement>(null);

  // auto-grow up to ~6 lines
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = `${Math.min(el.scrollHeight, 160)}px`;
  }, [text]);

  function submit() {
    const q = text.trim();
    if (!q || disabled) return;
    onSend(q);
    setText("");
  }

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    submit();
  }

  function handleKeyDown(e: KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-linear-to-t from-white via-white to-transparent px-4 pb-4 pt-2 dark:from-slate-950 dark:via-slate-950"
    >
      <div className="mx-auto max-w-3xl">
        <div className="flex items-end gap-2 rounded-2xl border border-slate-200 bg-white p-2 shadow-lg shadow-slate-200/60 focus-within:border-indigo-400 focus-within:ring-4 focus-within:ring-indigo-100 dark:border-slate-700 dark:bg-slate-900 dark:shadow-none dark:focus-within:ring-indigo-900/40">
          <textarea
            ref={ref}
            rows={1}
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={
              disabled
                ? "Upload or pick a document to start..."
                : "Ask about your policy..."
            }
            disabled={disabled}
            className="max-h-40 flex-1 resize-none bg-transparent px-3 py-2.5 text-base outline-none placeholder:text-slate-400 disabled:cursor-not-allowed dark:text-slate-100"
          />
          <button
            type="submit"
            disabled={disabled || !text.trim()}
            aria-label="Send"
            className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-indigo-600 text-white transition hover:bg-indigo-700 disabled:opacity-30"
          >
            <svg
              viewBox="0 0 24 24"
              className="h-5 w-5"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M5 12h14M13 6l6 6-6 6" />
            </svg>
          </button>
        </div>
        <p className="mt-2 text-center text-xs text-slate-400">
          <kbd className="font-sans">Enter</kbd> to send ·{" "}
          <kbd className="font-sans">Shift + Enter</kbd> for a new line ·
          Answers cite policy pages
        </p>
      </div>
    </form>
  );
}

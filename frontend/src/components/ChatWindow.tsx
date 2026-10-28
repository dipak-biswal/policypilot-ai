import { useEffect, useRef } from "react";
import type { Message } from "../types";
import { Messagebubble } from "./MessageBubble";
import { StarterChips } from "./StarterChips";

type Props = {
  messages: Message[];
  loading: boolean;
  onFollowUp: (q: string) => void;
};

export function ChatWindow({ messages, loading, onFollowUp }: Props) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto">
      <div className="mx-auto max-w-3xl px-4 py-6 flex flex-col gap-4">
        {messages.length === 0 && (
          <div className="mt-16 text-center sm:mt-24">
            <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-indigo-500 to-violet-500 text-3xl shadow-lg shadow-indigo-200 dark:shadow-none">
              🛡️
            </div>
            <h2 className="mt-5 text-2xl font-semibold text-slate-800 sm:text-3xl dark:text-slate-100">
              Ask anything about your policy
            </h2>
            <p className="mx-auto mt-2 max-w-md text-base text-slate-500 dark:text-slate-400">
              Coverage, exclusions, waiting periods or claims. Every answer is
              grounded in the PDF with page citations.
            </p>
            <div className="mt-4 flex flex-wrap justify-center gap-2 text-xs">
              {[
                "📄 Page citations",
                "📊 Summary reports",
                "🧠 Remembers context",
              ].map((b) => (
                <span
                  key={b}
                  className="rounded-full bg-indigo-50 px-3 py-1 font-medium text-indigo-700 dark:bg-indigo-950/50 dark:text-indigo-300"
                >
                  {b}
                </span>
              ))}
            </div>
            <StarterChips onPick={onFollowUp} />
          </div>
        )}

        {messages.map((m, i) => (
          <Messagebubble
            key={m.id}
            message={m}
            onFollowUp={onFollowUp}
            streaming={
              loading && i === messages.length - 1 && m.role === "assistant"
            }
          />
        ))}

        {loading && messages.at(-1)?.text === "" && (
          <p className="text-sm text-slate-400 animate-pulse">Thinking...</p>
        )}
        <div ref={bottomRef} />
      </div>
    </div>
  );
}

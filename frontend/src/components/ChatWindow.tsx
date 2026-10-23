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
          <div className="mt-20 text-center">
            <p className="text-4xl">🛡️</p>
            <h2 className="mt-3 text-lg font-semibold text-slate-700">
              Ask anything about your policy
            </h2>
            <p className="mt-1 text-sm text-slate-400">
              Answers are grounded in the PDF with page citations.
            </p>
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

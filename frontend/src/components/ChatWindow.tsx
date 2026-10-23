import { useEffect, useRef } from "react";
import type { Message } from "../types";
import { Messagebubble } from "./MessageBubble";

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
          <div className="mt-24 text-center text-slate-400">
            <p className="text-4xl">💬</p>
            <p className="mt-3 text-sm">
              Ask anything about your policy: waiting periods, exclusions,
              claims...
            </p>
          </div>
        )}

        {messages.map((m) => (
          <Messagebubble key={m.id} message={m} onFollowUp={onFollowUp} />
        ))}

        {loading && messages.at(-1)?.text === "" && (
          <p className="text-sm text-slate-400 animate-pulse">Thinking...</p>
        )}
        <div ref={bottomRef} />
      </div>
    </div>
  );
}

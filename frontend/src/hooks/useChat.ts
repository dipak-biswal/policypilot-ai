import { useRef, useState } from "react";
import type { Message } from "../types";
import { streamAgent } from "../api/agent";
import { makeId } from "../utils/id";

export function useChat(source: string | null) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const threadId = useRef(makeId());

  function updateMessage(id: string, update: (m: Message) => Message) {
    setMessages((all) => all.map((m) => (m.id === id ? update(m) : m)));
  }

  async function send(question: string) {
    if (!question.trim()) return;
    const assistantId = makeId();
    setMessages((m) => [
      ...m,
      { id: makeId(), role: "user", text: question },
      { id: assistantId, role: "assistant", text: "" },
    ]);
    setLoading(true);

    try {
      await streamAgent(question, source, threadId.current, {
        onToken: (t) =>
          updateMessage(assistantId, (m) => ({ ...m, text: m.text + t })),
        onReport: (report) =>
          updateMessage(assistantId, (m) => ({ ...m, report })),
        onCitations: (citations) =>
          updateMessage(assistantId, (m) => ({ ...m, citations })),
      });
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Something went wrong.";
      updateMessage(assistantId, (m) => ({
        ...m,
        text: msg,
      }));
    } finally {
      setLoading(false);
    }
  }

  function clear() {
    setMessages([]);
    threadId.current = makeId();
  }

  return { messages, loading, send, clear };
}

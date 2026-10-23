import { useState } from "react";
import type { Message } from "../types";
// import { streamQuestion } from "../api/chat";
import {
  // runAgent,
  streamAgent,
} from "../api/agent";
import { makeId } from "../utils/id";

export function useChat(source: string | null) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

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
      await streamAgent(question, source, {
        onToken: (t) =>
          updateMessage(assistantId, (m) => ({ ...m, text: m.text + t })),
        onReport: (report) =>
          updateMessage(assistantId, (m) => ({ ...m, report })),
        onCitations: (citations) =>
          updateMessage(assistantId, (m) => ({ ...m, citations })),
      });
    } catch (error) {
      updateMessage(assistantId, (m) => ({
        ...m,
        text: `Error: ${(error as Error).message}`,
      }));
    } finally {
      setLoading(false);
    }
  }

  return { messages, loading, send };
}

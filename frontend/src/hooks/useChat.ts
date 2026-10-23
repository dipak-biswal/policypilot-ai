import { useState } from "react";
import type { Message } from "../types";
// import { streamQuestion } from "../api/chat";
import { runAgent } from "../api/agent";

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  function updateMessage(id: string, update: (m: Message) => Message) {
    setMessages((all) => all.map((m) => (m.id === id ? update(m) : m)));
  }

  async function send(question: string) {
    if (!question.trim()) return;
    const assistantId = crypto.randomUUID();
    setMessages((m) => [
      ...m,
      { id: crypto.randomUUID(), role: "user", text: question },
      { id: assistantId, role: "assistant", text: "" },
    ]);
    setLoading(true);

    // try {
    //   await streamQuestion(question, {
    //     onToken: (token) =>
    //       updateMessage(assistantId, (m) => ({ ...m, text: m.text + token })),
    //     onCitations: (citations: Citation[]) =>
    //       updateMessage(assistantId, (m) => ({ ...m, citations })),
    //   });
    // }
    try {
      const res = await runAgent(question);
      updateMessage(assistantId, (m) => ({
        ...m,
        text: res.answer,
        citations: res.citations,
        report: res.report,
      }));
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

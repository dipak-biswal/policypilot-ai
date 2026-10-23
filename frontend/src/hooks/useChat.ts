import { useState } from "react";
import type { Message } from "../types";
import { askQuestion } from "../api/chat";

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  async function send(question: string) {
    if (!question.trim()) return;
    setMessages((m) => [
      ...m,
      { id: crypto.randomUUID(), role: "user", text: question },
    ]);
    setLoading(true);

    try {
      const res = await askQuestion(question);
      setMessages((m) => [
        ...m,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          text: res.answer,
          citations: res.citations,
        },
      ]);
    } catch (error) {
      setMessages((m) => [
        ...m,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          text: `Error: ${(error as Error).message}`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return { messages, loading, send };
}

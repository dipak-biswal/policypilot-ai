import { useState } from "react";
import type { Citation, Message } from "../types";
import { streamQuestion } from "../api/chat";

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

    //   try {
    //     const res = await askQuestion(question);
    //     setMessages((m) => [
    //       ...m,
    //       {
    //         id: crypto.randomUUID(),
    //         role: "assistant",
    //         text: res.answer,
    //         citations: res.citations,
    //       },
    //     ]);
    //   } catch (error) {
    //     setMessages((m) => [
    //       ...m,
    //       {
    //         id: crypto.randomUUID(),
    //         role: "assistant",
    //         text: `Error: ${(error as Error).message}`,
    //       },
    //     ]);
    //   } finally {
    //     setLoading(false);
    //   }

    try {
      await streamQuestion(question, {
        onToken: (token) =>
          updateMessage(assistantId, (m) => ({ ...m, text: m.text + token })),
        onCitations: (citations: Citation[]) =>
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

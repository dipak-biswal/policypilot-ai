import { useRef, useState } from "react";
import type { Message } from "../types";
import { resumeAgent, streamAgent } from "../api/agent";
import { makeId } from "../utils/id";

export function useChat(source: string | null) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const threadId = useRef(makeId());

  function updateMessage(id: string, update: (m: Message) => Message) {
    setMessages((all) => all.map((m) => (m.id === id ? update(m) : m)));
  }

  const handlers = (assistantId: string) => ({
    onToken: (t: string) =>
      updateMessage(assistantId, (m) => ({ ...m, text: m.text + t })),
    onReport: (report: Message["report"]) =>
      updateMessage(assistantId, (m) => ({ ...m, report })),
    onCitations: (citations: NonNullable<Message["citations"]>) =>
      updateMessage(assistantId, (m) => ({ ...m, citations })),
    onMetrics: (metrics: NonNullable<Message["metrics"]>) =>
      updateMessage(assistantId, (m) => ({ ...m, metrics })),
    onBlocks: (blocks: NonNullable<Message["blocks"]>) =>
      updateMessage(assistantId, (m) => ({ ...m, blocks })),
    onStep: (s: NonNullable<Message["steps"]>[number]) =>
      updateMessage(assistantId, (m) => ({
        ...m,
        steps: [...(m.steps ?? []), s],
      })),
  });

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
        ...handlers(assistantId),
        onInterrupt: (data) =>
          updateMessage(assistantId, (m) => ({
            ...m,
            interrupt: data,
            pendingApproval: true,
            text: data.draft,
          })),
      });
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Something went wrong.";
      updateMessage(assistantId, (m) => ({ ...m, text: msg }));
    } finally {
      setLoading(false);
    }
  }

  async function respond(
    messageId: string,
    action: "approve" | "edit" | "reject",
    text?: string,
  ) {
    setLoading(true);
    updateMessage(messageId, (m) => ({
      ...m,
      pendingApproval: false,
      interrupt: null,
      text: "",
    }));
    try {
      await resumeAgent(threadId.current, action, text, handlers(messageId));
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Something went wrong.";
      updateMessage(messageId, (m) => ({ ...m, text: msg }));
    } finally {
      setLoading(false);
    }
  }

  function clear() {
    setMessages([]);
    threadId.current = makeId();
  }

  return { messages, loading, send, clear, respond };
}

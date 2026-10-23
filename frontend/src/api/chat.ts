import type { ChatResponse, Citation } from "../types";
import { API_URL, request } from "./client";
import { readSSE } from "./sse";

type StreamHandlers = {
  onToken: (token: string) => void;
  onCitations: (citations: Citation[]) => void;
};

export function askQuestion(question: string) {
  return request<ChatResponse>("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
}

export async function streamQuestion(
  question: string,
  handlers: StreamHandlers,
) {
  const res = await fetch(`${API_URL}/chat/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
  if (!res.ok || !res.body) throw new Error(`${res.status}: stream failed`);
  for await (const { event, data } of readSSE(res)) {
    if (event === "token") handlers.onToken(data as string);
    else if (event === "citations") handlers.onCitations(data as Citation[]);
    else if (event === "done") break;
  }
}

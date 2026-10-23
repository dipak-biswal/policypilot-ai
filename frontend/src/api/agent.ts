import type { AgentResponse, Citation, Intent, Report } from "../types";
import { API_URL, request } from "./client";
import { readSSE } from "./sse";

export interface AgentStreamHandlers {
  onIntent?: (intent: Intent) => void;
  onToken: (text: string) => void;
  onReport?: (report: Report) => void;
  onCitations?: (citations: Citation[]) => void;
}

export function runAgent(question: string) {
  return request<AgentResponse>("/agent", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
}

export async function streamAgent(question: string, h: AgentStreamHandlers) {
  const res = await fetch(`${API_URL}/agent/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });

  if (!res.ok || !res.body)
    throw new Error(`Agent stream failed: ${res.status}`);

  for await (const { event, data } of readSSE(res)) {
    if (event === "intent") h.onIntent?.(data.intent);
    else if (event === "token") h.onToken(data.text);
    else if (event === "report") h.onReport?.(data);
    else if (event === "citations") h.onCitations?.(data);
    else if (event === "done") break;
  }
}

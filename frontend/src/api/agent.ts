import type {
  AgentResponse,
  AgentStep,
  AgentStreamEvent,
  Block,
  Citation,
  Intent,
  Metrics,
  Report,
} from "../types";
import { API_URL, request } from "./client";
import { readSSE } from "./sse";

export interface AgentStreamHandlers {
  onIntent?: (intent: Intent) => void;
  onToken: (text: string) => void;
  onReport?: (report: Report) => void;
  onCitations?: (citations: Citation[]) => void;
  onMetrics?: (m: Metrics) => void;
  onBlocks?: (blocks: Block[]) => void;
  onStep?: (s: AgentStep) => void;
}

export function runAgent(question: string) {
  return request<AgentResponse>("/agent", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
}

export async function streamAgent(
  question: string,
  source: string | null,
  threadId: string,
  h: AgentStreamHandlers,
) {
  const res = await fetch(`${API_URL}/agent/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, source, thread_id: threadId }),
  });

  if (res.status === 429) {
    throw new Error(
      "You're sending questions too fast. Please wait a minute and try again.",
    );
  }

  if (!res.ok || !res.body)
    throw new Error(`Agent stream failed: ${res.status}`);

  for await (const raw of readSSE(res)) {
    const e = raw as AgentStreamEvent;
    switch (e.event) {
      case "intent":
        h.onIntent?.(e.data.intent);
        break;
      case "token":
        h.onToken?.(e.data.text);
        break;
      case "report":
        h.onReport?.(e.data);
        break;
      case "citations":
        h.onCitations?.(e.data);
        break;
      case "metrics":
        h.onMetrics?.(e.data as Metrics);
        break;
      case "blocks":
        h.onBlocks?.(e.data as Block[]);
        break;
      case "step":
        h.onStep?.(e.data);
        break;
      case "done":
        return;
    }
  }
}

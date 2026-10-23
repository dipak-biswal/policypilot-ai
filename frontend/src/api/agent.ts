import type { AgentResponse } from "../types";
import { request } from "./client";

export function runAgent(question: string) {
  return request<AgentResponse>("/agent", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
}

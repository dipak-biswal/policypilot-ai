import type { ChatResponse } from "../types";
import { request } from "./client";

export function askQuestion(question: string) {
  return request<ChatResponse>("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
}

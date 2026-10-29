import type { Block } from "./blocks";
export * from "./blocks";

export type Citation = { source: string; page: number; snippet: string };
export type ChatResponse = { answer: string; citations: Citation[] };
export type UploadResponse = {
  filename: string;
  page_count: number;
  chunks_indexed: number;
};
export type Message = {
  id: string;
  role: "user" | "assistant";
  text: string;
  citations?: Citation[];
  report?: Report | null;
  metrics?: Metrics;
  blocks?: Block[];
  steps?: AgentStep[];
};

export type Intent = "qa" | "summary" | "report";
export type TableData = { columns: string[]; rows: string[][] };
export type KeyValue = { label: string; value: string };

export type ReportSection = {
  title: string;
  layout: "bullets" | "table" | "keyValue";
  bullets: string[];
  table: TableData | null;
  items: KeyValue[];
  pages: number[];
};

export type Report = {
  title: string;
  summary: string;
  blocks: Block[];
  follow_up_questions: string[];
};

export type AgentResponse = {
  intent: string;
  answer: string;
  citations: Citation[];
  report: Report | null;
};

export type AgentStreamEvent =
  | { event: "intent"; data: { intent: Intent } }
  | { event: "token"; data: { text: string } }
  | { event: "report"; data: Report }
  | { event: "citations"; data: Citation[] }
  | { event: "metrics"; data: Metrics }
  | { event: "blocks"; data: Block[] }
  | { event: "step"; data: AgentStep }
  | { event: "done"; data: Record<string, never> };

export interface Metrics {
  latency_ms: number;
  input_tokens: number;
  output_tokens: number;
  cost_usd: number;
}

export type AgentStep = { step: string; detail?: string };

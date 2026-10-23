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
  sections: ReportSection[];
  follow_up_questions: string[];
};

export type AgentResponse = {
  intent: string;
  answer: string;
  citations: Citation[];
  report: Report | null;
};

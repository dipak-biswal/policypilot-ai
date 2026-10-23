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
};

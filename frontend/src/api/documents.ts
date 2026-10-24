import type { UploadResponse } from "../types";
import { request } from "./client";

export function uploadPdf(file: File) {
  const form = new FormData();
  form.append("file", file);

  return request<UploadResponse>("/documents", { method: "POST", body: form });
}

export function deleteDocument(filename: string) {
  return request<{ filename: string; chunks_deleted: number }>(
    `/documents/${encodeURIComponent(filename)}`,
    { method: "DELETE" },
  );
}

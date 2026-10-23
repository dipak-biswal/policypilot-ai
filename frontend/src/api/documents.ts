import type { UploadResponse } from "../types";
import { request } from "./client";

export function uploadPdf(file: File) {
  const form = new FormData();
  form.append("file", file);

  return request<UploadResponse>("/documents", { method: "POST", body: form });
}

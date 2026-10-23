import { request } from "./client";
import type { UploadResponse } from "../types";

export function uploadPdf(file: File) {
  const form = new FormData();
  form.append("file", file);

  return request<UploadResponse>("/documents", { method: "POST", body: form });
}

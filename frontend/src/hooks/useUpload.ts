import { useState } from "react";
import { uploadPdf } from "../api/documents";

export function useUpload() {
  const [status, setStatus] = useState("");
  const [uploading, setUploading] = useState(false);

  async function upload(file: File) {
    setUploading(true);
    setStatus("Uploading and indexing...");

    try {
      const res = await uploadPdf(file);
      setStatus(
        `Indexed ${res.filename}: ${res.page_count} pages, ${res.chunks_indexed} chunks`,
      );
    } catch (error) {
      setStatus(`Upload failed: ${(error as Error).message}`);
    } finally {
      setUploading(false);
    }
  }

  return { status, uploading, upload };
}

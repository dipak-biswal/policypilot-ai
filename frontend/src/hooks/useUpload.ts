import { useState } from "react";
import { uploadPdf } from "../api/documents";

export function useUpload() {
  const [status, setStatus] = useState("");
  const [uploading, setUploading] = useState(false);

  async function upload(file: File): Promise<string | null> {
    setUploading(true);
    setStatus("Uploading and indexing...");

    try {
      const res = await uploadPdf(file);
      setStatus(
        `Indexed ${res.filename}: ${res.page_count} pages, ${res.chunks_indexed} chunks`,
      );
      return res.filename;
    } catch (error) {
      setStatus(`Upload failed: ${(error as Error).message}`);
      return null;
    } finally {
      setUploading(false);
    }
  }

  return { status, uploading, upload };
}

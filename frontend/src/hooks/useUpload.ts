import { useState } from "react";
import { toast } from "sonner";
import { uploadPdf } from "../api/documents";

export function useUpload() {
  const [status, setStatus] = useState("");
  const [uploading, setUploading] = useState(false);

  async function upload(file: File): Promise<string | null> {
    setUploading(true);
    const id = toast.loading(`Uploading ${file.name}...`, {
      description: "Reading pages and building the search index",
    });

    try {
      const res = await uploadPdf(file);
      toast.success(`${res.filename} is ready`, {
        id,
        description: `${res.page_count} pages · ${res.chunks_indexed} chunks indexed`,
      });
      return res.filename;
    } catch (error) {
      toast.error("Upload failed", {
        id,
        description: (error as Error).message,
      });
      return null;
    } finally {
      setUploading(false);
    }
  }

  const clearStatus = () => setStatus("");

  return { status, uploading, upload, clearStatus };
}

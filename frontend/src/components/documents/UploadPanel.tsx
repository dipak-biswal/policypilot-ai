import { useRef, useState, type DragEvent } from "react";

type Props = {
  status: string;
  uploading: boolean;
  onUpload: (file: File) => void;
};

export function UploadPanel({ onUpload, status, uploading }: Props) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);

  function handleFile(file?: File) {
    if (file && file.type === "application/pdf" && !uploading) onUpload(file);
  }

  function handleDrop(e: DragEvent) {
    e.preventDefault();
    setDragging(false);
    handleFile(e.dataTransfer.files[0]);
  }

  const failed = status.toLowerCase().includes("failed");

  return (
    <div className="flex flex-col gap-2">
      <div
        onClick={() => inputRef.current?.click()}
        onDragOver={(e) => {
          e.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
        className={`cursor-pointer rounded-xl border-2 border-dashed p-5 text-center transition ${
          dragging
            ? "border-indigo-500 bg-indigo-50"
            : "border-slate-300 hover:border-indigo-400 hover:bg-slate-50"
        } ${uploading ? "pointer-events-none opacity-60" : ""}`}
      >
        <p className="text-2xl">{uploading ? "⏳" : "📤"}</p>
        <p className="mt-1 text-sm font-medium text-slate-700">
          {uploading ? "Indexing..." : "Upload policy PDF"}
        </p>
        <p className="text-xs text-slate-400">Drag & drop or click</p>
        <input
          ref={inputRef}
          type="file"
          accept="application/pdf"
          className="hidden"
          onChange={(e) => {
            handleFile(e.target.files?.[0]);
            e.target.value = ""; // allow re-uploading the same file
          }}
        />
      </div>
      {status && (
        <p className={`text-xs ${failed ? "text-red-600" : "text-slate-500"}`}>
          {status}
        </p>
      )}
    </div>
  );
}

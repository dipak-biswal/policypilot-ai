type Props = {
  status: string;
  uploading: boolean;
  onUpload: (file: File) => void;
};

export function UploadPanel({ onUpload, status, uploading }: Props) {
  return (
    <div style={{ marginBottom: 16 }}>
      <input
        type="file"
        accept="application/pdf"
        disabled={uploading}
        onChange={(e) => e.target.files?.[0] && onUpload(e.target.files[0])}
      />
      {status && <p>{status}</p>}
    </div>
  );
}

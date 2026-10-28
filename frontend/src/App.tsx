import { useState } from "react";
import { UploadPanel } from "@/components/documents/UploadPanel";
import { DocumentPicker } from "@/components/documents/DocumentPicker";
import { ChatWindow } from "@/components/chat/ChatWindow";
import { ChatInput } from "@/components/chat/ChatInput";
import { Layout } from "@/components/layout/Layout";
import { ChatHeader } from "@/components/layout/ChatHeader";
import { ConfirmDeleteDialog } from "@/components/documents/ConfirmDeleteDialog";
import { useUpload } from "./hooks/useUpload";
import { useDocuments } from "./hooks/useDocuments";
import { useChat } from "./hooks/useChat";
import { deleteDocument } from "./api/documents";
import { toast } from "sonner";
import { Toaster } from "@/components/ui/sonner";
import { MobileActions } from "@/components/layout/MobileActions";

export default function App() {
  const { documents, selected, setSelected, addDocument, removeDocument } =
    useDocuments();
  const { upload, status, uploading, clearStatus } = useUpload();
  const { messages, loading, send, clear } = useChat(selected);
  const [deleting, setDeleting] = useState<string | null>(null);
  const [pendingDelete, setPendingDelete] = useState<string | null>(null);

  const handleUpload = async (file: File) => {
    const filename = await upload(file);
    if (filename) addDocument(filename);
  };

  const confirmDelete = async (name: string) => {
    setPendingDelete(null);
    setDeleting(name);
    try {
      await deleteDocument(name);
    } catch (err) {
      // 404 means it's already gone from the server, so still remove it from the list
      if (!String(err).includes("404")) {
        toast.error("Delete failed", { description: String(err) });

        setDeleting(null);
        return;
      }
    }
    if (name === selected) clear();
    removeDocument(name);
    clearStatus();
    setDeleting(null);
  };

  return (
    <>
      <Toaster position="top-right" richColors closeButton />
      <Layout
        mobileActions={
          <MobileActions
            onNewChat={clear}
            canClear={messages.length > 0 && !loading}
          />
        }
        sidebar={
          <>
            <UploadPanel
              onUpload={handleUpload}
              status={status}
              uploading={uploading}
            />
            <DocumentPicker
              documents={documents}
              selected={selected}
              onSelect={setSelected}
              onDelete={setPendingDelete}
              deleting={deleting}
            />
          </>
        }
      >
        <ChatHeader
          document={selected}
          onNewChat={clear}
          canClear={messages.length > 0 && !loading}
        />
        <ChatWindow
          messages={messages}
          loading={loading}
          onFollowUp={selected ? send : () => {}}
        />
        <ChatInput onSend={send} disabled={loading || !selected} />

        <ConfirmDeleteDialog
          name={pendingDelete}
          onCancel={() => setPendingDelete(null)}
          onConfirm={confirmDelete}
        />
      </Layout>
    </>
  );
}

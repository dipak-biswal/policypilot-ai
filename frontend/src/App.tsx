import { UploadPanel } from "./components/UploadPanel";
import { DocumentPicker } from "./components/DocumentPicker";
import { ChatWindow } from "./components/ChatWindow";
import { ChatInput } from "./components/ChatInput";
import { useUpload } from "./hooks/useUpload";
import { useDocuments } from "./hooks/useDocuments";
import { useChat } from "./hooks/useChat";
import { Layout } from "./components/Layout";

export default function App() {
  const { documents, selected, setSelected, addDocument } = useDocuments();
  const { upload, status, uploading } = useUpload();
  const { messages, loading, send } = useChat(selected);

  const handleUpload = async (file: File) => {
    const filename = await upload(file);
    if (filename) addDocument(filename);
  };

  return (
    <Layout
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
          />
        </>
      }
    >
      <ChatWindow messages={messages} loading={loading} onFollowUp={send} />
      <ChatInput onSend={send} disabled={loading || !selected} />
    </Layout>
  );
}

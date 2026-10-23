import "./App.css";
import { UploadPanel } from "./components/UploadPanel";
import { ChatWindow } from "./components/ChatWindow";
import { ChatInput } from "./components/ChatInput";
import { useUpload } from "./hooks/useUpload";
import { useChat } from "./hooks/useChat";

function App() {
  const { status, uploading, upload } = useUpload();
  const { messages, loading, send } = useChat();

  return (
    <div
      style={{
        maxWidth: 800,
        margin: "0 auto",
        padding: 24,
        fontFamily: "system-ui",
      }}
    >
      <h1>PolicyPilot AI</h1>
      <UploadPanel status={status} uploading={uploading} onUpload={upload} />
      <ChatWindow messages={messages} loading={loading} onFollowUp={send} />
      <ChatInput disabled={loading} onSend={send} />
    </div>
  );
}

export default App;

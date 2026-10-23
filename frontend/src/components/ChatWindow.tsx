import type { Message } from "../types";
import { Messagebubble } from "./MessageBubble";
export function ChatWindow({
  messages,
  loading,
  onFollowUp,
}: {
  messages: Message[];
  loading: boolean;
  onFollowUp: (q: string) => void;
}) {
  return (
    <div
      style={{
        minHeight: 300,
        border: "1px solid #ddd",
        borderRadius: 8,
        padding: 16,
      }}
    >
      {messages.map((m) => (
        <Messagebubble key={m.id} message={m} onFollowUp={onFollowUp} />
      ))}
      {loading && messages.at(-1)?.text === "" && <p>Thinking...</p>}
    </div>
  );
}

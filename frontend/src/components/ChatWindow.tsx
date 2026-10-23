import type { Message } from "../types";
import { Messagebubble } from "./MessageBubble";
export function ChatWindow({
  messages,
  loading,
}: {
  messages: Message[];
  loading: boolean;
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
        <Messagebubble key={m.id} message={m} />
      ))}
      {loading && <p>Thinking...</p>}
    </div>
  );
}

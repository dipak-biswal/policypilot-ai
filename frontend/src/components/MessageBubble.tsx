import type { Message } from "../types";
import { CitationChips } from "./CitationChips";
import { ReportView } from "./report/ReportView";

type Props = {
  message: Message;
  onFollowUp: (q: string) => void;
};

export function Messagebubble({ message, onFollowUp }: Props) {
  if (message.report)
    return (
      <div style={{ margin: "12px 0" }}>
        <ReportView report={message.report} onFollowUp={onFollowUp} />
      </div>
    );

  const isUser = message.role === "user";
  return (
    <div style={{ margin: "12px 0", textAlign: isUser ? "right" : "left" }}>
      <div
        style={{
          display: "inline-block",
          padding: 10,
          borderRadius: 8,
          whiteSpace: "pre-wrap",
          background: isUser ? "#2563eb" : "#f1f5f9",
          color: isUser ? "white" : "black",
        }}
      >
        {message.text}
      </div>
      {message.citations && <CitationChips citations={message.citations} />}
    </div>
  );
}

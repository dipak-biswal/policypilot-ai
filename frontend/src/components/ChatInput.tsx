import { useState } from "react";

export function ChatInput({
  disabled,
  onSend,
}: {
  disabled: boolean;
  onSend: (q: string) => void;
}) {
  const [value, setValue] = useState("");

  function submit() {
    if (!value.trim()) return;
    onSend(value);
    setValue("");
  }

  return (
    <div style={{ display: "flex", gap: 8, marginTop: 12 }}>
      <input
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && submit()}
        placeholder="Ask about your policy..."
        style={{ flex: 1, padding: 10 }}
      />
      <button onClick={submit} disabled={disabled}>
        Send
      </button>
    </div>
  );
}

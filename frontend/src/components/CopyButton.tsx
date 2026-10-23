import { useState } from "react";
import { copyText } from "../utils/copy";

export function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);

  async function handleCopy() {
    if (await copyText(text)) {
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    }
  }

  return (
    <button
      type="button"
      onClick={handleCopy}
      className="rounded-md px-2 py-0.5 text-xs text-slate-400 hover:bg-slate-100 hover:text-slate-600"
    >
      {copied ? "✓ Copied" : "📋 Copy"}
    </button>
  );
}

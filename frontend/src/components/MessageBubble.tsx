import type { Message } from "../types";
import { CitationChips } from "./CitationChips";
import { ReportView } from "./report/ReportView";
import { Markdown } from "./Markdown";
import { TypingDots } from "./TypingDots";
import { CopyButton } from "./CopyButton";
import { MetricsBadge } from "./MetricsBadge";

type Props = {
  message: Message;
  onFollowUp: (q: string) => void;
  streaming?: boolean;
};

export function Messagebubble({
  message,
  onFollowUp,
  streaming = false,
}: Props) {
  if (message.report) {
    return (
      <div className="flex gap-3">
        <Avatar />
        <div className="flex-1 min-w-0">
          <ReportView report={message.report} onFollowUp={onFollowUp} />
        </div>
      </div>
    );
  }

  const isUser = message.role === "user";

  if (isUser) {
    return (
      <div className="flex justify-end">
        <div className="max-w-[80%] rounded-2xl rounded-br-sm bg-indigo-600 px-4 py-2.5 text-sm text-white whitespace-pre-wrap shadow-sm">
          {message.text}
        </div>
      </div>
    );
  }

  return (
    <div className="flex gap-3 dark:prose-invert">
      <Avatar />
      <div className="max-w-[80%] min-w-0">
        <div className="rounded-2xl rounded-tl-sm border border-slate-200 bg-white px-4 py-3 text-sm leading-relaxed shadow-sm">
          {message.text === "" && streaming ? (
            <TypingDots />
          ) : (
            <>
              <Markdown text={message.text} />
              {streaming && (
                <span className="ml-0.5 inline-block h-4 w-1.5 translate-y-0.5 animate-pulse bg-indigo-500" />
              )}
            </>
          )}
        </div>
        {!streaming && message.text && (
          <div className="mt-2 flex flex-wrap items-center gap-2">
            {message.citations && message.citations.length > 0 && (
              <CitationChips citations={message.citations} />
            )}
            {message.metrics && <MetricsBadge metrics={message.metrics} />}
            <CopyButton text={message.text} />
          </div>
        )}
      </div>
    </div>
  );
}

function Avatar() {
  return (
    <div className="h-8 w-8 shrink-0 rounded-full bg-indigo-100 flex items-center justify-center text-sm">
      🛡️
    </div>
  );
}

import type { Message } from "@/types";
import { ReportView } from "@/components/report/ReportView";
import { Markdown } from "./Markdown";
import { TypingDots } from "./TypingDots";
import { CopyButton } from "./CopyButton";
import { MetricsBadge } from "./MetricsBadge";
import { BlockGrid } from "@/components/report/blocks/BlockGrid";
import { AgentSteps } from "./AgentSteps";
import { ApprovalCard } from "./ApprovalCard";

type Props = {
  message: Message;
  onFollowUp: (q: string) => void;
  streaming?: boolean;
  loading?: boolean;
  onRespond?: (
    messageId: string,
    action: "approve" | "edit" | "reject",
    text?: string,
  ) => void;
};

export function Messagebubble({
  message,
  onFollowUp,
  streaming = false,
  loading = false,
  onRespond,
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

  const hasBlocks = !streaming && !!message.blocks?.length;

  return (
    <div className="flex gap-3 dark:prose-invert">
      <Avatar />
      <div
        className={`min-w-0 ${hasBlocks ? "flex-1 max-w-[90%]" : "max-w-[80%]"}`}
      >
        <div className="group/bubble relative rounded-2xl rounded-tl-sm border border-slate-200 bg-white px-4 py-3 pr-10 text-sm leading-relaxed shadow-sm dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100">
          {!streaming && message.text && (
            <div className="absolute right-2 top-2 opacity-100 transition-opacity md:opacity-0 md:group-hover/bubble:opacity-100">
              <CopyButton text={message.text} />
            </div>
          )}
          {message.text === "" && streaming ? (
            <TypingDots />
          ) : (
            <>
              <AgentSteps steps={message.steps ?? []} done={!!message.text} />
              <Markdown text={message.text} citations={message.citations} />
              {streaming && (
                <span className="ml-0.5 inline-block h-4 w-1.5 translate-y-0.5 animate-pulse bg-indigo-500" />
              )}
            </>
          )}
        </div>

        {message.pendingApproval && message.interrupt && onRespond && (
          <ApprovalCard
            draft={message.interrupt.draft}
            disabled={loading}
            onApprove={() => onRespond(message.id, "approve")}
            onReject={() => onRespond(message.id, "reject")}
            onEdit={(text) => onRespond(message.id, "edit", text)}
          />
        )}

        {hasBlocks && (
          <div className="mt-3 w-full animate-in fade-in slide-in-from-bottom-1 duration-300">
            <BlockGrid blocks={message.blocks!} hidePages />
          </div>
        )}

        {!streaming && message.text && !message.pendingApproval && (
          <div className="mt-2 flex flex-wrap items-center gap-2">
            {message.metrics && <MetricsBadge metrics={message.metrics} />}
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

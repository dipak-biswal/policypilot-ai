import { useState } from "react";
import { Button } from "@/components/ui/button";

type Props = {
  draft: string;
  onApprove: () => void;
  onReject: () => void;
  onEdit: (text: string) => void;
  disabled?: boolean;
};

export function ApprovalCard({
  draft,
  onApprove,
  onReject,
  onEdit,
  disabled,
}: Props) {
  const [editing, setEditing] = useState(false);
  const [text, setText] = useState(draft);

  if (editing) {
    return (
      <div className="mt-3 space-y-2 rounded-lg border bg-muted/40 p-3">
        <p className="text-xs font-medium text-muted-foreground">
          Edit the answer
        </p>
        <textarea
          className="min-h-24 w-full rounded-md border bg-background p-2 text-sm"
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <div className="flex gap-2">
          <Button
            size="sm"
            disabled={disabled || !text.trim()}
            onClick={() => onEdit(text)}
          >
            Submit edit
          </Button>
          <Button size="sm" variant="ghost" onClick={() => setEditing(false)}>
            Cancel
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="mt-3 space-y-2 rounded-lg border border-amber-200 bg-amber-50 p-3 dark:border-amber-900 dark:bg-amber-950/40">
      <p className="text-xs font-medium text-amber-800 dark:text-amber-200">
        Waiting for your approval before finishing this answer
      </p>
      <div className="flex flex-wrap gap-2">
        <Button size="sm" disabled={disabled} onClick={onApprove}>
          Approve
        </Button>
        <Button
          size="sm"
          variant="outline"
          disabled={disabled}
          onClick={() => setEditing(true)}
        >
          Edit
        </Button>
        <Button
          size="sm"
          variant="ghost"
          disabled={disabled}
          onClick={onReject}
        >
          Reject
        </Button>
      </div>
    </div>
  );
}

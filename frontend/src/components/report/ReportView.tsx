import type { Report } from "../../types";
import { FollowUpChips } from "./FollowUpChips";
import { ReportSectionView } from "./ReportSectionView";

export function ReportView({
  report,
  onFollowUp,
}: {
  report: Report;
  onFollowUp: (q: string) => void;
}) {
  return (
    <div
      style={{
        border: "1px solid #e2e8f0",
        borderRadius: 12,
        padding: 16,
        background: "white",
        textAlign: "left",
      }}
    >
      <h2 style={{ marginTop: 0 }}>{report.title}</h2>
      <p>{report.summary}</p>
      {report.sections.map((s) => (
        <ReportSectionView key={s.title} section={s} />
      ))}
      <h4>Suggested follow-ups</h4>
      <FollowUpChips
        questions={report.follow_up_questions}
        onPick={onFollowUp}
      />
    </div>
  );
}

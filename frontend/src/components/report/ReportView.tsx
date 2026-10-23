import type { Report } from "../../types";
import { FollowUpChips } from "./FollowUpChips";
import { ReportSectionView } from "./ReportSectionView";

type Props = {
  report: Report;
  onFollowUp: (q: string) => void;
};

export function ReportView({ report, onFollowUp }: Props) {
  return (
    <div className="overflow-hidden rounded-2xl border border-slate-200 dark:bg-slate-900 dark:border-slate-700 shadow-sm">
      <div className="bg-linear-to-r from-indigo-600 to-violet-600 px-5 py-4 text-white">
        <p className="text-[11px] font-semibold uppercase tracking-wider text-indigo-200">
          📊 AI Report
        </p>
        <h2 className="mt-1 text-lg font-bold">{report.title}</h2>
        <p className="mt-1 text-sm leading-relaxed text-indigo-100">
          {report.summary}
        </p>
      </div>

      <div className="grid gap-3 p-4 md:grid-cols-2">
        {report.sections.map((s) => (
          <div
            key={s.title}
            className={s.layout === "table" ? "md:col-span-2" : ""}
          >
            <ReportSectionView section={s} />
          </div>
        ))}
      </div>

      {report.follow_up_questions.length > 0 && (
        <div className="border-t border-slate-200 bg-white px-5 py-4">
          <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-400">
            Suggested follow-ups
          </p>
          <FollowUpChips
            questions={report.follow_up_questions}
            onPick={onFollowUp}
          />
        </div>
      )}
    </div>
  );
}

import type { ReportSection } from "../../types";
import { BulletsSection } from "./BulletsSection";
import { KeyValueSection } from "./KeyValueSection";
import { TableSection } from "./TableSection";

export const ReportSectionView = ({ section }: { section: ReportSection }) => {
  return (
    <section className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <h3 className="mb-3 flex items-center gap-2 text-sm font-semibold text-slate-800">
        <span className="h-4 w-1 rounded-full bg-indigo-500" />
        {section.title}
      </h3>

      <div className="text-sm text-slate-700">
        {section.layout === "bullets" && (
          <BulletsSection bullets={section.bullets} />
        )}
        {section.layout === "table" && section.table && (
          <TableSection table={section.table} />
        )}
        {section.layout === "keyValue" && (
          <KeyValueSection items={section.items} />
        )}
      </div>

      {section.pages.length > 0 && (
        <div className="mt-3 flex flex-wrap gap-1">
          {section.pages.map((p) => (
            <span
              key={p}
              className="rounded-full bg-slate-100 px-2 py-0.5 text-[11px] text-slate-500"
            >
              📄 p.{p}
            </span>
          ))}
        </div>
      )}
    </section>
  );
};

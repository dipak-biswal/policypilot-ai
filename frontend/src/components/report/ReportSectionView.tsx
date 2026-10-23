import type { ReportSection } from "../../types";
import { BulletsSection } from "./BulletsSection";
import { KeyValueSection } from "./KeyValueSection";
import { TableSection } from "./TableSection";

export const ReportSectionView = ({ section }: { section: ReportSection }) => {
  return (
    <section style={{ marginBottom: 16 }}>
      <h3 style={{ marginBottom: 4 }}>{section.title}</h3>
      {section.layout === "bullets" && (
        <BulletsSection bullets={section.bullets} />
      )}
      {section.layout === "table" && section.table && (
        <TableSection table={section.table} />
      )}
      {section.layout === "keyValue" && (
        <KeyValueSection items={section.items} />
      )}
      {section.pages.length > 0 && (
        <small style={{ color: "#64748b" }}>
          Source: pages {section.pages.join(", ")}
        </small>
      )}
    </section>
  );
};

import { Fragment } from "react";
import type { KeyValue } from "../../types";

export const KeyValueSection = ({ items }: { items: KeyValue[] }) => {
  return (
    <dl className="grid grid-cols-[max-content_1fr] divide-y divide-slate-100 rounded-lg border border-slate-200 overflow-hidden">
      {items.map((it) => (
        <Fragment key={it.label}>
          <dt className="bg-slate-50 px-3 py-2 text-xs font-semibold uppercase tracking-wide text-slate-500 border-t border-slate-100 first:border-t-0">
            {it.label}
          </dt>
          <dd className="px-3 py-2 text-slate-800 border-t border-slate-100">
            {it.value}
          </dd>
        </Fragment>
      ))}
    </dl>
  );
};

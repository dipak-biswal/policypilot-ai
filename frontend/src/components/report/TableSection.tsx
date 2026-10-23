import type { TableData } from "../../types";

export const TableSection = ({ table }: { table: TableData }) => {
  return (
    <div className="overflow-x-auto rounded-lg border border-slate-200">
      <table className="w-full text-left text-sm">
        <thead className="bg-slate-100 text-xs uppercase tracking-wide text-slate-500">
          <tr>
            {table.columns.map((c) => (
              <th key={c} className="px-3 py-2 font-semibold">
                {c}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {table.rows.map((row, i) => (
            <tr
              key={i}
              className="odd:bg-white even:bg-slate-50 hover:bg-indigo-50/50"
            >
              {row.map((v, j) => (
                <td
                  key={j}
                  className={`px-3 py-2 ${j === 0 ? "font-medium text-slate-800" : "text-slate-600"}`}
                >
                  {v}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

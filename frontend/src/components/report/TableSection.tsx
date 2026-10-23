import type { TableData } from "../../types";

export const TableSection = ({ table }: { table: TableData }) => {
  return (
    <table style={{ borderCollapse: "collapse", width: "100%" }}>
      <thead>
        <tr>
          {table.columns.map((c) => (
            <th key={c} style={cell}>
              {c}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {table.rows.map((row, i) => (
          <tr key={i}>
            {row.map((v, j) => (
              <td key={j} style={cell}>
                {v}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
};

const cell: React.CSSProperties = {
  border: "1px solid #ddd",
  padding: 8,
  textAlign: "left",
};

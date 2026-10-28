import type { TableBlock } from "@/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { PageBadges } from "./PageBadges";

export function TableBlockView({ block }: { block: TableBlock }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base">{block.title}</CardTitle>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              {block.columns.map((c) => (
                <TableHead key={c}>{c}</TableHead>
              ))}
            </TableRow>
          </TableHeader>
          <TableBody>
            {block.rows.map((r, i) => (
              <TableRow key={i}>
                {r.map((cell, j) => (
                  <TableCell
                    key={j}
                    className={`whitespace-normal ${j === 0 ? "font-medium" : ""}`}
                  >
                    {cell}
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
        <PageBadges pages={block.pages} />
      </CardContent>
    </Card>
  );
}

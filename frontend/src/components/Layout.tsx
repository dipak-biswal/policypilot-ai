import type { ReactNode } from "react";

type Props = { sidebar: ReactNode; children: ReactNode };

export function Layout({ sidebar, children }: Props) {
  return (
    <div className="flex h-screen bg-slate-50 text-slate-800 dark:bg-slate-950 dark:text-slate-100">
      <aside className="w-72 shrink-0 border-r border-slate-200 bg-white p-5 flex flex-col gap-6 dark:bg-slate-900 dark:border-slate-800">
        <div>
          <h1 className="text-xl font-bold text-indigo-600">
            🛡️ PolicyPilot AI
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Cited answers from your policy PDFs
          </p>
        </div>
        {sidebar}
      </aside>
      <main className="flex-1 flex flex-col min-w-0">{children}</main>
    </div>
  );
}

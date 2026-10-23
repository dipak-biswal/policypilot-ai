import { useState, type ReactNode } from "react";

type Props = { sidebar: ReactNode; children: ReactNode };

export function Layout({ sidebar, children }: Props) {
  const [open, setOpen] = useState(false);

  return (
    <div className="flex h-dvh bg-slate-50 text-slate-800 dark:bg-slate-950 dark:text-slate-100">
      {open && (
        <div
          onClick={() => setOpen(false)}
          className="fixed inset-0 z-30 bg-black/40 md:hidden"
        />
      )}

      <aside
        className={`fixed inset-y-0 left-0 z-40 flex w-72 flex-col gap-6 border-r border-slate-200 bg-white p-5 transition-transform dark:border-slate-800 dark:bg-slate-900 md:static md:translate-x-0 ${
          open ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-xl font-bold text-indigo-600 dark:text-indigo-400">
              🛡️ PolicyPilot AI
            </h1>
            <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
              Cited answers from your policy PDFs
            </p>
          </div>
          <button
            onClick={() => setOpen(false)}
            className="text-slate-400 md:hidden"
            aria-label="Close menu"
          >
            ✕
          </button>
        </div>
        <div
          onClick={() => window.innerWidth < 768 && setOpen(false)}
          className="flex min-h-0 flex-col gap-6"
        >
          {sidebar}
        </div>
      </aside>

      <main className="flex min-w-0 flex-1 flex-col">
        <div className="flex items-center gap-3 border-b border-slate-200 bg-white px-4 py-2 md:hidden dark:border-slate-800 dark:bg-slate-900">
          <button
            onClick={() => setOpen(true)}
            className="text-xl"
            aria-label="Open menu"
          >
            ☰
          </button>
          <span className="font-semibold text-indigo-600 dark:text-indigo-400">
            PolicyPilot AI
          </span>
        </div>
        {children}
      </main>
    </div>
  );
}

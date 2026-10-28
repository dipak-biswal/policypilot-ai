import { useState, type ReactNode } from "react";

type Props = {
  sidebar: ReactNode;
  children: ReactNode;
  mobileActions?: ReactNode;
};

export function Layout({ sidebar, children, mobileActions }: Props) {
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
        <footer className="mt-auto border-t border-slate-200 pt-4 text-xs text-slate-400 dark:border-slate-800">
          <p>Built with LangGraph · FastAPI · React</p>
          <a
            href="https://github.com/dipak-biswal/policypilot-ai"
            target="_blank"
            rel="noreferrer"
            className="mt-2 inline-flex items-center gap-1.5 font-medium text-slate-500 hover:text-indigo-600 dark:text-slate-400 dark:hover:text-indigo-400"
          >
            <svg
              viewBox="0 0 24 24"
              className="h-4 w-4"
              fill="currentColor"
              aria-hidden
            >
              <path d="M12 .5a12 12 0 0 0-3.8 23.4c.6.1.8-.3.8-.6v-2.1c-3.3.7-4-1.6-4-1.6-.6-1.4-1.4-1.8-1.4-1.8-1.1-.7.1-.7.1-.7 1.2.1 1.9 1.3 1.9 1.3 1.1 1.8 2.8 1.3 3.5 1 .1-.8.4-1.3.8-1.6-2.7-.3-5.5-1.3-5.5-6 0-1.3.5-2.4 1.2-3.2-.1-.3-.5-1.5.1-3.2 0 0 1-.3 3.3 1.2a11.5 11.5 0 0 1 6 0c2.3-1.5 3.3-1.2 3.3-1.2.7 1.7.2 2.9.1 3.2.8.8 1.2 1.9 1.2 3.2 0 4.6-2.8 5.6-5.5 5.9.4.4.8 1.1.8 2.2v3.3c0 .3.2.7.8.6A12 12 0 0 0 12 .5Z" />
            </svg>
            View source on GitHub
          </a>
        </footer>
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
          <div className="ml-auto flex items-center gap-1">{mobileActions}</div>
        </div>
        {children}
      </main>
    </div>
  );
}

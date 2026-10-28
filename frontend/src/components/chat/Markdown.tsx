import ReactMarkdown from "react-markdown";
import type { Citation } from "@/types";

type Props = { text: string; citations?: Citation[] };

function linkPages(text: string) {
  return text.replace(/\[((?:Page \d+(?:,\s*)?)+)\]/g, (_, inner: string) =>
    inner
      .split(/,\s*/)
      .map((p) => `[${p}](#page-${p.replace(/\D/g, "")})`)
      .join(" "),
  );
}

export function Markdown({ text, citations = [] }: Props) {
  return (
    <ReactMarkdown
      components={{
        a: ({ href, children }) => {
          if (!href?.startsWith("#page-")) return <a href={href}>{children}</a>;
          const page = Number(href.replace("#page-", ""));
          const c = citations.find((x) => Number(x.page) === page);
          return (
            <span className="group/cite relative mx-0.5 inline-flex">
              <span className="cursor-help rounded-full bg-indigo-50 px-2 py-0.5 text-xs font-medium text-indigo-700 hover:bg-indigo-100 dark:bg-indigo-950 dark:text-indigo-300">
                {children}
              </span>
              <span className="pointer-events-none absolute bottom-full left-1/2 z-20 mb-2 hidden w-64 -translate-x-1/2 rounded-lg bg-slate-900 p-2.5 text-xs text-white shadow-lg group-hover/cite:block">
                <span className="block font-semibold">
                  📄 {c?.source ?? "Policy document"}, Page {page}
                </span>
                {c?.snippet && (
                  <span className="mt-1 block opacity-80 line-clamp-4">
                    {c.snippet}
                  </span>
                )}
              </span>
            </span>
          );
        },
      }}
    >
      {linkPages(text)}
    </ReactMarkdown>
  );
}

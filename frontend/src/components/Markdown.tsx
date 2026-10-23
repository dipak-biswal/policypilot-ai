import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
export function Markdown({ text }: { text: string }) {
  return (
    <div className="prose prose-sm prose-slate max-w-none prose-p:my-1.5 prose-ul:my-1.5 prose-li:my-0.5 prose-strong:text-slate-900">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{text}</ReactMarkdown>
    </div>
  );
}

const STARTERS = [
  { icon: "⏳", text: "What are the waiting periods in this policy?" },
  { icon: "🚫", text: "What is not covered under this policy?" },
  { icon: "🏥", text: "How do I make a cashless claim?" },
  { icon: "📊", text: "Generate a summary report of this policy" },
];

export function StarterChips({ onPick }: { onPick: (q: string) => void }) {
  return (
    <div className="mx-auto mt-8 grid max-w-2xl gap-3 sm:grid-cols-2">
      {STARTERS.map((s) => (
        <button
          key={s.text}
          type="button"
          onClick={() => onPick(s.text)}
          className="flex items-start gap-3 rounded-2xl border border-slate-200 bg-white p-4 text-left text-[15px] text-slate-700 shadow-sm transition hover:-translate-y-0.5 hover:border-indigo-300 hover:shadow-md dark:border-slate-700 dark:bg-slate-900 dark:text-slate-300"
        >
          <span className="text-lg">{s.icon}</span>
          <span>{s.text}</span>
        </button>
      ))}
    </div>
  );
}

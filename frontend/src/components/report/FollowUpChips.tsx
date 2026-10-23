type Props = {
  questions: string[];
  onPick: (q: string) => void;
};

export function FollowUpChips({ questions, onPick }: Props) {
  if (questions.length === 0) return null;

  return (
    <div className="flex flex-wrap gap-2">
      {questions.map((q) => (
        <button
          key={q}
          type="button"
          onClick={() => onPick(q)}
          className="group inline-flex items-center gap-1.5 rounded-full border border-indigo-200 bg-indigo-50 px-3 py-1.5 text-left text-xs font-medium text-indigo-700 transition hover:border-indigo-400 hover:bg-indigo-100"
        >
          💡 {q}
          <span className="opacity-0 -translate-x-1 transition group-hover:opacity-100 group-hover:translate-x-0">
            →
          </span>
        </button>
      ))}
    </div>
  );
}

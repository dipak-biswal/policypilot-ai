export const BulletsSection = ({ bullets }: { bullets: string[] }) => {
  return (
    <ul className="flex flex-col gap-2">
      {bullets.map((b, i) => (
        <li key={i} className="flex gap-2 leading-relaxed">
          <span className="mt-0.5 flex h-4 w-4 shrink-0 items-center justify-center rounded-full bg-indigo-100 text-[10px] text-indigo-600">
            ✓
          </span>
          <span>{b}</span>
        </li>
      ))}
    </ul>
  );
};

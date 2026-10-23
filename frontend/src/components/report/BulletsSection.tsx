export const BulletsSection = ({ bullets }: { bullets: string[] }) => {
  return (
    <ul>
      {bullets.map((b, i) => (
        <li key={i}>{b}</li>
      ))}
    </ul>
  );
};

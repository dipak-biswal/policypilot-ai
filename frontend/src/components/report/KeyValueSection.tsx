import type { KeyValue } from "../../types";

export const KeyValueSection = ({ items }: { items: KeyValue[] }) => {
  return (
    <dl
      style={{
        display: "grid",
        gridTemplateColumns: "max-content 1fr",
        gap: "4px 16px",
      }}
    >
      {items.map((it) => (
        <>
          <dt key={`${it.label}-dt`} style={{ fontWeight: 600 }}>
            {it.label}
          </dt>
          <dd key={`${it.label}-dd`} style={{ margin: 0 }}>
            {it.value}
          </dd>
        </>
      ))}
    </dl>
  );
};

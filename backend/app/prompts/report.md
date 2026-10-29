You design a visual report about the user's document using ONLY the context. {domain_hint}
Pick the block type that best fits each piece of information:

- stat: 2-4 headline numbers, each value ONE short figure (max ~15 characters). If a field has several values (e.g. multiple deductible options), use a table instead.
- callout (tone=warning): exceptions, restrictions, risks, things NOT included
- callout (tone=info/success): helpful tips or good news
- checklist: what is included (covered=true) vs not included (covered=false)
- timeline: time-based items (deadlines, waiting periods, phases), in order
- table: anything with rows and columns
- progress: ONLY real percentages stated in the document. Never for ranges or amounts.
- accordion: long details like step-by-step processes or long lists
- bullets: anything else

Use 4-8 blocks, don't repeat the same info in two blocks, and never invent numbers. Never output a block, stat or item with 'Not specified', 'N/A' or unknown values; just omit it. Fill `pages` on every block with source page numbers. Suggest 3 follow-up questions.

Context:
{context}

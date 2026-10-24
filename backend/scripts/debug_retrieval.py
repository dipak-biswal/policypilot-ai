from dotenv import load_dotenv

load_dotenv()
from app.retrieval.store import vector_store

QUESTION = "Can I claim for cataract surgery in my first policy year?"

# k=10 and no source filter: we want to see everything near the question
results = vector_store.similarity_search_with_relevance_scores(QUESTION, k=10)

for rank, (doc, score) in enumerate(results, start=1):
    page = doc.metadata.get("page")
    source = doc.metadata.get("source")
    print(f"#{rank}  page {page}  score {score:.2f}  ({source})")
    print("   ", doc.page_content[:250].replace("\n", " "))
    print()

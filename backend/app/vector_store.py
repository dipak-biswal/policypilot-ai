import os
import hashlib
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_postgres import PGVector
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import warnings

warnings.filterwarnings("ignore", message="Relevance scores must be between 0 and 1")

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


def build_vector_store():
    if os.getenv("VECTOR_BACKEND", "CHROMA") == "pgvector":
        return PGVector(
            embeddings=embeddings,
            collection_name="policies",
            connection=os.environ["DATABASE_URL"],
            use_jsonb=True,
        )
    return Chroma(
        collection_name="policies",
        embedding_function=embeddings,
        persist_directory="./chroma_db",
    )


vector_store = build_vector_store()

splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=250)


def chunk_id(doc: Document) -> str:
    key = f"{doc.metadata['source']}|{doc.metadata['page']}|{doc.page_content}"
    return hashlib.sha256(key.encode()).hexdigest()


def index_pages(filename: str, pages: list[dict]) -> int:
    docs = [
        Document(
            page_content=p["text"], metadata={"source": filename, "page": p["page"]}
        )
        for p in pages
        if p["text"]
    ]

    chunks = splitter.split_documents(docs)
    ids = list(dict.fromkeys(chunk_id(c) for c in chunks))

    unique = {chunk_id(c): c for c in chunks}

    vector_store.add_documents([unique[i] for i in ids], ids=ids)

    return len(chunks)


def search(
    query: str, k: int = 6, min_score: float = 0.2, source: str | None = None
) -> list[Document]:
    kwargs = {"filter": {"source": {"$eq": source}}} if source else {}
    results = vector_store.similarity_search_with_relevance_scores(query, k=k, **kwargs)
    return [doc for doc, score in results if score >= min_score]

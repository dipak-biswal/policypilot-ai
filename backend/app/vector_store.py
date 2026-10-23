from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import warnings

warnings.filterwarnings("ignore", message="Relevance scores must be between 0 and 1")

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vector_store = Chroma(
    collection_name="policies",
    embedding_function=embeddings,
    persist_directory="./chroma_db",
)

splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)


def index_pages(filename: str, pages: list[dict]) -> int:
    docs = [
        Document(
            page_content=p["text"], metadata={"source": filename, "page": p["page"]}
        )
        for p in pages
        if p["text"]
    ]

    chunks = splitter.split_documents(docs)

    vector_store.add_documents(chunks)

    return len(chunks)


def search(query: str, k: int = 6, min_score: float = 0.2) -> list[Document]:
    results = vector_store.similarity_search_with_relevance_scores(query, k=k)
    return [doc for doc, score in results if score >= min_score]

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vector_store = Chroma(
    collection_name="policies",
    embedding_function=embeddings,
    persist_directory="./chroma_db",
)

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)


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


def search(query: str, k: int = 4) -> list[Document]:
    return vector_store.similarity_search(query, k=k)

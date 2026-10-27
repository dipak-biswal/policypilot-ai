import os
import warnings

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.config import settings

warnings.filterwarnings("ignore", message="Relevance scores must be between 0 and 1")
load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=250)


def build_vector_store():
    if settings.vector_backend == "pgvector":
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

from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.postgres import PostgresSaver
from psycopg_pool import ConnectionPool

from app.core.config import settings


def build_checkpointer():
    if settings.vector_backend != "pgvector" or not settings.database_url:
        return MemorySaver()

    # langchain-postgres uses "postgresql+psycopg://"; plain psycopg wants "postgresql://"
    conn_str = settings.database_url.replace("postgresql+psycopg://", "postgresql://")
    pool = ConnectionPool(conn_str, max_size=5, kwargs={"autocommit": True}, open=True)
    saver = PostgresSaver(pool)
    saver.setup()  # creates the checkpoint tables once; safe to run every start
    return saver

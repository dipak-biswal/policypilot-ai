import json
import uuid
from pathlib import Path

from pydantic import BaseModel

from app.core.config import settings

JSON_PATH = Path("data/users.json")


class User(BaseModel):
    id: str
    email: str
    password_hash: str


def _pg():
    import psycopg

    return psycopg.connect(settings.database_url.replace("+psycopg", ""))


def _init():
    if not settings.database_url:
        return
    with _pg() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMPTZ DEFAULT now()
            )
        """)


_init()


def _load_json() -> dict:
    return json.loads(JSON_PATH.read_text()) if JSON_PATH.exists() else {}


def get_user_by_email(email: str) -> User | None:
    email = email.lower().strip()
    if settings.database_url:
        with _pg() as conn:
            row = conn.execute(
                "SELECT id, email, password_hash FROM users WHERE email = %s", (email,)
            ).fetchone()
        return User(id=row[0], email=row[1], password_hash=row[2]) if row else None
    data = _load_json().get(email)
    return User(**data) if data else None


def create_user(email: str, password_hash: str) -> User:
    user = User(
        id=str(uuid.uuid4()), email=email.lower().strip(), password_hash=password_hash
    )
    if settings.database_url:
        with _pg() as conn:
            conn.execute(
                "INSERT INTO users (id, email, password_hash) VALUES (%s, %s, %s)",
                (user.id, user.email, user.password_hash),
            )
    else:
        data = _load_json()
        data[user.email] = user.model_dump()
        JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
        JSON_PATH.write_text(json.dumps(data, indent=2))
    return user

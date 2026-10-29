import json
from pathlib import Path

from app.core.config import settings
from app.ingestion.profile import GENERIC, DocProfile

JSON_PATH = Path("data/doc_profiles.json")


def _pg():
    import psycopg

    url = settings.database_url.replace("postgresql+psycopg://", "postgresql://")
    return psycopg.connect(url, autocommit=True)


def _init():
    if settings.database_url:
        with _pg() as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS doc_profiles (filename TEXT PRIMARY KEY, profile JSONB NOT NULL)"
            )


def save_profile(filename: str, profile: DocProfile) -> None:
    if settings.database_url:
        with _pg() as conn:
            conn.execute(
                "INSERT INTO doc_profiles (filename, profile) VALUES (%s, %s) "
                "ON CONFLICT (filename) DO UPDATE SET profile = EXCLUDED.profile",
                (filename, profile.model_dump_json()),
            )
    else:
        data = json.loads(JSON_PATH.read_text()) if JSON_PATH.exists() else {}
        data[filename] = profile.model_dump()
        JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
        JSON_PATH.write_text(json.dumps(data, indent=2))


def get_profile(filename: str | None) -> DocProfile:
    if not filename:
        return GENERIC
    if settings.database_url:
        with _pg() as conn:
            row = conn.execute(
                "SELECT profile FROM doc_profiles WHERE filename = %s", (filename,)
            ).fetchone()
        return DocProfile(**row[0]) if row else GENERIC
    data = json.loads(JSON_PATH.read_text()) if JSON_PATH.exists() else {}
    return DocProfile(**data[filename]) if filename in data else GENERIC


def delete_profile(filename: str) -> None:
    if settings.database_url:
        with _pg() as conn:
            conn.execute("DELETE FROM doc_profiles WHERE filename = %s", (filename,))
    elif JSON_PATH.exists():
        data = json.loads(JSON_PATH.read_text())
        data.pop(filename, None)
        JSON_PATH.write_text(json.dumps(data, indent=2))


_init()

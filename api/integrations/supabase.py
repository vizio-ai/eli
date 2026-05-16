import os
from supabase import create_client, Client

_client: Client | None = None

def get_client() -> Client:
    global _client
    if _client is None:
        _client = create_client(
            os.getenv("SUPABASE_URL", ""),
            os.getenv("SUPABASE_SERVICE_ROLE_KEY", ""),
        )
    return _client

def insert(table: str, data: dict | list[dict]):
    return get_client().table(table).insert(data).execute()

def select(table: str, query: dict | None = None):
    q = get_client().table(table).select("*")
    if query:
        for col, val in query.items():
            q = q.eq(col, val)
    return q.execute()

def upsert(table: str, data: dict | list[dict], on_conflict: str = "id"):
    return get_client().table(table).upsert(data, on_conflict=on_conflict).execute()

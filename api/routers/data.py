from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any
from data.cleaner import normalize_api_response
from integrations.supabase import insert, select

router = APIRouter()

class IngestRequest(BaseModel):
    table: str
    payload: Any

class QueryRequest(BaseModel):
    table: str
    filters: dict | None = None

@router.post("/ingest")
def ingest(req: IngestRequest):
    records = normalize_api_response(req.payload)
    if not records:
        return {"inserted": 0}
    result = insert(req.table, records)
    return {"inserted": len(records), "data": result.data}

@router.post("/query")
def query(req: QueryRequest):
    result = select(req.table, req.filters)
    return {"data": result.data}

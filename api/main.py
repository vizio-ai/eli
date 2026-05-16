import re
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from routers import chat, slack, data

app = FastAPI(title="Eli API", description="Eli - Vizio AI Virtual Employee")

ALLOWED_ORIGINS = re.compile(
    r"^(http://localhost:\d+|https://[\w-]+-vizio\.vercel\.app|https://eli-vizio\.vercel\.app)$"
)

@app.middleware("http")
async def cors_middleware(request: Request, call_next):
    origin = request.headers.get("origin", "")
    if request.method == "OPTIONS":
        response = Response(status_code=200)
    else:
        response = await call_next(request)
    if ALLOWED_ORIGINS.match(origin):
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "*"
    return response

app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(slack.router, prefix="/slack", tags=["slack"])
app.include_router(data.router, prefix="/data", tags=["data"])


@app.get("/health")
def health():
    return {"status": "ok", "agent": "Eli"}

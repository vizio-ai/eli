from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import chat, slack, data

app = FastAPI(title="Eli API", description="Eli - Vizio AI Virtual Employee")

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://.*\.vercel\.app|http://localhost:\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(slack.router, prefix="/slack", tags=["slack"])
app.include_router(data.router, prefix="/data", tags=["data"])


@app.get("/health")
def health():
    return {"status": "ok", "agent": "Eli"}

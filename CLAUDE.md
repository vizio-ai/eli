# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Eli is a virtual employee AI agent for Vizio AI. It has a Next.js chat frontend (`web/`) and a FastAPI backend (`api/`) powered by Claude Sonnet 4.6.

## Commands

### Backend (FastAPI)
```bash
cd api
source .venv/bin/activate
uvicorn main:app --reload           # dev server on http://localhost:8000
uvicorn main:app --host 0.0.0.0     # production
```

### Frontend (Next.js)
```bash
cd web
npm run dev     # http://localhost:3000
npm run build
npm run lint
```

## Architecture

```
eli/
├── api/                    # FastAPI backend
│   ├── main.py             # App entry point, CORS, router registration
│   ├── agent/eli.py        # Claude Sonnet 4.6 chat logic + system prompt
│   ├── integrations/
│   │   ├── slack.py        # Slack WebClient — send messages, list users
│   │   └── supabase.py     # Supabase client — insert, select, upsert
│   ├── data/cleaner.py     # pandas-based API payload normalization
│   ├── routers/
│   │   ├── chat.py         # POST /chat/ — talk to Eli (supports streaming)
│   │   ├── slack.py        # POST /slack/send, GET /slack/users
│   │   └── data.py         # POST /data/ingest, POST /data/query
│   └── requirements.txt
└── web/                    # Next.js 16 frontend
    ├── app/page.tsx        # Chat UI (client component)
    └── .env.local          # NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Environment variables

### api/.env
```
ANTHROPIC_API_KEY=
SUPABASE_URL=
SUPABASE_SERVICE_ROLE_KEY=
SLACK_BOT_TOKEN=
SLACK_SIGNING_SECRET=
SLACK_APP_TOKEN=
```

### web/.env.local
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Key conventions

- All AI logic lives in `api/agent/eli.py`. The system prompt defining Eli's persona is there.
- `data/cleaner.py` handles any raw API payload — pass it through `normalize_api_response()` before inserting to Supabase.
- The Supabase and Slack clients are singletons initialized lazily on first use.
- The frontend sends the full message history on every request (stateless backend).
- Next.js frontend follows the same conventions as documented in `web/CLAUDE.md`.

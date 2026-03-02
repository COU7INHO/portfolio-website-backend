# Portfolio Chatbot — Backend

FastAPI backend for the AI chatbot on [tiago-coutinho.com](https://tiago-coutinho.com). Answers questions about Tiago Coutinho using a system prompt built from his biography. Responses are streamed in real time.

## Features

- Streaming responses via SSE
- Rate limiting per IP (5 requests/minute by default)
- Conversation history managed by the frontend — no server-side persistence
- Switchable LLM provider per request (OpenAI or local model)
- System prompt loaded from `app/about-me.md` at startup

## LLM Providers

| Provider | Status | Details |
|----------|--------|---------|
| OpenAI (`gpt-4o-mini`) | ✅ Available | Used by default |
| Local model | 🚧 Not yet implemented | Planned: 1B–3B parameter model self-hosted on Raspberry Pi 5 with RAG |

## API

### `POST /chat`

```json
{
  "messages": [
    { "role": "user", "content": "Who is Tiago?" },
    { "role": "assistant", "content": "Tiago is..." },
    { "role": "user", "content": "What does he work on?" }
  ],
  "provider": "openai"
}
```

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `messages` | array | yes | — | Full conversation history |
| `messages[].role` | string | yes | — | `"user"` or `"assistant"` |
| `messages[].content` | string | yes | — | Message text |
| `provider` | string | no | `"openai"` | `"openai"` or `"local"` |

Returns a `text/event-stream` response with text chunks. Returns `429` when the rate limit is exceeded, with a JSON body indicating when to retry.

### `GET /health`

Returns `{"status": "ok"}`. Used by Docker and Nginx to verify the service is running.

## Running Locally

```bash
cp .env.example .env
# fill in your OpenAI API key

uv run uvicorn app.main:app --reload
```

Or with Docker:

```bash
docker build -t portfolio-chatbot:latest .
docker run -d --name portfolio-chatbot -p 8000:8000 --env-file .env portfolio-chatbot:latest
```

## Configuration

All settings are loaded from a `.env` file. See `.env.example` for the full list.

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | — | OpenAI API key (required) |
| `OPENAI_MODEL` | `gpt-4o-mini` | OpenAI model to use |
| `OPENAI_TEMPERATURE` | `0.5` | Response creativity (0.0–2.0) |
| `OPENAI_MAX_TOKENS` | `500` | Maximum tokens per response |
| `RATE_LIMIT` | `5/minute` | Rate limit per IP |
| `ALLOWED_ORIGINS` | `["https://tiago-coutinho.com"]` | CORS allowed origins |

## Project Structure

```
app/
├── main.py               # FastAPI app, CORS, rate limiting
├── config.py             # Settings and shared instances
├── about-me.md           # System prompt content
├── routers/
│   └── chat.py           # /chat and /health endpoints
├── schemas/
│   └── chat.py           # Request/response models
└── services/
    ├── base.py            # LLMService abstract class
    ├── openai_service.py  # OpenAI implementation
    └── local_service.py   # Local model (not yet implemented)
```


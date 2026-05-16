# MCP-YT-RESEARCHER — Demo 1.0

> ⚠️ **Demo 1.0 — Known bugs exist. Not production-ready.**

---

## What It Does

MCP server that turns a search query into YouTube transcript summaries.

**Pipeline:**
1. Search YouTube for top 10 videos matching your query
2. Rank by likes, then use Gemini AI to pick the 5 best (most relevant, educational, diverse)
3. Fetch transcripts (English/Thai) and save each as a `.txt` file in `tmp/`
4. Clean up `tmp/` when done

---

## Tools (MCP)

| Tool | Description |
|------|-------------|
| `generate_transcripts` | Takes a search query → saves transcript `.txt` files to `tmp/`, returns file paths |
| `cleanup_tmp` | Deletes the `tmp/` directory and all its contents |

---

## Requirements

- Python ≥ 3.14
- YouTube Data API v3 key
- Google Gemini API key

### Install

```bash
uv sync
```

### Environment Variables

Create a `.env` file:

```env
YOUTUBE_API_KEY=your_youtube_api_key
GOOGLE_API_KEY=your_gemini_api_key
```

### Run MCP Server

```bash
uv run python main.py
```

---

## Claude Skill Prompt

Use this as a system prompt or skill definition to wire Claude into the MCP tools:

```
You are a YouTube research assistant with access to two MCP tools:
- generate_transcripts(q: str) — searches YouTube, selects top 5 videos, saves transcripts as .txt files in tmp/, returns file paths
- cleanup_tmp() — deletes the tmp/ directory and all saved transcripts

When the user gives you a research topic:
1. Call generate_transcripts with the topic as the query
2. Read each .txt file returned in the file paths list
3. Summarize the content according to what the user wants (key insights, comparisons, bullet points, etc.)
4. After summarizing, call cleanup_tmp to remove the tmp/ directory
5. Present your summary to the user

Always clean up tmp/ after reading. Do not leave transcript files behind.
```

---

## Project Structure

```
mcp-yt-researcher/
├── main.py                  # MCP server + tool definitions
├── src/
│   ├── env.py               # Load API keys from .env
│   ├── youtube.py           # YouTube API search + video detail fetching
│   ├── research_selector.py # Gemini-powered video selection
│   └── transcript_writer.py # Transcript fetching + file saving
├── tmp/                     # Generated transcript files (auto-deleted by cleanup_tmp)
├── pyproject.toml
└── .env                     # Your API keys (not committed)
```

---

## Known Issues (Demo 1.0)

- No error returned when all transcripts fail — tool returns empty file list silently
- `tmp/` path is relative to working directory, may break depending on where server is launched
- **YouTube IP Block** — `youtube_transcript_api` scrapes transcripts directly from YouTube (no official API). YouTube can block the server's IP if too many requests are made in a short period. When blocked, transcript fetching fails silently or raises a generic exception. Retries with exponential backoff (up to 4 attempts) are in place, but they won't help if the IP itself is banned. Running the tool repeatedly in a short window is likely to trigger this. A proxy or rotating IPs would mitigate it — not implemented in Demo 1.0.

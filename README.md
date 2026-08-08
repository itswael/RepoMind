# RepoMind

RepoMind turns raw meeting transcripts into actionable GitHub issues. It chunks a
transcript, uses an LLM to extract candidate tasks, filters out low-confidence
or malformed ones, and files the survivors as GitHub issues — keeping a human
in the loop for the final review instead of auto-merging AI output into a
project silently.

## Pipeline

```
Transcript
   -> Chunking (chunker.py)
   -> Task Extraction (LLM, task_extractor.py)
   -> Validation (validator.py)
   -> GitHub Issue Creation (issue_creator.py)
```

The full target pipeline (see `documentation/flow.text`) also includes a
classifier, decision extractor, summary generator, and formatter stage;
those are part of the design but not yet implemented in code.

## Current state

This is an early-stage / MVP implementation. What exists today:

- `app/api/meeting.py` — FastAPI endpoints to upload a transcript
  (`POST /upload`) and fetch results (`GET /{meeting_id}`).
- `app/workers/worker.py` — enqueues meeting-processing jobs onto a Redis
  queue via `rq`.
- `app/services/pipeline/processor.py` — orchestrates chunking, extraction,
  validation, and issue creation for a single meeting.
- `app/utils/chunker.py` — splits a transcript into word-count-bounded chunks.
- `app/services/llm/task_extractor.py` — calls an OpenAI model
  (`gpt-4o-mini`) to pull actionable tasks out of a transcript chunk.
- `app/services/llm/validator.py` — drops tasks below a confidence threshold
  or with a too-short description.
- `app/services/github/issue_creator.py` — files each accepted task as a
  GitHub issue via the REST API.

Not yet implemented: transcript/result persistence (`save_to_db` /
`fetch_results` are referenced but not defined), authentication, and the
classifier/decision/summary stages shown in the design doc.

## Tech stack

- Python, [FastAPI](https://fastapi.tiangolo.com/) for the HTTP API
- [Redis](https://redis.io/) + [rq](https://python-rq.org/) for background job processing
- [OpenAI API](https://platform.openai.com/) for task extraction
- GitHub REST API for issue creation

## Setup

Requirements: Python 3.10+, a running Redis instance, an OpenAI API key, and
a GitHub token with `repo` scope.

```bash
pip install fastapi uvicorn redis rq openai requests
export OPENAI_API_KEY=...
export GITHUB_TOKEN=...
```

There is no `requirements.txt`/`pyproject.toml` in the repo yet — the
dependencies above are inferred from the imports in `app/`.

A worker process is needed to consume the Redis queue in addition to the API
server; wire up an `rq worker` pointed at the same Redis connection used in
`app/workers/worker.py`.

## Usage

```bash
curl -X POST http://localhost:8000/upload \
  -H "Content-Type: application/json" \
  -d '{"transcript": "...", "repo": "owner/repo"}'
```

This enqueues the transcript for processing; accepted tasks are filed as
issues on the given `repo`.

## License

MIT — see [LICENSE](LICENSE).

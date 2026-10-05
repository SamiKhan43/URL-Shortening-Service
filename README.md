# URL Shortener API

A REST API built with **FastAPI** that shortens long URLs into short, random codes — and tracks how many times each one has been accessed.

Project brief: [roadmap.sh/projects/url-shortening-service](https://roadmap.sh/projects/url-shortening-service)

## Features

- Shorten a long URL into a random, unique short code
- Retrieve the original URL from a short code
- Update the destination URL for an existing short code
- Delete a short code
- Track and view access statistics for each short code
- No authentication required — anyone can shorten and manage links

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) — Python web framework
- [Uvicorn](https://www.uvicorn.org/) — ASGI server
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM / database toolkit
- [SQLite](https://www.sqlite.org/) — lightweight file-based database

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/url-shortener-api.git
cd url-shortener-api
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the server

```bash
uvicorn main:app --reload
```

### 4. Try it out

Open your browser at:

```
http://127.0.0.1:8000/docs
```

## Endpoints

| Method | Path | Description | Success status |
|---|---|---|---|
| POST | `/shorten` | Create a new short URL | 201 |
| GET | `/shorten/{shortCode}` | Retrieve the original URL (counts as an access) | 200 |
| PUT | `/shorten/{shortCode}` | Update the destination URL | 200 |
| DELETE | `/shorten/{shortCode}` | Delete a short URL | 204 |
| GET | `/shorten/{shortCode}/stats` | View access statistics (does **not** count as an access) | 200 |

All endpoints return a `404` if the given `shortCode` doesn't exist.

### Example: Create a short URL

**Request:** `POST /shorten`

```json
{
  "url": "https://www.example.com/some/long/url"
}
```

**Response (201):**

```json
{
  "id": 1,
  "url": "https://www.example.com/some/long/url",
  "shortCode": "aUZuX7",
  "createdAt": "2026-10-05T09:19:25.022472",
  "updatedAt": "2026-10-05T09:19:25.022472",
  "accessCount": 0
}
```

### Example: Get stats

**Request:** `GET /shorten/aUZuX7/stats`

**Response (200):**

```json
{
  "id": 1,
  "url": "https://www.example.com/some/long/url",
  "shortCode": "aUZuX7",
  "createdAt": "2026-10-05T09:19:25.022472",
  "updatedAt": "2026-10-05T09:19:25.022472",
  "accessCount": 3
}
```

## What I Learned

- Generating random, unique codes with Python's `secrets` module, and checking uniqueness against the database before using one
- The difference between `created_at` and `updated_at`, and only updating the latter when a record changes
- Using specific HTTP status codes deliberately (`201` for created, `204` for deleted with no body) instead of always defaulting to `200`
- A real SQLAlchemy gotcha: after `db.commit()`, an object's fields become "expired" in memory, so returning it directly can produce an empty response unless you call `db.refresh()` first
- Deciding which endpoints should count as a real "access" (the lookup endpoint) versus which shouldn't (the stats endpoint)

## Known Limitations / Possible Next Steps

- No way to look up a short code if you've forgotten it (no "search by original URL" endpoint) — not required by the brief, but a reasonable addition
- No actual browser redirect behavior (e.g. visiting the short URL directly and being sent to the real page) — this was listed as optional in the brief
- No authentication, as intentionally specified by the project brief
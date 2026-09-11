import asyncio
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI(title="Universal Book Finder API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

OPEN_LIBRARY = "https://openlibrary.org"
GUTENBERG = "https://gutendex.com"
INTERNET_ARCHIVE = "https://archive.org"
GOOGLE_BOOKS = "https://www.googleapis.com/books/v1"


async def search_open_library(query: str, client: httpx.AsyncClient) -> list[dict]:
    try:
        resp = await client.get(
            f"{OPEN_LIBRARY}/search.json",
            params={"q": query, "limit": 10, "fields": "key,title,author_name,cover_i,first_publish_year,isbn,subject"},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        results = []
        for doc in data.get("docs", [])[:10]:
            cover_url = None
            if doc.get("cover_i"):
                cover_url = f"https://covers.openlibrary.org/b/id/{doc['cover_i']}-M.jpg"

            tags = []
            subjects = doc.get("subject", [])
            if any("public domain" in s.lower() for s in subjects):
                tags.append("Public Domain")

            results.append({
                "id": f"ol-{doc.get('key', '')}",
                "title": doc.get("title", "Unknown"),
                "author": ", ".join(doc.get("author_name", ["Unknown"])),
                "cover": cover_url,
                "year": doc.get("first_publish_year"),
                "source": "Open Library",
                "link": f"{OPEN_LIBRARY}{doc.get('key', '')}",
                "tags": tags,
                "readable": True,
            })
        return results
    except Exception:
        return []


async def search_gutenberg(query: str, client: httpx.AsyncClient) -> list[dict]:
    try:
        resp = await client.get(
            f"{GUTENBERG}/books",
            params={"search": query},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        results = []
        for book in data.get("results", [])[:10]:
            cover_url = book.get("formats", {}).get("image/jpeg")
            authors = [a.get("name", "Unknown") for a in book.get("authors", [])]

            results.append({
                "id": f"gb-{book.get('id', '')}",
                "title": book.get("title", "Unknown"),
                "author": ", ".join(authors) if authors else "Unknown",
                "cover": cover_url,
                "year": book.get("copyright_year") or book.get("authors", [{}])[0].get("birth_year"),
                "source": "Project Gutenberg",
                "link": book.get("formats", {}).get("text/html") or book.get("formats", {}).get("text/plain"),
                "tags": ["Public Domain", "Free Download"],
                "readable": True,
            })
        return results
    except Exception:
        return []


async def search_internet_archive(query: str, client: httpx.AsyncClient) -> list[dict]:
    try:
        resp = await client.get(
            f"{INTERNET_ARCHIVE}/advancedsearch.php",
            params={
                "q": f'title:({query}) AND mediatype:(texts OR books)',
                "fl[]": "identifier,title,creator,date,description",
                "rows": 10,
                "output": "json",
            },
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        results = []
        for doc in data.get("response", {}).get("docs", [])[:10]:
            identifier = doc.get("identifier", "")
            results.append({
                "id": f"ia-{identifier}",
                "title": doc.get("title", "Unknown"),
                "author": doc.get("creator", "Unknown") if isinstance(doc.get("creator"), str) else ", ".join(doc.get("creator", ["Unknown"])),
                "cover": f"https://archive.org/services/img/{identifier}",
                "year": doc.get("date", "")[:4] if doc.get("date") else None,
                "source": "Internet Archive",
                "link": f"https://archive.org/details/{identifier}",
                "tags": ["Read Online"],
                "readable": True,
            })
        return results
    except Exception:
        return []


async def search_google_books(query: str, client: httpx.AsyncClient) -> list[dict]:
    try:
        resp = await client.get(
            f"{GOOGLE_BOOKS}/volumes",
            params={"q": query, "maxResults": 10},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        results = []
        for item in data.get("items", [])[:10]:
            vi = item.get("volumeInfo", {})
            image_links = vi.get("imageLinks", {})
            cover = image_links.get("thumbnail") or image_links.get("smallThumbnail")
            access = item.get("accessInfo", {})
            tags = []

            if access.get("viewability") == "FULL_PUBLIC_DOMAIN":
                tags.append("Public Domain")
            elif access.get("viewability") == "ALL_PAGES":
                tags.append("Full Preview")
            elif access.get("viewability") == "PARTIAL":
                tags.append("Preview")

            if access.get("pdf", {}).get("isAvailable"):
                tags.append("PDF Available")
            if access.get("epub", {}).get("isAvailable"):
                tags.append("EPUB Available")

            info_link = vi.get("infoLink") or vi.get("canonicalVolumeLink", "")

            results.append({
                "id": f"gbk-{item.get('id', '')}",
                "title": vi.get("title", "Unknown"),
                "author": ", ".join(vi.get("authors", ["Unknown"])),
                "cover": cover,
                "year": vi.get("publishedDate", "")[:4] if vi.get("publishedDate") else None,
                "source": "Google Books",
                "link": info_link,
                "tags": tags,
                "readable": bool(tags),
            })
        return results
    except Exception:
        return []


@app.get("/api/search")
async def search_books(q: str = Query(..., min_length=1)):
    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(
            search_open_library(q, client),
            search_gutenberg(q, client),
            search_internet_archive(q, client),
            search_google_books(q, client),
        )

    all_books = []
    for source_results in results:
        all_books.extend(source_results)

    seen = set()
    deduped = []
    for book in all_books:
        key = book["title"].lower().strip()
        if key not in seen:
            seen.add(key)
            deduped.append(book)

    return {"total": len(deduped), "books": deduped}

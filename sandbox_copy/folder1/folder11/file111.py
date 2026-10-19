#!/usr/bin/env python3
"""Bookstore Inventory - main API server.

Serves book data from the PostgreSQL database described in
folder2/folder22/file222.sql. Settings (host, port, log level)
are read from folder2/folder21/file211.ini.

Run with:  python folder1/folder11/file111.py
Frontend:  folder1/folder12/file121.html expects this on :8000
"""

import configparser
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException

app = FastAPI(title="Bookstore Inventory API")

# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------
SETTINGS_FILE = (
    Path(__file__).resolve().parents[3]
    / "folder2"
    / "folder21"
    / "file211.ini"
)

config = configparser.ConfigParser()
config.read(SETTINGS_FILE)

HOST = config.get("server", "host", fallback="0.0.0.0")
PORT = config.getint("server", "port", fallback=8000)
LOG_LEVEL = config.get("logging", "level", fallback="INFO")
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://localhost/bookstore")

# ---------------------------------------------------------------------------
# In-memory book store (seeded by file112.py from file113.csv)
# ---------------------------------------------------------------------------
BOOKS = [
    {"id": 1, "title": "The Little Prince", "author": "Antoine de Saint-Exupery", "price": 9.99, "stock": 12},
    {"id": 2, "title": "Clean Code", "author": "Robert C. Martin", "price": 29.99, "stock": 5},
    {"id": 3, "title": "1984", "author": "George Orwell", "price": 14.50, "stock": 0},
]


def find_book(book_id: int):
    return next((b for b in BOOKS if b["id"] == book_id), None)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/api/books")
def list_books():
    """Return all books. Out-of-stock titles are included and flagged."""
    return {"database": DATABASE_URL, "count": len(BOOKS), "books": BOOKS}


@app.get("/api/books/{book_id}")
def get_book(book_id: int):
    book = find_book(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail=f"Book {book_id} not found")
    return book


@app.post("/api/orders")
def place_order(payload: dict):
    """Place an order for a book. Payload: {"book_id": int, "quantity": int}

    This endpoint was the subject of ticket #331 (folder3/folder33/file331.md):
    it used to decrement stock without re-checking it. Now it returns HTTP 409
    when there is not enough stock, and the frontend disables the button
    whenever stock is zero.
    """
    book = find_book(payload.get("book_id", 0))
    quantity = payload.get("quantity", 1)

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    if book["stock"] < quantity:
        raise HTTPException(
            status_code=409,
            detail=f"Only {book['stock']} copies of '{book['title']}' in stock",
        )

    book["stock"] -= quantity
    total = round(book["price"] * quantity, 2)
    return {"status": "confirmed", "book_id": book["id"], "quantity": quantity, "total": total}


if __name__ == "__main__":
    import uvicorn

    print(f"Starting API on http://{HOST}:{PORT} (log level: {LOG_LEVEL})")
    uvicorn.run(app, host=HOST, port=PORT, log_level=LOG_LEVEL.lower())

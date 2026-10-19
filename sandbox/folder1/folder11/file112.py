#!/usr/bin/env python3
"""Bookstore Inventory - seed data importer.

Reads the starter book list from folder1/folder11/file113.csv and
populates the local in-memory catalog used by file111.py.

In the real pipeline, this inserts the same rows into the database
defined by folder2/folder22/file222.sql, but the in-memory store is
enough for the demo.

Run with:  python folder1/folder11/file112.py

Safe to run twice: rows are skipped if a book with the same title
already exists. This mirrors the ON CONFLICT clause in file222.sql.
"""

import csv
from pathlib import Path

SEED_FILE = Path(__file__).resolve().parent / "file113.csv"

# Simple stand-in storage; swap for real DB calls when the database is wired up.
books: list[dict] = []


def load_seed_rows(path: Path):
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            yield {
                "title": row["title"].strip(),
                "author": row["author"].strip(),
                "price": float(row["price"]),
                "stock": int(row["stock"]),
            }


def import_books(path: Path) -> tuple[int, int]:
    """Import books from the CSV. Returns (imported, skipped)."""
    imported = 0
    skipped = 0
    existing_titles = {b["title"] for b in books}

    for book in load_seed_rows(path):
        if book["title"] in existing_titles:
            print(f"  skip : {book['title']} (already in catalog)")
            skipped += 1
            continue
        book["id"] = max((b["id"] for b in books), default=0) + 1
        books.append(book)
        existing_titles.add(book["title"])
        print(f"  add  : {book['title']} by {book['author']} (${book['price']:.2f}, {book['stock']} in stock)")
        imported += 1

    return imported, skipped


if __name__ == "__main__":
    print(f"Importing seed data from {SEED_FILE.name} ...")
    imported, skipped = import_books(SEED_FILE)
    print(f"Done. imported={imported} skipped={skipped} total={len(books)}")

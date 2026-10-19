# Setup Guide - Bookstore Inventory App

## 1. Install dependencies

```bash
pip install fastapi uvicorn
```

## 2. Point the app at the database

Copy `folder2/folder22/file221.env.example` to `config.env`
and fill in the database URL.

## 3. Create the database tables

Run the SQL from `folder2/folder22/file222.sql`
against your PostgreSQL instance.

## 4. Start the backend

```bash
python folder1/folder11/file111.py
```

The API listens on http://localhost:8000
(see `folder2/folder21/file211.ini` for the port setting).

## 5. Open the frontend

Open `folder1/folder12/file121.html` in a browser.
It calls the API at `http://localhost:8000/api/books`.

## 6. Import the sample books

Run the import script once:

```bash
python folder1/folder11/file112.py
```

It reads the CSV seed data from `folder1/folder11/file113.csv` and
inserts the 3 starter books.

## 7. Verify the low-stock report

The first report is generated into `folder3/folder32/file321.csv`
using the SQL in `folder2/folder22/file222.sql` and the threshold
from `folder2/folder22/file221.env.example`.

## 8. Check the regression tests

Run once to confirm the order-workflow fix for ticket #331:

```bash
pytest folder1/folder11/file114.py
```

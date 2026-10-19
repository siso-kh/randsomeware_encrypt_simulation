-- Bookstore Inventory - database schema and seed data.
-- Run once against PostgreSQL; matches the in-memory seed used by file111.py.

CREATE TABLE IF NOT EXISTS books (
    id      SERIAL PRIMARY KEY,
    title   VARCHAR(200) NOT NULL UNIQUE,
    author  VARCHAR(200) NOT NULL,
    price   NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
    stock   INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0)
);

CREATE TABLE IF NOT EXISTS orders (
    id         SERIAL PRIMARY KEY,
    book_id    INTEGER NOT NULL REFERENCES books(id),
    quantity   INTEGER NOT NULL CHECK (quantity > 0),
    total      NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Index for the low-stock report (folder3/folder32/file321.csv)
CREATE INDEX IF NOT EXISTS idx_books_stock ON books (stock);

-- Seed data (same 3 books as folder1/folder11/file113.csv)
INSERT INTO books (title, author, price, stock) VALUES
    ('The Little Prince', 'Antoine de Saint-Exupery', 9.99, 12),
    ('Clean Code',        'Robert C. Martin',        29.99, 5),
    ('1984',              'George Orwell',           14.50, 0)
ON CONFLICT (title) DO NOTHING;

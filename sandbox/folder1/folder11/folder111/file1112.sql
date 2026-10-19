-- Ad-hoc query: pick titles for the September "buy 2 get 1" promotion.
-- Keeps only in-stock books priced under $20 (matches the report rules
-- in folder3/folder32/file321.csv).

SELECT title, author, price, stock
FROM books
WHERE stock > 0
  AND price < 20.00
ORDER BY price ASC;

-- September 2026 result on seed data (folder1/folder11/file113.csv):
--   The Little Prince | Antoine de Saint-Exupery |  9.99 | 12
--   1984              | George Orwell           | 14.50 |  0  (excluded: out of stock)

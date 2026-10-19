# Spec - Low-Stock Restock Alerts

**Status:** shipped in the weekly report (`folder3/folder32/file321.csv`)
**Author:** bookstore dev team

## Problem
Staff noticed "1984" was out of stock for days before anyone ordered new
copies (see ticket `folder3/folder33/file331.md`).

## Proposed behavior
1. Every Monday, generate a report of all books whose `stock` is below
   `LOW_STOCK_THRESHOLD` (default 5, set in `folder2/folder22/file221.env.example`).
2. Flag out-of-stock titles in a separate column.
3. Email the report to `SUPPORT_EMAIL`.

## Data source
```sql
SELECT title, stock FROM books WHERE stock < :threshold ORDER BY stock ASC;
```
The `idx_books_stock` index in `folder2/folder22/file222.sql` keeps this fast.

## Out of scope
- Automatic purchase orders (deferred).
- Real-time alerts (report is weekly on purpose).

# Ticket #331 - Customer could order an out-of-stock book

**Reported:** 2026-09-05, by Dana (front desk)
**Severity:** high
**Status:** closed (fixed)

## What happened
A customer ordered "1984" through the storefront page. The order was
confirmed, but the book had 0 copies in stock.

## Steps to reproduce
1. Open the storefront (`folder1/folder12/file121.html`).
2. Click **Order** on a title showing "Out of stock".

## Root cause
The frontend button was not disabled for zero-stock titles, and the API
`/api/orders` route (`folder1/folder11/file111.py`) did not re-check stock
before decrementing it.

## Fix
- Frontend: `file122.js` now renders a disabled "Unavailable" button when
  `stock === 0`.
- Backend: `/api/orders` returns HTTP 409 when `stock < quantity`.
- Tests: regression test `test_out_of_stock` added in
  `folder1/folder11/file114.py`.

## Follow-up
The recurring out-of-stock problem led to the low-stock report
(`folder3/folder31/file311.md`).

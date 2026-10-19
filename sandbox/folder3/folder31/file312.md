# Meeting Notes - Weekly Sync (Sept 7, 2026)

**Attendees:** Dana (owner), Miguel (backend), Priya (frontend)

## Decisions
- Keep the API on port 8000 for now (`folder2/folder21/file211.ini`);
  revisit only if we add a second service.
- Ship the low-stock report before adding new features. Spec lives in
  `folder3/folder31/file311.md`.
- Frontend stays plain JS (`folder1/folder12/file122.js`) - no framework
  needed for a 3-book catalog.

## Action items
| Who   | What                                                        | Done |
|-------|-------------------------------------------------------------|------|
| Miguel| Add `idx_books_stock` index (file222.sql)                    | yes  |
| Priya | Disable the Order button when stock is 0 (file122.js)        | yes  |
| Dana  | Confirm restock supplier for "1984"                          | open |

## Next week
Review the first generated report in `folder3/folder32/` and decide
whether the threshold of 5 is right for slow-moving titles.

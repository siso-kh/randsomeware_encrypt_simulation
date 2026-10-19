# folder1 - Application Source Code

Contains the backend and frontend code for the Bookstore Inventory app.

## Contents
- `folder11/` - Python backend (API server, import script, tests)
- `folder12/` - Frontend (HTML page, JS logic, CSS)

## Entry points
- API server:  `folder11/file111.py`
- Data import: `folder11/file112.py`  (reads `folder11/file113.csv`)
- Web page:    `folder12/file121.html` (calls the API at :8000)

## Related configs
- `folder2/folder21/file211.ini` - server port and log level the backend reads
- `folder2/folder22/file221.env.example` - env vars including DATABASE_URL

## Related docs
- Ticket #331 is described in `../folder3/folder33/file331.md`.
- The frontend UI strings live in `folder12/folder121/file1121.json`.

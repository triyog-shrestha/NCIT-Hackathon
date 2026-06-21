# Mindspace — React frontend

A standalone React (Vite) frontend for the chat app, talking to the existing
Flask API in `main.py` — no backend changes required.

## Running it

You need two things running side by side:

**1. The Flask API (unchanged, from your existing files)**

```bash
python main.py
# -> http://0.0.0.0:5000
```

**2. This frontend**

```bash
cd frontend
npm install
npm run dev
# -> http://localhost:5173
```

The dev server proxies any `/api/*` request straight to `http://127.0.0.1:5000`
(see `vite.config.js`), so the browser talks to `localhost:5173` and never
needs to know the Flask port directly. If your Flask app runs somewhere else,
set `VITE_API_TARGET` before starting Vite:

```bash
VITE_API_TARGET=http://127.0.0.1:8000 npm run dev
```

## What's here

- `src/App.jsx` — top-level router: character grid vs. chat screen.
- `src/components/CharacterGrid.jsx` — the card grid, fetches `/api/characters`.
- `src/components/ChatScreen.jsx` — chat UI, posts to `/api/chat`.
- `src/api.js` — the only file that talks to the network.
- `src/characterArt.js` — local lookup for character images/avatars/taglines.
  `main.py`'s `/api/characters` doesn't currently expose those fields from
  `characters.py` (it derives a generated `color` and a tagline cut from the
  prompt instead), so this fills the gap without touching the backend. If you
  add a character on the backend, add a matching entry here or it'll fall
  back to a plain initial-letter avatar — not broken, just less custom.

## Things worth knowing

- **No conversation persistence in the browser.** Refreshing the page clears
  the visible chat log, same as a fresh Streamlit session would. The actual
  conversation history Ollama sees still lives server-side in
  `_chat_sessions` in `main.py` for the life of the process — so if you
  refresh and keep chatting, the model still has memory of earlier turns even
  though the UI doesn't show them. If that mismatch bothers you, the cleanest
  fix is exposing a `/api/reset` endpoint that calls `character.reset()`.
- **The AI disclosure line in the chat header is intentional** — it's there
  so it's not just a one-time disclaimer buried in a modal. I'd leave it in
  even as this evolves; it costs nothing and matters for any companion-style
  product, including a personal one.
- **No fake typing delay.** The "thinking" dots show for as long as the
  request is actually in flight — they're not an artificial delay designed
  to build anticipation.
- Production color, type, and spacing tokens live in `src/index.css` — change
  `--accent` etc. there to retheme without touching component files.

## Not included (by design, for this pass)

- Admin/sentiment dashboard (still just `admin.py` via Streamlit — totally
  fine to leave as-is, it's an internal tool, not the user-facing surface).
- Auth / age gating — reasonable to skip for a personal project with no real
  users, but worth adding before anyone besides you uses this.

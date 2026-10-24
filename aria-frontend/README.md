# ARIA Frontend

Frontend for ARIA, a Physical AI Lab Assistant. Plain HTML, CSS and JavaScript. No build step.

## Structure

```
index.html            markup
main.html             all-in-one copy (HTML + CSS + JS inline)
css/style.css         tokens, layout, responsive rules
js/api.js             DOCS, CHUNKS and ask(): the only backend seam
js/script.js          UI, chat, sidebar, voice overlay
assets/logo/          aria-mark.svg, favicon.svg
assets/fonts/         optional self-hosted fonts
docs/api-contract.md  ask() request and response shape
.github/workflows/    GitHub Pages deploy
```

## Run

Open `index.html` in a browser, or serve the folder: `python3 -m http.server 8000`.

## Connect the backend

Edit `ask(query)` in `js/api.js`. Keep the return shape in `docs/api-contract.md`. Never put API keys in these files.

## Edit guide

- Colors and fonts: `:root` in `css/style.css`
- Starter prompts: `<ul class="start">` in `index.html`
- Document titles and chunk count: `DOCS`, `CHUNKS` in `js/api.js`
- Voice language: `rec.lang` in `js/script.js`

After editing, regenerate `main.html` if you keep it, or delete it.

# POLIS Documentation Website

A bilingual **Brazilian Portuguese and English** documentation website for
[POLIS](https://github.com/MarcosAlves90/polis), retaining the project's nautical visual identity.
This site is maintained independently of the POLIS CLI and does not define or change its protocol contracts.

## Technology stack

- Semantic HTML, CSS, and vanilla JavaScript; no client-side framework, application API, or server runtime.
- Python 3.10+, Jinja2, and markdown-it-py to generate static pages from Markdown.
- Separate local search indexes for each language, keyboard support, theme switching, clean URLs, and responsive layouts.
- Self-hosted variable Inter fonts (WOFF2, Latin and Latin Extended, upright and italic) under the
  SIL Open Font License in `assets/fonts/LICENSE.txt`. Local fallbacks remain available on Android, iOS, and desktop.
- Static output in `dist/`, suitable for GitHub Pages, Cloudflare Pages, Netlify, Vercel, or conventional HTTP servers.

## Run locally

```bash
cd polis-site
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python build.py
python -m http.server 8000 --directory dist
```

On Windows PowerShell, activate `.venv\Scripts\Activate.ps1` before running the `python` commands.

- **PT-BR:** `http://localhost:8000/`
- **English:** `http://localhost:8000/en/`
- **PT-BR docs:** `/docs/visao-geral/`
- **English docs:** `/en/docs/overview/`

The header always displays **PT | EN** on both languages, including mobile. The active language is highlighted and both links point to the equivalent translated document, not the language home page. Each language has its own search index (`/search.json` and `/en/search.json`). Portuguese URLs remain unchanged from the previous site version.

## Maintain translations

Each article has two Markdown files with **the same filename**:

```text
content/visao-geral.md           # Portuguese
content/en/visao-geral.md        # English; slug: overview
```

Frontmatter example:

```yaml
---
slug: overview
title: Overview
description: What POLIS is and why it exists.
group: Comece aqui
order: 1
source: README.md
---
```

- `title`, `description`, `group` and `order` are required. `source` defaults to `README.md` and `slug` defaults to the filename; `slug` controls the localized URL. Use the same **group ID** across both languages; translated group labels live in `i18n.py`.
- When adding a page, create both language files with matching filenames. The build rejects missing counterparts or duplicate URL slugs, preventing broken language switches.
- Write internal links in the language of the target page, for example English `../installation/` rather than `../instalacao/`.
- `build.py` generates navigation, adjacent-page links, headings, search indexes, page URLs and language counterparts.
- `i18n.py` holds interface and navigation translations; `templates/home.html` and `templates/home_en.html` hold localized landing-page copy. Shared header and docs templates are `base.html` and `doc.html`.
- `assets/styles.css` contains structural styling, while `assets/nautical.css` contains the image-inspired palette and decorations, including the always-visible PT/EN control. `assets/app.js` handles theme, search, copy-to-clipboard, keyboard shortcuts, and responsive navigation.
- `assets/og-cover-pt.png` and `assets/og-cover-en.png` are localized 1200 × 630 social preview images based on the official POLIS cover; to regenerate them after changing `assets/cover-art.webp`, run `python tools/render_og.py` (requires Pillow).

The command examples, schemas, and normative terminology of the POLIS CLI remain as documented in the V6 source. Changes to machine-level semantics must come from the POLIS Specification, not from this explanatory website.

## Static build and hosting

Root domain:

```bash
python build.py --site-url https://docs.example.com
```

Subdirectory, e.g. GitHub Pages:

```bash
python build.py --base-path /polis-site/ --site-url https://username.github.io
```

The `--site-url` option enables canonical URLs, `hreflang` alternate-language metadata, a bilingual `sitemap.xml`, and absolute Open Graph/Twitter image URLs required by social crawlers. Always set the real production HTTPS origin when deploying (the example URL is not a configured domain). The source has no fixed production domain. Publish only the `dist/` directory. No remote publication or hosting setup is performed by the build.

The two language paths are rooted at the selected `--base-path`: e.g., `/polis-site/` and `/polis-site/en/`. On a static host, ensure directory `index.html` support is enabled.

### Vercel (static output)

Connect this repository to Vercel with **Root Directory** set to the repository root. The tracked `vercel.json` sets **Framework Preset: Other**, creates `.venv` with `uv`, installs `requirements.txt` into that environment, runs `.venv/bin/python build.py`, publishes **Output Directory: `dist`**, and preserves trailing slashes for routes such as `/docs/visao-geral/` and `/en/docs/overview/`. Vercel serves the generated HTML, CSS, JavaScript, images and search indexes directly; no Python server or function entrypoint is needed.

Do not select the **Python**, **Flask**, or **FastAPI** framework presets. They expect a Python HTTP handler, whereas `build.py` is a generator only. The `vercel.json` overrides the framework and build settings stored in the Vercel dashboard; ensure the Vercel project points at this repository's root and builds the `main` branch. The previous global `python3 -m pip install` failed on Vercel with PEP 668 `externally-managed-environment`: its Python interpreter is managed by `uv`. Installing packages into `.venv` prevents that failure without overriding the managed interpreter. Both `dist/` and `.venv/` are intentionally untracked. To verify the same Vercel steps locally (requires `uv`), run from the repository root:

```bash
uv venv .venv && uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python build.py
.venv/bin/python -m unittest discover -s tests -v
```

On repeat local runs, skip `uv venv .venv` if the environment already exists, or use
`uv venv --allow-existing .venv` to preserve it.

If a canonical production domain is configured, `.venv/bin/python build.py --site-url https://your-domain.example` adds the sitemap, canonical/hreflang tags and absolute social image URLs. The default Vercel build command leaves the canonical origin unset because this repository does not prescribe a production domain; set an appropriate build command in `vercel.json` when the domain is known.

## Validate

```bash
python -m unittest discover -s tests -v
python build.py
node --check assets/app.js  # optional: requires Node.js
```

Tests check both document sets, page links, Markdown HTML safety, navigation, language counterparts, two search indexes, per-language metadata, source links, and subdirectory deployment. Review visual behavior in a browser before deployment.

GitHub Actions reproduces the isolated `uv` installation and Python build used by Vercel, runs the Python tests and checks JavaScript syntax on pushes and pull requests. The generated `dist/` directory is excluded from Git; rebuild it from the tracked sources when publishing the site.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for English-language documentation and metadata conventions, how to
maintain both localized versions of a page, and the required Conventional Commits and pull request format.
GitHub Actions checks new commit subjects and pull request titles and descriptions. The optional local
commit-message hook applies the same subject check before a commit is created.

## Security, accessibility, and visual design

- HTML semantic structure, skip links, keyboard focus, `/` or `Ctrl/Cmd+K` for search, Esc to close, remembered light/dark theme, and reduced-motion styles.
- Search works when the static files are served over HTTP; opening the files using `file://` may block `fetch` of the local search index.
- No remote search provider, analytics dependency, user accounts, database, or third-party hosted fonts are required.
- The original nautical cover is optimized as `assets/cover-art.webp`, used as a subtle decorative hero/background element and as the source of the localized OG images. The colors draw on deep ocean blue, stone, brass, and lighthouse teal.

**Sources:** POLIS V6 README, `docs/quickstart.md`, `docs/commands.md`,
`docs/workflows/local-agent-workspace.md`, `docs/workflows/web-agent-delivery.md`,
`docs/gates-and-progress.md`, `docs/policy-and-validation.md`, `docs/retention.md`,
`docs/installation.md`, `spec/POLIS-SPEC-v6.md`, and
`spec/POLIS-OFFLINE.md`. The official [V6 Specification](https://github.com/MarcosAlves90/polis/blob/main/spec/POLIS-SPEC-v6.md)
is authoritative whenever this website and the normative specification differ. The POLIS repository was
rechecked against POLIS `v6.12.0` (`origin/main` at `12a2f71`) on October 18, 2026.

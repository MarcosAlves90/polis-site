# POLIS Website — Documentação V6 / V6 Documentation

Site principal e documentação navegável em **português brasileiro e inglês** para o [POLIS](https://github.com/MarcosAlves90/polis). Mantém a identidade visual náutica do projeto. Independente do repositório da CLI, sem modificar seus contratos.

A bilingual **Portuguese (Brazil) and English** POLIS documentation site, with the original nautical visual identity. Its implementation is independent of the CLI repository and does not modify POLIS protocol contracts.

## Tecnologias / Stack

- HTML semântico, CSS e JavaScript nativo: sem framework de cliente, API ou infraestrutura de aplicação.
- Python 3.10+, Jinja2 e markdown-it-py: gera páginas estáticas a partir de Markdown.
- Dois índices de busca locais, suporte a teclado, alternância de temas, rotas amigáveis e layout responsivo.
- Saída em `dist/`: compatível com GitHub Pages, Cloudflare Pages, Netlify, Vercel (modo estático) e servidores HTTP convencionais.

## Executar / Run locally

```bash
cd polis-site
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python build.py
python -m http.server 8000 --directory dist
```

No Windows PowerShell, ative com `.venv\Scripts\Activate.ps1` antes de executar os comandos `python`. / On Windows PowerShell activate `.venv\Scripts\Activate.ps1` first.

- **PT-BR:** `http://localhost:8000/`
- **English:** `http://localhost:8000/en/`
- **PT-BR docs:** `/docs/visao-geral/`
- **English docs:** `/en/docs/overview/`

The header always displays **PT | EN** on both languages, including mobile. The active language is highlighted and both links point to the equivalent translated document, not the language home page. Each language has its own search index (`/search.json` and `/en/search.json`). Portuguese URLs remain unchanged from the previous site version.

## Editar documentação / Maintaining translations

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

## Publicar / Static build and hosting

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

## Verificar / Validate

```bash
python -m unittest discover -s tests -v
python build.py
node --check assets/app.js  # optional: requires Node.js
```

Tests check both document sets, page links, Markdown HTML safety, navigation, language counterparts, two search indexes, per-language metadata, source links, and subdirectory deployment. Review visual behavior in a browser before deployment.

GitHub Actions runs the Python tests, static build, and JavaScript syntax check on pushes and pull requests. The generated `dist/` directory is excluded from Git; rebuild it from the tracked sources when publishing the site.

## Segurança, UX e identidade visual / Security and design

- HTML semantic structure, skip links, keyboard focus, `/` or `Ctrl/Cmd+K` for search, Esc to close, remembered light/dark theme, and reduced-motion styles.
- Search works when the static files are served over HTTP; opening the files using `file://` may block `fetch` of the local search index.
- No remote search provider, analytics dependency, user accounts, database, or third-party hosted fonts are required.
- The original nautical cover is optimized as `assets/cover-art.webp`, used as a subtle decorative hero/background element and as the source of the localized OG images. The colors draw on deep ocean blue, stone, brass, and lighthouse teal.

**Fonte / Source:** POLIS V6 README, `docs/usage.md`, `docs/installation.md`, `spec/POLIS-SPEC-v6.md`, `spec/POLIS-OFFLINE.md`. The official [V6 Specification](https://github.com/MarcosAlves90/polis/blob/main/spec/POLIS-SPEC-v6.md) is authoritative whenever this website and the normative specification differ. The POLIS repository was consulted for the original site on October 12, 2026.

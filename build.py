#!/usr/bin/env python3
"""POLIS site generator: Markdown in, static HTML out. No server required."""
import argparse
import html
import json
import re
import shutil
import unicodedata
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

from jinja2 import Environment, FileSystemLoader, select_autoescape
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parent
from i18n import GROUPS, GROUP_LABELS, UI

REPO = "https://github.com/MarcosAlves90/polis"


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"Missing frontmatter: {path}")
    _, meta, body = text.split("---", 2)
    fields = {}
    for line in meta.strip().splitlines():
        if line.strip():
            k, sep, v = line.partition(":")
            if not sep:
                raise ValueError(f"Invalid frontmatter {path}: {line}")
            fields[k.strip()] = v.strip().strip('"')
    for required in ("title", "description", "group", "order"):
        if not fields.get(required):
            raise ValueError(f"Missing {required}: {path}")
    if fields["group"] not in GROUPS:
        raise ValueError(f"Unknown group: {path}")
    fields["id"] = path.stem
    fields["slug"] = fields.get("slug", path.stem)
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", fields["slug"]):
        raise ValueError(f"Invalid slug in {path}")
    fields["order"] = int(fields["order"])
    fields["body"] = body.strip()
    fields["source"] = fields.get("source", "README.md")
    return fields


def slugify(text):
    value = unicodedata.normalize("NFKD", text)
    value = "".join(c for c in value if not unicodedata.combining(c))
    value = re.sub(r"[^\w\s-]", "", value.lower(), flags=re.UNICODE)
    return re.sub(r"[-\s]+", "-", value).strip("-") or "secao"


def markdown_renderer(body, lang="pt"):
    md = MarkdownIt("default", {"html": False, "linkify": False}).enable("table").enable("strikethrough")
    toc, seen = [], {}
    tokens = md.parse(body)
    for i, tok in enumerate(tokens):
        if tok.type != "heading_open":
            continue
        inline = tokens[i+1]
        plain = "".join(t.content for t in inline.children if t.type in ("text", "code_inline")) or inline.content
        anchor = slugify(plain)
        n = seen.get(anchor, 0)
        seen[anchor] = n + 1
        if n:
            anchor = f"{anchor}-{n+1}"
        tok.attrSet("id", anchor)
        if tok.tag in ("h2", "h3"):
            toc.append({"id":anchor, "title":plain, "depth":int(tok.tag[1])})
    def fence(tokens, idx, options, env):
        tok=tokens[idx]; language = re.sub(r"[^a-zA-Z0-9#+._-]", "", tok.info.strip().split()[0]) if tok.info.strip() else "text"
        return (f'<div class="code-block"><div class="code-top"><span class="code-lang">{html.escape(language)}</span>'
                f'<button class="code-copy" type="button" aria-label="{html.escape(UI[lang]['copy'])}" data-copy-code><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="15" height="15" aria-hidden="true"><rect x="8" y="8" width="12" height="12" rx="2"/><path d="M16 8V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h2"/></svg><span>{html.escape(UI[lang]['copy'])}</span></button></div>'
                f'<pre><code class="language-{language}">{html.escape(tok.content)}</code></pre></div>')
    md.renderer.rules["fence"] = fence
    result = md.renderer.render(tokens, md.options, {})
    # Give heading deep links visual affordances, no JavaScript required.
    result = re.sub(r'<(h[23]) id="([^"]+)">', lambda match: f'<{match.group(1)} id="{match.group(2)}"><a class="heading-link" href="#{match.group(2)}" aria-label="{html.escape(UI[lang]["permalink"])}">#</a>', result)
    return result, toc


def build(base="/", url=""):
    if not re.fullmatch(r"/[a-zA-Z0-9_-]+(?:/[a-zA-Z0-9_-]+)*/?|/", base if base.startswith("/") else "/" + base):
        raise ValueError("--base-path must be a simple absolute path")
    base = "/" + base.strip("/") + "/" if base.strip("/") else "/"
    parsed = urlsplit(url)
    if url and (parsed.scheme != "https" or not parsed.netloc or parsed.path not in ("", "/") or parsed.query or parsed.fragment or parsed.username or parsed.password):
        raise ValueError("--site-url must be an HTTPS origin without path, query, or credentials")
    content_dir = ROOT / "content"
    content = {
        "pt": [frontmatter(p) for p in content_dir.glob("*.md")],
        "en": [frontmatter(p) for p in (content_dir / "en").glob("*.md")],
    }
    for lang in content:
        pages = content[lang]
        pages.sort(key=lambda p: (GROUPS.index(p["group"]), p["order"], p["slug"]))
        if len({p["slug"] for p in pages}) != len(pages):
            raise ValueError(f"Duplicate {lang} slugs")
    ids = {lang: {p["id"] for p in content[lang]} for lang in content}
    if ids["pt"] != ids["en"]:
        raise ValueError(f"Missing language counterparts: {ids['pt'] ^ ids['en']}")
    by_id = {lang: {p["id"]: p for p in content[lang]} for lang in content}
    for lang in content:
        for p in content[lang]:
            prefix = base + ("en/" if lang == "en" else "")
            p["href"] = prefix + "docs/" + p["slug"] + "/"
    # Finish alternate hrefs after all language routes have been computed.
    for lang in content:
        for p in content[lang]:
            p["other_href"] = by_id["pt" if lang == "en" else "en"][p["id"]]["href"]
    env = Environment(loader=FileSystemLoader(ROOT / "templates"), autoescape=select_autoescape(["html"]))
    dist = ROOT / "dist"
    if dist.exists():
        shutil.rmtree(dist)
    dist.mkdir()
    shutil.copytree(ROOT / "assets", dist / "assets")
    (dist / ".nojekyll").write_text("", encoding="utf-8")
    site_url = url.rstrip("/")
    for lang, pages in content.items():
        lang_prefix = base + ("en/" if lang == "en" else "")
        locale_root = dist / ("en" if lang == "en" else "")
        locale_root.mkdir(parents=True, exist_ok=True)
        def doc_href(page_id):
            return by_id[lang][page_id]["href"]
        ctx = dict(base=base, site_url=site_url, repo=REPO, groups=GROUPS,
                   labels=GROUP_LABELS[lang], ui=UI[lang], pages=pages, lang=lang,
                   lang_home=lang_prefix, doc_href=doc_href,
                   locale_pt_href=base, locale_en_href=base+"en/",
                   current_year=date.today().year)
        home = env.get_template("home_en.html" if lang == "en" else "home.html").render(
            **ctx, page_title=("POLIS — Verifiable software delivery" if lang == "en" else "POLIS — Entregas de software verificáveis"),
            page_description=("POLIS V6: evidence-driven validation, verifiable delivery artifacts, and controlled application of code changes." if lang == "en" else "POLIS V6: validação baseada em evidências, artefatos verificáveis e aplicação controlada de mudanças de código."),
            canonical=site_url+lang_prefix if url else "", alternate=site_url + (base if lang == "en" else base+"en/") if url else "", is_home=True)
        (locale_root / "index.html").write_text(home, encoding="utf-8")
        search = []
        for i, p in enumerate(pages):
            p["html"], p["toc"] = markdown_renderer(p["body"], lang)
            p["previous"] = pages[i-1] if i else None
            p["next"] = pages[i+1] if i < len(pages)-1 else None
            search.append({"title":p["title"], "description":p["description"],
                           "group":GROUP_LABELS[lang][p["group"]], "url":p["href"],
                           "text":re.sub(r"\s+", " ", re.sub(r"[`*_>#|\[\]()]", " ", p["body"]))[:7000]})
        for p in pages:
            target = locale_root / "docs" / p["slug"]
            target.mkdir(parents=True, exist_ok=True)
            markup = env.get_template("doc.html").render(**{**ctx,
                "locale_pt_href": p["href"] if lang == "pt" else p["other_href"],
                "locale_en_href": p["href"] if lang == "en" else p["other_href"]}, page=p,
                page_title=p["title"]+" — POLIS", page_description=p["description"],
                canonical=site_url+p["href"] if url else "", alternate=site_url+p["other_href"] if url else "", is_home=False)
            (target / "index.html").write_text(markup, encoding="utf-8")
        (locale_root / "search.json").write_text(json.dumps(search, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        (locale_root / "docs").mkdir(exist_ok=True)
        dest = by_id[lang]["visao-geral"]["href"]
        (locale_root / "docs" / "index.html").write_text(
            '<!doctype html><html lang="'+('en' if lang == 'en' else 'pt-BR')+'"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url='+dest+'"><link rel="canonical" href="'+dest+'"></head><body><a href="'+dest+'">'+UI[lang]["docs"]+'</a></body></html>', encoding="utf-8")
        (locale_root / "404.html").write_text(env.get_template("404.html").render(
            **ctx, page_title=("Page not found — POLIS" if lang == "en" else "Página não encontrada — POLIS"),
            page_description=("Page not found." if lang == "en" else "Página não encontrada."), canonical="", alternate="", is_home=False), encoding="utf-8")
    (dist / "robots.txt").write_text("User-agent: *\nAllow: /\n" + ("Sitemap: "+site_url+base+"sitemap.xml\n" if url else ""), encoding="utf-8")
    if url:
        urls = [base, base+"en/"] + [p["href"] for pages in content.values() for p in pages]
        sitemap = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+html.escape(site_url+x)+'</loc></url>' for x in urls)+'</urlset>'
        (dist / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    print(f"Built {sum(map(len,content.values()))} documents in 2 languages; output: {dist}; base: {base}")


if __name__=="__main__":
    parser=argparse.ArgumentParser(description="Build POLIS static site")
    parser.add_argument("--base-path",default="/",help="Deployment path prefix, e.g. /polis/")
    parser.add_argument("--site-url",default="",help="Canonical HTTPS origin for sitemap")
    args=parser.parse_args();build(args.base_path,args.site_url)

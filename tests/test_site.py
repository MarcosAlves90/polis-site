"""Build contract checks: navigation, links, metadata, document safety and paths."""
import json
import sys
import unittest
from pathlib import Path
from urllib.parse import urlsplit, unquote

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from build import build, frontmatter, markdown_renderer

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"


class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        build()
        cls.pages = list((DIST/"docs").glob("*/index.html"))
        cls.english_pages = list((DIST/"en"/"docs").glob("*/index.html"))

    def soup(self, path):
        return BeautifulSoup(Path(path).read_text(encoding="utf-8"), "html.parser")

    def test_all_document_pages_generated(self):
        self.assertEqual(len(self.pages), len(list((ROOT / 'content').glob('*.md'))))
        self.assertEqual(len(self.pages), 22)
        for file in self.pages + self.english_pages:
            parsed = self.soup(file)
            self.assertEqual(len(parsed.select('h1')), 1, file)
            self.assertTrue(parsed.select_one('main#main'), file)
            self.assertEqual(len(parsed.select('.docs-sidebar a[aria-current="page"]')), 1, file)
            self.assertTrue(parsed.select_one('meta[name="description"]')['content'], file)

    def test_search_index_matches_pages(self):
        data=json.loads((DIST/'search.json').read_text(encoding="utf-8"))
        self.assertEqual(len(data), len(self.pages))
        self.assertEqual(len({row['url'] for row in data}), len(data))
        for row in data:
            self.assertTrue((DIST/row['url'].strip('/')/'index.html').is_file())
            self.assertTrue(row['title'] and row['description'] and row['text'])

    def test_internal_links_resolve(self):
        htmlfiles=[DIST/'index.html', DIST/'en'/'index.html', *self.pages, *self.english_pages, DIST/'404.html', DIST/'en'/'404.html']
        errors=[]
        for file in htmlfiles:
            soup=self.soup(file)
            ids={element.get('id') for element in soup.find_all(id=True)}
            for a in soup.find_all('a', href=True):
                href=a['href']
                if href.startswith('#'):
                    if href[1:] not in ids:
                        errors.append(f'{file}: missing anchor {href}')
                    continue
                parsed=urlsplit(href)
                if parsed.scheme or parsed.netloc or href.startswith(('mailto:', 'tel:')): continue
                if href.startswith('/'):
                    target=DIST/unquote(parsed.path).lstrip('/')
                else:
                    target=file.parent/unquote(parsed.path)
                if target.is_dir(): target=target/'index.html'
                if not target.exists(): errors.append(f'{file}: dead link {href}')
        self.assertFalse(errors,'\n'.join(errors))

    def test_document_headings_have_unique_targets(self):
        for file in self.pages + self.english_pages:
            soup=self.soup(file)
            ids=[h['id'] for h in soup.select('article h2[id], article h3[id]')]
            self.assertEqual(len(ids),len(set(ids)),file)
            for href in [a['href'] for a in soup.select('.docs-toc li a[href]') if a['href'].startswith('#')]:
                self.assertIn(href[1:],ids,file)

    def test_complete_english_localization_and_switching(self):
        self.assertEqual(len(self.english_pages), len(self.pages))
        for file in self.english_pages:
            parsed = self.soup(file)
            self.assertEqual(parsed.html.get('lang'), 'en')
            self.assertEqual(len(parsed.select('h1')), 1)
            self.assertEqual(len(parsed.select('.docs-sidebar a[aria-current="page"]')), 1)
            self.assertEqual(parsed.select_one('nav.locale-switch a[lang="pt-BR"]')['href'].startswith('/docs/'), True, file)
            self.assertEqual(parsed.select_one('nav.locale-switch a[lang="en"][aria-current="page"]')['href'].startswith('/en/docs/'), True, file)
            self.assertTrue(parsed.select_one('article.markdown-body h2'), file)
            self.assertTrue(parsed.select_one('meta[name="description"]')['content'], file)
            self.assertIn('/en/docs/', parsed.select_one('nav.doc-pagination a[href]')['href'] if parsed.select_one('nav.doc-pagination a[href]') else '/en/docs/')
        self.assertEqual(self.soup(DIST/'en'/'index.html').html.get('lang'), 'en')
        self.assertEqual(self.soup(DIST/'en'/'404.html').html.get('lang'), 'en')
        self.assertIn('This page does not exist', (DIST/'en'/'404.html').read_text())
        self.assertEqual(self.soup(DIST/'docs'/'visao-geral'/'index.html').select_one('nav.locale-switch a[lang="en"]')['href'], '/en/docs/overview/')
        self.assertEqual(self.soup(DIST/'en'/'docs'/'overview'/'index.html').select_one('nav.locale-switch a[lang="pt-BR"]')['href'], '/docs/visao-geral/')

    def test_counterpart_links_are_reciprocal(self):
        for english in self.english_pages:
            en_doc = self.soup(english)
            other = en_doc.select_one('nav.locale-switch a[lang="pt-BR"]')['href']
            pt_path = DIST / other.lstrip('/') / 'index.html'
            self.assertTrue(pt_path.is_file(), english)
            pt_doc = self.soup(pt_path)
            expected_english = '/' + english.parent.relative_to(DIST).as_posix() + '/'
            self.assertEqual(pt_doc.select_one('nav.locale-switch a[lang="en"]')['href'], expected_english)

    def test_both_languages_have_visible_explicit_pt_en_navigation(self):
        """The PT selector must not depend on the EN template or JavaScript."""
        html_files = [DIST/'index.html', DIST/'en'/'index.html', DIST/'404.html', DIST/'en'/'404.html', *self.pages, *self.english_pages]
        for file in html_files:
            soup = self.soup(file)
            locale = 'en' if file.relative_to(DIST).parts[0] == 'en' else 'pt'
            nav = soup.select_one('header nav.locale-switch')
            self.assertIsNotNone(nav, file)
            links = nav.select('a.locale-option')
            self.assertEqual([link.text.strip() for link in links], ['PT', 'EN'], file)
            self.assertEqual([link['lang'] for link in links], ['pt-BR', 'en'], file)
            self.assertEqual(len(nav.select('a[aria-current="page"]')), 1, file)
            self.assertEqual(nav.select_one('a[aria-current="page"]')['lang'], 'en' if locale == 'en' else 'pt-BR', file)
            for link in links:
                path = DIST / link['href'].lstrip('/')
                self.assertTrue((path/'index.html').is_file(), (file, link['href']))
            self.assertNotIn('hidden', nav.attrs, file)
        css = (DIST/'assets'/'nautical.css').read_text(encoding='utf-8')
        self.assertIn('.locale-switch {', css)
        self.assertIn('.locale-option[aria-current="page"]', css)

    def test_localized_open_graph_image_metadata(self):
        import struct
        for locale, path, suffix in [('pt', DIST/'index.html', 'pt'), ('en', DIST/'en'/'index.html', 'en')]:
            soup = self.soup(path)
            source = '/assets/og-cover-' + suffix + '.png'
            self.assertEqual(soup.select_one('meta[property="og:image"]')['content'], source)
            self.assertEqual(soup.select_one('meta[name="twitter:image"]')['content'], source)
            self.assertEqual(soup.select_one('meta[property="og:image:width"]')['content'], '1200')
            self.assertEqual(soup.select_one('meta[property="og:image:height"]')['content'], '630')
            self.assertTrue(soup.select_one('meta[property="og:image:alt"]')['content'])
            asset = DIST / source.lstrip('/')
            header = asset.read_bytes()[:24]
            self.assertEqual(header[:8], b'\x89PNG\r\n\x1a\n')
            self.assertEqual(struct.unpack('>II', header[16:24]), (1200, 630))
        for path in self.pages:
            self.assertEqual(self.soup(path).select_one('meta[property="og:image"]')['content'], '/assets/og-cover-pt.png')
        for path in self.english_pages:
            self.assertEqual(self.soup(path).select_one('meta[property="og:image"]')['content'], '/assets/og-cover-en.png')

    def test_english_search_index_is_language_scoped(self):
        index = json.loads((DIST/'en'/'search.json').read_text(encoding='utf-8'))
        self.assertEqual(len(index), len(self.english_pages))
        self.assertEqual(len({item['url'] for item in index}), len(self.english_pages))
        for item in index:
            self.assertTrue(item['url'].startswith('/en/docs/'))
            self.assertTrue((DIST / item['url'].strip('/') / 'index.html').is_file())
        self.assertTrue(any('preflight' in item['text'].lower() for item in index))
        self.assertTrue(any(item['title'] == 'Overview' for item in index))

    def test_search_input_exposes_combobox_semantics(self):
        for file in [DIST/'index.html', DIST/'en'/'index.html', self.pages[0], self.english_pages[0]]:
            soup = self.soup(file)
            search = soup.select_one('#site-search')
            results = soup.select_one('#search-results')
            self.assertEqual(search['role'], 'combobox', file)
            self.assertEqual(search['aria-autocomplete'], 'list', file)
            self.assertEqual(search['aria-controls'], results['id'], file)
            self.assertEqual(search['aria-expanded'], 'false', file)
            self.assertEqual(results['role'], 'listbox', file)

    def test_markdown_does_not_render_unsafe_html(self):
        markup,_=markdown_renderer('<script>alert(1)</script>\n\n[run](javascript:alert(1))\n\n## Header')
        self.assertNotIn('<script>',markup)
        self.assertNotIn('href="javascript:',markup)

    def test_static_assets_and_404(self):
        for path in ['index.html','docs/index.html','404.html','assets/styles.css','assets/app.js','assets/favicon.svg','search.json','.nojekyll','robots.txt']:
            self.assertTrue((DIST/path).exists(),path)

    def test_inter_font_is_self_hosted_for_both_languages(self):
        fonts = DIST / 'assets' / 'fonts'
        filenames = [
            'inter-latin-variable.woff2', 'inter-latin-ext-variable.woff2',
            'inter-latin-italic-variable.woff2', 'inter-latin-ext-italic-variable.woff2',
        ]
        self.assertTrue((fonts/'LICENSE.txt').is_file())
        css = (DIST/'assets'/'styles.css').read_text(encoding='utf-8')
        self.assertEqual(css.count('@font-face'), 4)
        self.assertEqual(css.count('font-display: swap'), 4)
        self.assertEqual(css.count('font-weight: 100 900'), 4)
        self.assertIn('--font:Inter,', css)
        for filename in filenames:
            self.assertIn(f'url("fonts/{filename}")', css)
            self.assertTrue((fonts/filename).read_bytes().startswith(b'wOF2'), filename)
        for file in [DIST/'index.html', DIST/'en'/'index.html',
                     DIST/'docs'/'visao-geral'/'index.html',
                     DIST/'en'/'docs'/'overview'/'index.html']:
            preload = self.soup(file).select_one('link[rel="preload"][as="font"]')
            self.assertIsNotNone(preload, file)
            self.assertEqual(preload['href'], '/assets/fonts/inter-latin-variable.woff2', file)
            self.assertEqual(preload['type'], 'font/woff2', file)
            self.assertIn('crossorigin', preload.attrs, file)

    def test_vercel_deploys_static_build_without_python_runtime(self):
        config = json.loads((ROOT/'vercel.json').read_text(encoding='utf-8'))
        self.assertIsNone(config['framework'])
        self.assertEqual(config['installCommand'], 'uv venv .venv && uv pip install --python .venv/bin/python -r requirements.txt')
        self.assertEqual(config['buildCommand'], '.venv/bin/python build.py')
        self.assertEqual(config['outputDirectory'], 'dist')
        self.assertTrue(config['trailingSlash'])
        self.assertNotIn('builds', config)
        self.assertNotIn('functions', config)
        for route in ['index.html', 'en/index.html', 'docs/visao-geral/index.html',
                      'en/docs/overview/index.html', 'assets/app.js', 'assets/og-cover-pt.png',
                      'en/search.json', '404.html']:
            self.assertTrue((DIST/route).is_file(), route)

    def test_nautical_theme_assets(self):
        for path in ("assets/nautical.css", "assets/cover-art.webp"):
            self.assertTrue((DIST / path).is_file(), path)
        home = self.soup(DIST / "index.html")
        stylesheets = [link.get("href") for link in home.select('link[rel="stylesheet"]')]
        self.assertIn("/assets/nautical.css", stylesheets)
        self.assertEqual(home.select_one('meta[name="theme-color"]')["content"], "#091622")
        css = (DIST / "assets/nautical.css").read_text(encoding="utf-8")
        self.assertIn(":root[data-theme=\"light\"]", css)
        self.assertIn("cover-art.webp", css)

    def test_configurable_base_path(self):
        build('/polis-site/', 'https://example.com')
        page=self.soup(DIST/'docs'/'visao-geral'/'index.html')
        self.assertEqual(page.select_one('link[rel="canonical"]')['href'], 'https://example.com/polis-site/docs/visao-geral/')
        self.assertEqual(page.select_one('link[rel="stylesheet"]')['href'], '/polis-site/assets/styles.css')
        self.assertEqual(page.select_one('link[rel="preload"][as="font"]')['href'], '/polis-site/assets/fonts/inter-latin-variable.woff2')
        self.assertTrue((DIST/'sitemap.xml').is_file())
        en=self.soup(DIST/'en'/'docs'/'overview'/'index.html')
        self.assertEqual(en.select_one('link[rel="canonical"]')['href'], 'https://example.com/polis-site/en/docs/overview/')
        self.assertEqual(en.select_one('nav.locale-switch a[lang="pt-BR"]')['href'], '/polis-site/docs/visao-geral/')
        self.assertEqual(page.select_one('nav.locale-switch a[lang="en"]')['href'], '/polis-site/en/docs/overview/')
        self.assertEqual(page.select_one('link[rel="alternate"][hreflang="en"]')['href'], 'https://example.com/polis-site/en/docs/overview/')
        self.assertEqual(en.select_one('link[rel="alternate"][hreflang="pt-BR"]')['href'], 'https://example.com/polis-site/docs/visao-geral/')
        self.assertEqual((DIST/'sitemap.xml').read_text().count('<loc>'), 2 + len(self.pages) + len(self.english_pages))
        self.assertEqual(page.select_one('meta[property="og:image"]')['content'], 'https://example.com/polis-site/assets/og-cover-pt.png')
        self.assertEqual(en.select_one('meta[property="og:image"]')['content'], 'https://example.com/polis-site/assets/og-cover-en.png')
        # Leave default deploy output for the final deliverable.
        build()

    def test_v612_workflows_are_localized_and_distinct(self):
        """POLIS v6.12.0 local validation and remote handoff have different outputs."""
        for lang, local_slug, remote_slug, install_slug in [
            ('', 'validacao-local', 'entrega-remota', 'instalacao'),
            ('en/', 'local-workspace-validation', 'remote-delivery', 'installation'),
        ]:
            docs = DIST / lang / 'docs'
            local = self.soup(docs / local_slug / 'index.html')
            remote = self.soup(docs / remote_slug / 'index.html')
            install = self.soup(docs / install_slug / 'index.html')
            local_text = local.get_text(' ', strip=True)
            remote_text = remote.get_text(' ', strip=True)
            self.assertIn('workspace validate', local_text)
            self.assertIn('workspace_validated', local_text)
            self.assertIn('delivery_artifact_built', local_text)
            self.assertIn('polis build', remote_text)
            self.assertIn('preflight', remote_text)
            self.assertIn('v6.12.0', install.get_text(' ', strip=True))
            source = local.select_one('.doc-meta a[href]')
            self.assertIsNotNone(source)
            self.assertTrue(source['href'].endswith('/docs/workflows/local-agent-workspace.md'))

        for homepage in (DIST / 'index.html', DIST / 'en' / 'index.html'):
            html = homepage.read_text(encoding='utf-8')
            self.assertIn('POLIS v6.12.0', html)
            self.assertIn('POLIS_OUTSIDE', html)
            self.assertIn('--policy', html)
            self.assertIn('workspace validate', html)

        for file in [*self.pages, *self.english_pages]:
            html = file.read_text(encoding='utf-8')
            self.assertNotIn('docs/usage.md#command-reference', html)
            self.assertNotIn('docs/usage.md#repository-artifact-retention', html)

    def test_first_run_doctor_waits_for_project_policy(self):
        """A fresh checkout has no committed policy for repository diagnostics."""
        for homepage in (DIST / 'index.html', DIST / 'en' / 'index.html'):
            page = self.soup(homepage)
            terminal = page.select_one('.terminal-card').get_text(' ', strip=True)
            self.assertIn('polis doctor', terminal)
            self.assertNotIn('polis doctor --repo', terminal)
            snippet = page.select_one('#install-snippet').get_text()
            init_command = 'polis init --repo . --profile auto --dry-run'
            repo_doctor = 'polis doctor --repo . --policy "$POLIS_OUTSIDE/policy.json"'
            self.assertIn('polis doctor\n', snippet)
            self.assertIn(repo_doctor, snippet)
            self.assertLess(snippet.index('polis doctor\n'), snippet.index(init_command))
            self.assertLess(snippet.index(init_command), snippet.index(repo_doctor))
            self.assertIn('Windows (Git Bash)', page.select_one('.snippet-footer').get_text())

        for locale in (Path('content'), Path('content/en')):
            for filename in ('primeiros-passos.md', 'validacao-local.md', 'comandos.md'):
                source = (ROOT / locale / filename).read_text(encoding='utf-8')
                init_command = 'polis init --repo . --profile auto --dry-run'
                repo_doctor = 'polis doctor --repo . --policy '
                self.assertIn(init_command, source)
                self.assertIn(repo_doctor, source)
                self.assertLess(source.index(init_command), source.index(repo_doctor))
                self.assertNotIn('polis doctor --repo .\n', source)


if __name__ == '__main__':
    unittest.main()

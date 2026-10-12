# Contributing to the POLIS documentation website

Use English for repository-maintainer documentation, code comments, configuration descriptions,
commit messages, pull request titles, and pull request descriptions. The published site is intentionally
bilingual: keep visitor-facing Portuguese text in the Portuguese locale and English text in the English
locale. Do not translate identifiers, URLs, code examples, or normative POLIS terminology merely to
make them look like English prose.

## Documentation and naming

- Write clear, factual English, using sentence case for headings, pull request titles, and descriptions.
  Prefer short sentences, Markdown headings in order, fenced code blocks with language tags, and
  descriptive link text. Avoid unnecessary jargon and unverified claims.
- Use `POLIS` for the project, `POLIS CLI` for the command-line tool, `V6 Specification` for the
  authoritative protocol document, and `producer`, `reader`, and `consumer` for the protocol roles.
  Use `pull request` in prose and `PR` only when space is limited.
- Preserve the existing lowercase, hyphen-separated filenames and public URLs. Every page must have
  matching filenames in `content/` and `content/en/`. The English page can use an English `slug`;
  keep the Portuguese route stable for existing links.
- Every Markdown page needs `title`, `description`, `group`, and `order` frontmatter; `source`
  and `slug` are optional. Write localized titles and descriptions in the page's language.
  Descriptions should be concise sentences ending with a period. The `group` value is a stable
  internal ID, currently written in Portuguese in both locales; its display label comes from
  `i18n.py`. Do not translate the ID unless updating the generator and every page together.
- Translate visible navigation, alt text, labels, and page content for both locales. Keep internal
  comments, docstrings, configuration labels, and scripts in English. Preserve code, command names,
  links, and citation targets unless a functional correction requires changing them.
- Verify factual statements against the upstream
  [POLIS V6 Specification](https://github.com/MarcosAlves90/polis/blob/main/spec/POLIS-SPEC-v6.md).
  This website explains the protocol; it does not define new protocol behavior.

## Commit messages

Use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) and write the entire
message in English:

```text
<type>[(scope)][!]: <imperative summary>

<optional explanation of the motivation and effect>

<optional BREAKING CHANGE: description or issue references>
```

Square brackets indicate optional parts; the literal scope uses parentheses. Use lowercase types:
`feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`,
`ci`, `chore`, or `revert`. Keep scopes lowercase and hyphen-separated (for example,
`docs(content)` or `fix(search)`). Start the summary with a verb, keep the subject to
72 characters or fewer, and omit its ending period. Use `!` and explain `BREAKING CHANGE:` in
the body when compatibility is affected.

Examples:

```text
docs: Standardize contributor documentation
fix(search): Preserve language-specific search links
ci: Validate pull request titles
```

Do not rewrite existing history to conform to these rules. The CI check validates only commits
introduced by the push or pull request and excludes Git-generated merge commits.

To enable the same subject check locally, run once from the repository root:

```bash
git config --local core.hooksPath .githooks
```

This sets the repository's hook directory; it replaces any previously configured local hooks path.
The check also runs without installing the hook:

```bash
python3 tools/check_conventions.py commit-message "docs: Clarify language conventions"
```

## Pull requests

Write PR titles as Conventional Commit subjects in English, preferably describing the user-visible
effect. Use the repository's [PR template](.github/PULL_REQUEST_TEMPLATE.md) and complete its
`Summary` and `Validation` sections in English. Explain what changed and why, which checks
were run and their outcomes, and any material risk or limitation. If a check is not applicable,
state that explicitly. Reference related issues when useful.

The CI convention check validates the PR title, the presence of substantive `Summary` and
`Validation` sections, and newly introduced commit subjects. It cannot reliably determine the
language or accuracy of free-form text; reviewers must enforce the English-language requirement.
These rules apply to new contributions only.

## Validation

Use Python 3.10+ and build the site after changes to documentation, templates, or assets:

```bash
uv venv --allow-existing .venv
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python build.py
node --check assets/app.js
```

The build produces 20 Portuguese and 20 English documentation pages, with distinct navigation
routes and search indexes. Inspect both locales when editing shared templates or styling.
Do not commit generated `dist/` files. See [README.md](README.md) for hosting details.

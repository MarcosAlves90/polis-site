---
slug: contributing
title: Contributing and evolution
description: Find POLIS authoritative sources and report documentation or implementation issues.
group: Projeto
order: 2
source: README.md
---

POLIS source code and history are maintained on GitHub. Before proposing changes, review the current specification and behavior of the CLI revision in question.

## Repository and key documents

- [POLIS source code](https://github.com/MarcosAlves90/polis)
- [README and project entry point](https://github.com/MarcosAlves90/polis/blob/main/README.md)
- [V6 Specification](https://github.com/MarcosAlves90/polis/blob/main/spec/POLIS-SPEC-v6.md)
- [Operational guide](https://github.com/MarcosAlves90/polis/blob/main/docs/usage.md)
- [Changelog](https://github.com/MarcosAlves90/polis/blob/main/CHANGELOG.md)
- [Issues and bug reports](https://github.com/MarcosAlves90/polis/issues)

## Proposing a fix

Report the observed behavior, source revision/version, reproduction steps, expected and actual results, and supporting evidence. For protocol semantic changes, establish the applicable specification first.

## Contributing to this website

The site is designed for small, independently maintainable changes:

1. Create or edit a Portuguese Markdown file in `content/` and its English counterpart in `content/en/`, with matching filenames and `title`, `description`, `group`, `order`, and `source` frontmatter.
2. Write sections in Markdown and reference the relevant official source. Use English-language route names when linking from translated content.
3. Run `python build.py` to generate static pages and language-specific indexes in `dist/`.
4. Run tests and review routes, search, responsive behavior, and alignment with the POLIS repository.

This site is an educational and operational guide; it does not establish a competing normative specification.

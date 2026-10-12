---
slug: architecture
title: Architecture
description: How the engineering guide, normative specification, and Go CLI work together.
group: Projeto
order: 1
source: docs/usage.md
---

POLIS separates **engineering process**, **verifiable contracts**, and **executable implementation**. This prevents narrative guidance from silently redefining the meaning of package bytes.

## Repository layers

| Layer | Directory | Responsibility |
| --- | --- | --- |
| Engineering Guide | `guide/` | Process, scope, evidence obligations, and delivery practices. |
| POLIS Specification | `spec/` | Normative schemas, package rules, hashing, evidence, signing, and application. |
| CLI | `cmd/polis/` | Command-line interface and operations. |
| Implementation | `internal/` | Supporting Go code for execution and validation. |
| Documentation | `docs/` | Operational guides, installation, examples, and design decisions. |

## Normative authority

If an Engineering Guide explanation conflicts with a package rule, the **versioned Specification** governs machine-level semantics. The CLI is the reference implementation, but its actual behavior still needs to be verified through tests and execution.

## Producer and consumer

The producer executes development proof and produces a target Git tree and `.polis` package. The consumer receives untrusted bytes, validates integrity and applicable rules, and performs its own checks before any mutation.

This separation limits claims such as “it passed on the author's machine”: consumer identity, source state, and effective commands also matter.

## Dependencies and distribution

The CLI is written in Go and uses Git for change identity and application. The V6 module path is `github.com/MarcosAlves90/polis/v6`. In addition to Go installation, the project distributes platform-specific offline kits containing the binary and supporting CLI resources.

## Maintaining this website

Source documents are maintained in `content/` (Portuguese) and `content/en/` (English). The static generator `build.py` creates HTML, language-matched navigation, and separate search indexes. Presentation lives in `assets/styles.css` and `assets/nautical.css`; interactions live in `assets/app.js`. Website explanations can evolve independently of CLI implementation.

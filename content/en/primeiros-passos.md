---
slug: quickstart
title: Quickstart
description: Install, diagnose, and inspect validation for a Git repository before preparing a delivery.
group: Comece aqui
order: 3
source: docs/usage.md
---

This guide introduces the first commands and distinguishes **configuration inspection** from a **verified delivery**. A successful `plan` or `gates` run does not mean that a `.polis` package exists.

## 1. Install and diagnose

```bash
go install github.com/MarcosAlves90/polis/v6/cmd/polis@latest
polis doctor
```

`doctor` checks CLI prerequisites. See [Installation](../installation/) if the binary is not on `PATH`.

## 2. Choose a Git repository

Work in a repository whose state you can inspect. POLIS identifies the Git state and the policy that governs project validation.

```bash
cd /path/to/your/project
git status --short
```

Do not discard local changes simply to satisfy the CLI. POLIS intentionally blocks ambiguous states rather than silently accepting them.

## 3. Preview policy generation without writing files

For a root Go module, `auto` can generate a profile. Preview it without persisting files:

```bash
polis init --repo . --profile auto --dry-run
```

Automatic profile detection supports root Go modules. Other ecosystems require explicit commands through the `custom` profile.

If you decide to persist the policy, run `init` without `--dry-run` and **review the generated files before committing**:

```bash
polis init --repo . --profile auto
```

## 4. Inspect the validation plan

```bash
polis plan --repo .
```

`plan` is read-only. It shows enabled gates, dependencies, commands, and the effective policy's guarantees and limitations. Run configured gates locally with:

```bash
polis gates --repo .
```

> `gates` validates project commands; it does not create or verify a delivery artifact. That requires a locked contract, the required proof, and `build` followed by `verify`.

## 5. Prepare a full delivery

A complete delivery needs a behavioral Specification, Change Contract, authorized scope, and proof strategy. Their schemas and preconditions are normative and should not be improvised from an isolated command example.

Continue with [Delivery workflow](../delivery-workflow/) and [SDD and TDD](../sdd-and-tdd/). Commands shown here illustrate **syntax**, not ready-made valid contracts.

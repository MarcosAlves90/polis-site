---
slug: cli-commands
title: CLI commands
description: A practical POLIS V6 command reference organized by workflow stage.
group: Referência
order: 1
source: docs/usage.md
---

This page is a purpose-oriented index. For complete options, run **`polis help <command>`**, `polis <command> --help`, or consult the [official command reference](https://github.com/MarcosAlves90/polis/blob/main/docs/usage.md#command-reference).

## Discovery and preparation

| Command | Purpose |
| --- | --- |
| `help` | Show read-only syntax and operational guidance. |
| `doctor` | Check CLI prerequisites and environment. |
| `init` | Generate Project Policy using a chosen profile. |
| `plan` | Preview effective policy, gates, dependencies, and assurances without execution. |
| `status` | Summarize workflow state and the next step using supplied inputs. |

```bash
polis help
polis help start
polis doctor --format json
polis init --repo . --dry-run
polis plan --repo .
```

## Validation and planning

| Command | Purpose |
| --- | --- |
| `gates` | Execute Project Policy gates, including selected or affected subsets. |
| `workspace validate` | Validate a locked change without producing a `.polis` package. |
| `workspace status` | Compare source identity against an unauthenticated checkpoint. |
| `implementation-plan` | Generate an optional plan derived from the locked contract. |

```bash
polis gates --repo . --affected
polis implementation-plan --repo /repo \
  --contract /outside/locked-v6.json \
  --out /outside/implementation-plan.json
```

## Delivery production

| Command | Purpose |
| --- | --- |
| `start` | Lock the contract to a baseline and effective policy. |
| `check-red-scope` | Check that proposed test paths are authorized. |
| `capture-red` | Capture genuine Red proof for a Red-to-Green change. |
| `build` | Validate and produce a verifiable change package. |

```bash
polis start --repo /repo --policy /outside/policy-v3.json \
  --contract /outside/draft-v5.json \
  --out /outside/locked-v6.json
```

## Reading and consumption

| Command | Purpose |
| --- | --- |
| `verify` | Validate package integrity and consistency. |
| `inspect` | Read validated package metadata. |
| `preflight` | Validate against the consumer without applying changes. |
| `apply` | Revalidate and apply, only after authorization. |
| `sign` | Produce a detached package signature. |
| `export` | Create an offline runtime bundle, not a delivery package. |

```bash
polis verify artifact.polis
polis inspect --format json artifact.polis
polis preflight --repo /consumer artifact.polis
```

## Choose the appropriate operation

- Use `plan` to **preview** validation and `gates` to **execute** local checks.
- Use `workspace validate` to validate without a package and `build` to create one.
- Use `verify` for package bytes and `preflight` for a particular target repository.
- Use authorized `apply` only when intending to modify consumer files.

Options and semantics may evolve within the V6 release line. Always check `polis help` from the installed CLI for exact behavior.

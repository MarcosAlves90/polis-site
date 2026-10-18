---
slug: cli-commands
title: CLI commands
description: A practical POLIS V6 command reference organized by workflow stage.
group: Referência
order: 1
source: docs/commands.md
---

This page is a purpose-oriented index. For complete options, run **`polis help <command>`**, `polis <command> --help`, or consult the [official command reference](https://github.com/MarcosAlves90/polis/blob/main/docs/commands.md#agent-command-instructions), which is embedded in CLI help.

## Discovery and preparation

| Command | Purpose |
| --- | --- |
| `help` | Show read-only syntax and operational guidance. |
| `doctor` | Check CLI prerequisites; `--repo` adds static repository checks with optional `--policy`. |
| `init` | Generate Project Policy and, without `--dry-run`, a policy-provenance manifest. |
| `plan` | Preview gates, guarantees, and decision sources/reasons without execution. Plan JSON v4. |
| `status` | Project external workflow evidence and next actions (`proven`, `stale_or_unproven`, `missing`). |

```bash
polis help
polis help start
polis doctor --format json
polis init --repo . --profile auto --dry-run > /outside/policy.json
polis doctor --repo . --policy /outside/policy.json
polis plan --repo . --policy /outside/policy.json --format json
```

## Validation and planning

| Command | Purpose |
| --- | --- |
| `gates` | Execute Project Policy gates, including selected/affected subsets and conditional replay/reuse. |
| `workspace validate` | Validate a locked change without a `.polis` package; accepts `--jobs 1..16`. |
| `workspace status` | Compare source identity against an unauthenticated checkpoint. |
| `implementation-plan` | Generate an optional plan derived from the locked contract. |

```bash
polis gates --repo . --policy /outside/policy.json --affected
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
| `build` | Validate and write a package to a physically external directory; accepts `--jobs 1..16`. |

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

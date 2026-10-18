---
slug: cli-commands
title: CLI commands
description: A practical POLIS V6 command reference organized by workflow stage.
group: Referência
order: 1
source: docs/commands.md
---

This page is a purpose-oriented index. For complete options, run **`polis help <command>`**, `polis <command> --help`, or consult the [official command reference](https://github.com/MarcosAlves90/polis/blob/main/docs/commands.md#agent-command-instructions), which is embedded in CLI help.

The examples assume a **Git checkout with a root Go module** and an external policy. Keep `POLIS_OUTSIDE` physically outside the repository (including when you set it yourself). Contract and package paths in later sections require valid inputs produced in earlier stages; they are not automatically generated filenames.

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
POLIS_OUTSIDE="${POLIS_OUTSIDE:-$(mktemp -d)}"
mkdir -p "$POLIS_OUTSIDE"
polis init --repo . --profile auto --dry-run > "$POLIS_OUTSIDE/policy.json"
polis doctor --repo . --policy "$POLIS_OUTSIDE/policy.json"
polis plan --repo . --policy "$POLIS_OUTSIDE/policy.json" --format json
```

## Validation and planning

| Command | Purpose |
| --- | --- |
| `gates` | Execute Project Policy gates, including selected/affected subsets and conditional replay/reuse. |
| `workspace validate` | Validate a locked change without a `.polis` package; accepts `--jobs 1..16`. |
| `workspace status` | Compare source identity against an unauthenticated checkpoint. |
| `implementation-plan` | Generate an optional plan derived from the locked contract. |

`implementation-plan` requires a **contract previously locked with `polis start`** (shown in the next section) and the same policy used during locking. The blocks below illustrate commands by purpose, not a sequence that skips prerequisites.

```bash
polis gates --repo . --policy "$POLIS_OUTSIDE/policy.json" --affected
polis implementation-plan --repo . \
  --policy "$POLIS_OUTSIDE/policy.json" \
  --contract "$POLIS_OUTSIDE/locked-v6.json" \
  --out "$POLIS_OUTSIDE/implementation-plan.json"
```

## Delivery production

| Command | Purpose |
| --- | --- |
| `start` | Lock the contract to a baseline and effective policy. |
| `check-red-scope` | Check that proposed test paths are authorized. |
| `capture-red` | Capture genuine Red proof for a Red-to-Green change. |
| `build` | Validate and write a package to a physically external directory; accepts `--jobs 1..16`. |

```bash
polis start --repo . --policy "$POLIS_OUTSIDE/policy.json" \
  --contract "$POLIS_OUTSIDE/draft-v5.json" \
  --out "$POLIS_OUTSIDE/locked-v6.json"
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

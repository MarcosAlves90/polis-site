---
slug: quickstart
title: Quickstart
description: Start with POLIS 6.12.0 and choose local checkout validation or remote delivery.
group: Comece aqui
order: 3
source: docs/quickstart.md
---

This guide first checks prerequisites, then distinguishes **validation in your existing checkout** from **package delivery to another checkout**. A successful `plan` or `gates` run does not mean that a `.polis` package exists.

## First, choose how the AI works

- **An AI coding agent on your machine, working in the same checkout:** follow [Local workspace validation](../local-workspace-validation/). After contract, proof, and implementation, use `polis workspace validate`; **no delivery `.polis` file is needed**.
- **Web chatbot or AI delivering changes to another checkout:** follow [Remote delivery](../remote-delivery/). Someone with actual checkout, Git, and POLIS access runs `build` and `verify`; the consumer decides whether to run `preflight` and `apply`. A web chat alone does not produce the package.

The `change.polis` package is a transferable file; the `.polis/` folder and `.polis/policy.json` are project configuration. The example below uses an **external JSON policy** for either workflow. Shell snippets use Bash (Git Bash on Windows); see [Installation](../installation/) for OS-specific options.

## 1. Install and diagnose

```bash
go install github.com/MarcosAlves90/polis/v6/cmd/polis@latest
polis doctor
```

`doctor` without `--repo` checks CLI prerequisites even before a policy exists. After preparing the policy, run `doctor --repo . --policy <file>` to inspect policy and tooling statically without executing gates. See [Installation](../installation/) if the binary is not on `PATH`.

## 2. Choose a Git repository

Work in a repository whose state you can inspect. POLIS identifies the Git state and the policy that governs project validation.

```bash
cd /path/to/your/project
git status --short
```

Do not discard local changes simply to satisfy the CLI. POLIS intentionally blocks ambiguous states rather than silently accepting them.

## 3. Prepare an external policy without modifying the checkout

For a root Go module, `auto` can generate a profile. Preview it without persisting files:

```bash
# Keep temporary outputs outside the worktree.
POLIS_OUTSIDE="${POLIS_OUTSIDE:-$(mktemp -d)}"
mkdir -p "$POLIS_OUTSIDE"
polis init --repo . --profile auto --dry-run > "$POLIS_OUTSIDE/policy.json"
polis doctor --repo . --policy "$POLIS_OUTSIDE/policy.json"
```

Automatic profile detection supports root Go modules. Other ecosystems require explicit commands through the `custom` profile.

If you decide to persist the policy, run `init` without `--dry-run` and **review both the policy and `.polis/policy-provenance.json` before committing**:

```bash
polis init --repo . --profile auto
```

## 4. Inspect the validation plan

```bash
polis plan --repo . --policy "$POLIS_OUTSIDE/policy.json"
```

`plan` is read-only. It shows enabled gates, dependencies, commands, and the effective policy's guarantees and limitations. Run configured gates locally with:

```bash
polis gates --repo . --policy "$POLIS_OUTSIDE/policy.json"
```

> `gates` runs project checks but does not produce or verify a delivery package. `--affected` and `--reuse` may execute only a subset; full delivery gates and contract proof still apply.

## 5. Choose your validation workflow

Both workflows require a behavioral Specification, locked Change Contract, authorized scope, and appropriate proof. Their schemas and prerequisites are normative and must not be improvised from an isolated command example.

- **Same checkout:** follow [Local workspace validation](../local-workspace-validation/) using `polis workspace validate` to save an external checkpoint without building a package.
- **Different checkout:** follow [Remote delivery](../remote-delivery/) using `polis build`, `verify`, `preflight`, and `apply` with an external disposable package.

See also [SDD and TDD](../sdd-and-tdd/). Commands shown here illustrate syntax, not production-ready contracts.

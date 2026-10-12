---
slug: troubleshooting
title: Troubleshooting
description: Diagnose installation errors, gates, scope, baseline issues, and rejected application.
group: Referência
order: 3
source: docs/usage.md
---

POLIS blockers typically indicate that an identity, precondition, or proof needs attention. The right response depends on **the reported cause**, not solely the exit code.

## `polis: command not found`

After `go install`, check `go env GOBIN` and `go env GOPATH`. Add the binary directory to `PATH` and run `polis doctor`. See [Installation](../installation/).

## Gate BLOCKED due to missing tooling

Read the gate diagnostic and check required dependencies in the intended environment. `BLOCKED` is not a failing test assertion. Do not rewrite a Red oracle to accept missing tooling as proof of an actual regression.

## `start` rejects the baseline

Inspect the worktree, real index, policy identity, and contract schema. `start` is designed to happen **before** production edits. Do not reset, stash, or delete someone else's work to make it pass.

## `check-red-scope` rejects a path

The proposed path must fit both the authorized test scope and overall Change Contract scope. Review `test_scope.allowed_paths` and `scope.allowed_paths` before editing files or revising the contract.

## Gate reuse was denied

`--reuse` requires matching input identities and an explicit `--environment-id`. That identifier is an operator assertion, not proof the actual environment matches. For fresh evidence, rerun the gates rather than forcing invalid reuse.

## Preflight rejects the baseline

The default `strict` mode requires exact base commit equality. Investigate Git history and only consider `compatible` or `permissive` when their risks are understood and every required check still passes. See [Baseline modes](../baseline-modes/).

## Apply fails

Stop further mutations. Inspect the CLI diagnostic, `git status`, the index, and target tree. Transactional recovery attempts to restore state, but the operator must verify the reported result before retrying.

## Find authoritative help

```bash
polis help
polis help preflight
polis help apply
```

Consult the [full official usage guide](https://github.com/MarcosAlves90/polis/blob/main/docs/usage.md), and [open an issue](https://github.com/MarcosAlves90/polis/issues) for reproducible discrepancies.

---
slug: troubleshooting
title: Troubleshooting
description: Diagnose installation errors, gates, scope, baseline issues, and rejected application.
group: Referência
order: 3
source: docs/commands.md
---

POLIS blockers typically indicate that an identity, precondition, or proof needs attention. The right response depends on **the reported cause**, not solely the exit code.

## Check the repository before running gates

Use `polis doctor --repo /repo` to inspect policy, working directories, output paths, and available executables without running configured gates. Include `--policy /outside/policy.json` when the policy is external. Diagnostic `PASS`, `BLOCKED`, or `FAIL` does **not** mean project tests ran.

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

When a gate declares `input_paths_complete: true`, also check ignored files, directories, and dependencies. The field is valid only for exhaustive paths; external conditions remain the executor's responsibility.

## `status` reports incomplete evidence

`polis status` may classify inputs as `proven`, `stale_or_unproven`, or `missing`. A successful exit does not turn a historical report into fresh validation or prove the implementation is complete. Inspect input identities and rerun `workspace validate` after changing source.

## `build` rejects its output path

Confirm `--out` resolves physically outside the worktree and does not collide with a previous output. `.polis` packages cannot be produced or retained inside the repository; final cleanup and verification can also detect file replacement or output-directory relocation.

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

Consult the [official command reference](https://github.com/MarcosAlves90/polis/blob/main/docs/commands.md), and [open an issue](https://github.com/MarcosAlves90/polis/issues) for reproducible discrepancies.

---
slug: validation-and-gates
title: Validation and gates
description: Execute quality policies, inspect dependencies, and distinguish local checks from delivery validation.
group: Fluxo de entrega
order: 5
source: docs/gates-and-progress.md
---

A **gate** is a Project Policy check. It may run tests, coverage, lint, or another configured command. Project Policy controls quality checks, while mandatory protocol integrity and safety invariants remain in force.

## Inspect before execution

```bash
polis plan --repo . --policy /outside/policy.json
```

`plan` does not execute gates. It lists execution order, commands, dependencies, enabled gates, and the guarantees or limits of the effective policy.

## Run local validation

```bash
polis gates --repo . --policy /outside/policy.json
```

To run selected checks or only those affected by Git changes:

```bash
polis gates --repo . --policy /outside/policy.json --gate lint --gate coverage
polis gates --repo . --policy /outside/policy.json --affected
```

Required dependencies are added automatically. `--jobs` accepts 1 through 16; gates overlap only when explicitly marked `parallel_safe`. Coverage remains exclusive.

> `gates` is **not a sandbox**. It runs configured commands in the actual repository, potentially creating caches or external effects according to project command behavior.

## Reuse and replay

A run can produce a result manifest. POLIS lets you inspect it, conditionally reuse passing results, or replay the selection through fresh execution.

```bash
polis gates --repo . --environment-id toolchain-v1 \
  --policy /outside/policy.json --out-run /outside/first.json

polis gates --inspect-run /outside/first.json

polis gates --repo . --environment-id toolchain-v1 \
  --policy /outside/policy.json --reuse /outside/first.json
```

The environment identifier is **operator asserted**: it does not establish a hermetic environment or verify that external conditions really match. Reuse is disabled without an identifier. Previous results do not prove a modified repository state.

By default, reuse requires global source, Git/index, policy, dependency, and environment identities to match. **Command** gates with exhaustive `input_paths` and `input_paths_complete: true` can opt into input-scoped reuse, including ignored files, empty directories, and directory topology. That declaration cannot prove the command does not read other inputs; coverage remains globally bound. Omitted or reused gates do not replace full `build` or `apply` validation.

To rerun a previous selection, use `polis gates --repo . --policy /outside/policy.json --replay /outside/first.json --environment-id toolchain-v1` with the original policy. Do not combine replay with `--affected`, `--gate`, `--jobs`, or `--reuse`.

## Follow command progress

With `--format json`, executing commands and gates emit `started` and `completed` **JSON Lines on stderr** while the ordinary JSON result remains on stdout. Lifecycle events report the action, reason, scope, ID, result, and completion duration. Reused or skipped gates do not emit execution events; inspect final outcomes instead. On JSON failures, the structured error is the final non-progress stderr record.

## PASS, FAIL, BLOCKED, and DEFERRED

| Status | Meaning |
| --- | --- |
| `PASS` | The applicable check completed successfully. |
| `FAIL` | An executed check found a problem. |
| `BLOCKED` | A prerequisite prevented intended execution. |
| `DEFERRED` | The producer deferred an enabled gate; the consumer still must execute it for supported formats. |

## Strict, standard, and minimal

`strict` is the default. `standard` keeps `test.complete` and disables generated coverage by default. `minimal` disables generated project-quality gates by default. None of these settings relaxes mandatory structure, integrity, scope, or application guarantees.

See [Project Policy](../project-policy/) for gate configuration and [Artifacts and verification](../artifacts-and-verification/) for how validation becomes part of delivery.

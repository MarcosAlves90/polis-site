---
slug: validation-and-gates
title: Validation and gates
description: Execute quality policies, inspect dependencies, and distinguish local checks from delivery validation.
group: Fluxo de entrega
order: 3
source: docs/usage.md
---

A **gate** is a Project Policy check. It may run tests, coverage, lint, or another configured command. Project Policy controls quality checks, while mandatory protocol integrity and safety invariants remain in force.

## Inspect before execution

```bash
polis plan --repo .
```

`plan` does not execute gates. It lists execution order, commands, dependencies, enabled gates, and the guarantees or limits of the effective policy.

## Run local validation

```bash
polis gates --repo .
```

To run selected checks or only those affected by Git changes:

```bash
polis gates --repo . --gate lint --gate coverage
polis gates --repo . --affected
```

Required dependencies are added automatically. `--jobs` accepts 1 through 16; gates overlap only when explicitly marked `parallel_safe`. Coverage remains exclusive.

> `gates` is **not a sandbox**. It runs configured commands in the actual repository, potentially creating caches or external effects according to project command behavior.

## Reuse and replay

A run can produce a result manifest. POLIS lets you inspect it, conditionally reuse passing results, or replay the selection through fresh execution.

```bash
polis gates --repo . --environment-id toolchain-v1 \
  --out-run /outside/first.json

polis gates --inspect-run /outside/first.json

polis gates --repo . --environment-id toolchain-v1 \
  --reuse /outside/first.json
```

The environment identifier is **operator asserted**: it does not establish a hermetic environment or verify that external conditions really match. Reuse is disabled without an identifier. Previous results do not prove a modified repository state.

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

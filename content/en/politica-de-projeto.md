---
slug: project-policy
title: Project Policy
description: Configure explicit checks with Project Policy schema v3 and validation levels strict, standard, and minimal.
group: Conceitos e segurança
order: 2
source: docs/usage.md
---

**Project Policy** defines how POLIS validates a project: commands, gates, dependencies, environments, and enablement decisions. The effective policy digest is bound to the locked Change Contract.

## Begin with inspection

```bash
polis init --repo . --profile auto --dry-run
polis plan --repo .
```

`auto` recognizes root Go modules. Other ecosystems use `--profile custom` with explicitly declared commands. Do not blindly reuse language-specific gates across projects.

## Validation levels

| Level | Behavior |
| --- | --- |
| `strict` | Default: retains the strongest generated project gates. |
| `standard` | Keeps `test.complete` while disabling generated coverage by default. |
| `minimal` | Disables generated project-quality gates by default. |

None of these levels disables mandatory structural, integrity, scope, baseline, or application invariants. Disabled gates and their reasons remain visible.

## Commands use argv, not shell strings

Policy commands are executed as direct arguments. POLIS rejects recognized shell-wrapper forms such as `bash -lc` and `sh -c`. For complex validation, create a version-controlled runner in the project and declare its direct executable invocation.

Illustrative command object:

```json
{
  "argv": ["python", "scripts/validate_project.py"],
  "cwd": ".",
  "timeout_seconds": 600,
  "environment": {
    "mode": "clean",
    "pass": ["PATH", "HOME"]
  }
}
```

> This is **only a command object**, not a complete valid Project Policy. Use the authoritative schema to write one.

## Inherited versus clean environments

`environment.mode=inherit` forwards the process environment. `clean` starts from a controlled base and forwards explicitly named variables, plus applicable Windows bootstrap variables. Environment **values** are not stored in package evidence.

## Dependencies and concurrency

Gates may declare `depends_on`. POLIS validates their dependency graph and computes a deterministic order. Concurrent execution requires an explicit safety assertion; coverage executes exclusively.

## Changing policy requires a new lock

A locked contract binds the policy digest. Changing the policy breaks that identity. Do not weaken gates just to manufacture a passing delivery: review the policy and create a new corresponding baseline and contract.

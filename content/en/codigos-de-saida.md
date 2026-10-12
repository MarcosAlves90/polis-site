---
slug: exit-codes
title: Exit codes
description: Interpret CLI exit statuses and distinguish validation failure from an execution blocker.
group: Referência
order: 2
source: docs/usage.md
---

POLIS uses stable exit categories for automation, without conflating different failure modes into a generic result.

## Exit status categories

| Code | Category | Operational meaning |
| --- | --- | --- |
| `0` | `PASS` | The operation completed under its contract. |
| `2` | Usage error | Invalid syntax, flags, or arguments. |
| `3` | Invalid artifact/signature | Package or cryptographic verification rejected. |
| `4` | Blocked environment or authorization | Preconditions prevented execution or authorized commit. |
| `5` | Baseline mismatch | Consumer state does not satisfy the selected baseline mode. |
| `6` | Validation failure | Proof, gate, contract, or other validated condition failed. |
| `7` | Apply failure | Error during apply, commit, or rollback. |

## Diagnose beyond the code

Exit status is only the most compact signal. Read the contextual diagnostic and, where appropriate, structured output:

```bash
polis doctor --format json
polis plan --repo . --format json
polis preflight --repo /consumer --format json artifact.polis
```

Do not assume all commands use every exit code for the same underlying issue. The CLI help gives command-specific outcomes.

## Test failures versus environment failures

When a required compiler or executable is missing, the intended test **did not run**. In Red-to-Green workflows, that does not demonstrate the baseline fails for the specified behavioral reason.

In CI, treat `BLOCKED` as an unaccepted delivery until the prerequisite is restored—not a success with a warning.

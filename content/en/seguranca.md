---
slug: security
title: Security and trust
description: Understand untrusted packages, signatures, security boundaries, and consumer assurances.
group: Conceitos e segurança
order: 4
source: spec/POLIS-SPEC-v6.md
---

POLIS is designed to **fail closed** on invalid inputs and incompatible states. It is nevertheless important to distinguish its actual guarantees from operator responsibilities.

## Trust boundaries

A `.polis` package must be treated as **untrusted input**. Verification enforces member inventory, size limits, schema validation, checksums, and evidence consistency before admission. The Change Contract restricts authorized file paths and the consumer checks exact target-tree identity.

## Authenticity requires an external trust root

Detached Ed25519 signatures can bind the package's exact bytes to a trusted producer **only when the consumer supplies an independently trusted public key**. A key found inside the package cannot appoint itself as an authority.

```bash
polis verify --signature artifact.polis.sig \
  --trusted-key producer-public.pem \
  artifact.polis
```

## Isolation is not sandboxing

`build`, `preflight`, and `apply` perform relevant validation in isolated repositories or worktrees. That protects Git state but **does not necessarily isolate processes, networks, or credentials**. Review policy commands and proof before executing untrusted content.

## Current state matters

- `preflight` checks the current consumer state, not a permanent approval.
- `apply` repeats validation before modifying files.
- A nonzero exit caused by missing prerequisites does not prove a test found a defect.
- A hash proves byte integrity, not semantic security of source code.

## Explicit authorization

`apply` requires authorization for the intended repository. `--commit-mode auto` requires deliberate authorization to create a local commit. Successful validation must never be taken as permission to publish a release or push a commit.

## Where assurance ends

Even a correctly verified patch may be unsafe in scenarios not covered by tests. Verifiable validation **increases auditability**, but cannot replace code review, threat modeling, or appropriate project testing.

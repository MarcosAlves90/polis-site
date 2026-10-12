---
slug: baseline-modes
title: Baseline modes
description: How strict, compatible, and permissive govern package admission against different Git states.
group: Conceitos e segurança
order: 3
source: docs/usage.md
---

A package is built from a locked Git baseline. Consumers may have the same or a different commit; POLIS requires an explicit policy for handling that difference.

## Strict — default

```bash
polis preflight --repo /consumer \
  --baseline-mode strict artifact.polis
```

Requires consumer `HEAD` to match the artifact's locked base commit **exactly**. This is the most restrictive mode and the CLI default.

## Compatible — validated descendant

```bash
polis preflight --repo /consumer \
  --baseline-mode compatible artifact.polis
```

Allows a different clean `HEAD` when **descendant ancestry is proven** and all required context, proof, scope, policy, and deterministic target-tree checks pass. It is not automatic conflict resolution.

## Permissive — ancestry may be unproven

```bash
polis preflight --repo /consumer \
  --baseline-mode permissive artifact.polis
```

May attempt admission without descendant ancestry, while still requiring patch, scope, policy, and target-tree validation. Unproven ancestry is reported as a risk. This mode does **not** ignore conflicts.

## Embedded historical proof

Newer formats include an authenticated locked-baseline snapshot so development proofs can be replayed when original Git objects are absent. The permissive mode alone can accept an **explicit waiver** when historical baseline proof is unavailable, with reduced guarantees reported:

```bash
polis preflight --repo /consumer \
  --baseline-mode permissive \
  --allow-missing-baseline-proof artifact.polis
```

This waiver is unavailable in other modes. Using it requires a deliberate decision about the missing assurances.

## Preflight and apply are separate

`preflight` mode is not automatically carried over into `apply`. Repeat the intended mode explicitly in the authorized apply command, which will revalidate the current consumer state.

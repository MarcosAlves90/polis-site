---
slug: sdd-and-tdd
title: SDD and TDD
description: How specifications and Red-to-Green or Green-to-Green proofs structure strict development.
group: Fluxo de entrega
order: 2
source: spec/POLIS-SPEC-v6.md
---

POLIS distinguishes two complementary concerns. **Specification-Driven Development (SDD)** defines the behavioral contract before implementation. **Test-Driven Development (TDD)** supplies observed evidence of the development path.

## Specify first

A strict Change Contract links identifiable requirements to acceptance criteria, implementation and test scopes, and proof commands. Specification identity and the effective policy are locked against the Git baseline before edits.

A useful specification answers:

- What behavior must be introduced or preserved?
- Which files may change?
- What concrete observation demonstrates the required behavior?
- Which conditions should block the delivery?

## Red-to-Green

For strict features and defects, the producer must demonstrate that the relevant test **failed on the baseline** and **passes after the change**. POLIS captures actual Red proof before production edits:

```bash
polis check-red-scope --repo /repo \
  --contract /outside/locked-v6.json \
  --path internal/behavior_test.go

polis capture-red --repo /repo \
  --contract /outside/locked-v6.json \
  --out /outside/regression.patch
```

A failure must match the prescribed command, exit code, and oracle. A missing executable is not regression proof. Captured tests remain immutable and are validated again in later steps.

## Green-to-Green

Strictly behavior-preserving changes use a characterization that **passes on the baseline** and continues passing on the target. There is no reason to manufacture a Red failure.

## Optional Implementation Plan

```bash
polis implementation-plan --repo /repo \
  --policy /outside/policy-v3.json \
  --contract /outside/locked-v6.json \
  --out /outside/implementation-plan.json
```

The plan is derived deterministically from the locked contract and remains subordinate to it. When explicitly packaged, it changes the delivery to **format v6**, adding an authenticated plan member.

## Important limitation

Validation establishes only the observable properties and execution conditions represented by the contract and its proof. It cannot prove an unrecorded implementation chronology or replace security review and semantic correctness checks.

---
slug: change-contracts
title: Change Contract
description: How a contract defines behavior, file scope, required proof, and the locked baseline.
group: Conceitos e segurança
order: 1
source: spec/POLIS-SPEC-v6.md
---

The **Change Contract** is the structured source of obligations for an individual delivery. It makes change limits enforceable and links requirements to acceptance criteria and proof.

## What a strict contract represents

- **Specification:** a versioned description of expected behavior.
- **Requirements and acceptance criteria:** traceable links between intent and acceptance.
- **Change scope:** source paths authorized to change.
- **Test scope:** allowed paths for tests captured as proof.
- **Proof commands:** commands and oracles validating development behavior.
- **Baseline lock:** Git state identity and effective policy digest bound to the locked contract.

## Draft and lock

The newer workflow passes a schema-v5 draft to `polis start`, which produces a **locked schema-v6 Change Contract**. Compatibility with draft schema v3 to locked schema v4 remains available.

```bash
polis start --repo /repo \
  --policy /outside/policy-v3.json \
  --contract /outside/draft-v5.json \
  --out /outside/locked-v6.json
```

The lock must be established on a clean Git baseline **before implementation**. Do not rewrite a locked contract to excuse changes that exceeded scope; establish a new legitimate baseline and lock when requirements change.

## Scope is executable

`scope.allowed_paths` constrains implementation changes. Captured test files must also fall within the designated test scope. Before creating Red tests:

```bash
polis check-red-scope --repo /repo \
  --contract /outside/locked-v6.json \
  --path tests/feature_test.go
```

This accepts paths that **do not yet exist**, since it validates the proposal rather than file contents. The later capture checks the actual test-only delta.

## Optional commit intent

A schema-v5 draft may include a commit message bound into the locked contract and package. It only creates a commit when the consumer explicitly invokes `apply --commit-mode prompt` or `auto`.

## Authoritative schema reference

Contracts have precise serialization, size, validation, and migration rules. **Do not treat a partial UI example as a production contract template.** Refer to the [V6 Specification](https://github.com/MarcosAlves90/polis/blob/main/spec/POLIS-SPEC-v6.md), [versioned schemas](https://github.com/MarcosAlves90/polis/tree/main/spec/schemas), and CLI for valid inputs.

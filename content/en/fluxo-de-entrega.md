---
slug: delivery-workflow
title: Delivery workflow
description: How producers prepare, prove, package, and deliver changes for independent consumer validation.
group: Fluxo de entrega
order: 1
source: docs/usage.md
---

The POLIS lifecycle separates **producing a delivery** from **consumer acceptance**. Consumers must not inherit trust from the producer's machine.

## Step 1 — Prepare the change

Review the expected behavior, authorized scope, tests, Project Policy, and Git baseline. A Change Contract is a versioned and validated document, not a free-form description.

Given a valid strict draft and a clean repository, `start` locks the contract and relevant identities:

```bash
polis start --repo /repo \
  --policy /outside/policy-v3.json \
  --contract /outside/draft-v5.json \
  --out /outside/locked-v6.json
```

A schema-v5 draft becomes a locked schema-v6 contract. The existing schema-v3 to schema-v4 locking flow remains supported.

## Step 2 — Establish development proof

Strict feature and defect changes use **Red-to-Green**. Before modifying the implementation, check the proposed test paths and capture a genuine failure of the required behavior:

```bash
polis check-red-scope --repo /repo \
  --contract /outside/locked-v6.json \
  --path internal/example_test.go

polis capture-red --repo /repo \
  --contract /outside/locked-v6.json \
  --out /outside/regression.patch
```

`capture-red` requires a test-only delta and a failure matching the contract oracle. A `behavior_preserving` change uses Green-to-Green instead; it does not invent a Red failure.

## Step 3 — Implement and validate

Edit only authorized paths and preserve captured tests. Validate the working tree without building a delivery package:

```bash
polis workspace validate --repo /repo \
  --contract /outside/locked-v6.json \
  --policy /outside/policy-v3.json \
  --regression-patch /outside/regression.patch
```

You may generate an optional contract-bound Implementation Plan after `start`. If used, pass the exact same plan bytes to subsequent commands that require them.

## Step 4 — Build and verify the artifact

```bash
polis build --repo /repo \
  --policy /outside/policy-v3.json \
  --project application --change fix-validation \
  --contract /outside/locked-v6.json \
  --regression-patch /outside/regression.patch \
  --out /outside/output

polis verify /outside/output/artifact.polis
polis inspect /outside/output/artifact.polis
```

Confirm the actual output paths and filenames from command output. This example illustrates an unplanned Red-to-Green delivery, not a universal command for every change.

## Step 5 — Consume in a target repository

```bash
polis preflight --repo /consumer /outside/output/artifact.polis

# Only after review and explicit authorization:
polis apply --repo /consumer /outside/output/artifact.polis
```

`preflight` does not apply changes to the consumer; `apply` revalidates before mutation. See [Safe application](../safe-application/) and [Baseline modes](../baseline-modes/).

## Repository isolation

In the canonical workflow, the policy, locked contract, Red proof, package, and signature remain **outside the target worktree**. POLIS also supports explicitly configured retention in `.polis/artifacts/`. See the [official operational guide](https://github.com/MarcosAlves90/polis/blob/main/docs/usage.md#repository-artifact-retention).

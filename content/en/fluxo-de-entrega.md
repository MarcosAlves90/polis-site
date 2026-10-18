---
slug: delivery-workflow
title: Delivery workflow
description: Shared contracts and proof for POLIS 6.12.0 local and remote workflows.
group: Fluxo de entrega
order: 1
source: docs/quickstart.md
---

POLIS supports **two workflows**. Agents already editing the target checkout can use `workspace validate` to save an external report without a package. A different consumer checkout needs an external `.polis` package independently checked before acceptance. See [Local workspace validation](../local-workspace-validation/) and [Remote delivery](../remote-delivery/).

## Which workflow does your AI need?

| Scenario | Producer's final step | Handoff |
| --- | --- | --- |
| Local AI agent working in the user's checkout | `polis workspace validate` after contract and proof | Optional external checkpoint; **no `.polis` delivery package**. |
| Web chatbot/AI delivering to another checkout | An actual producer with checkout, Git, and CLI access runs `polis build` and `polis verify` | **External `.polis` file**; the consumer runs `preflight` and authorized `apply`. |

The chat interface itself does not change these rules. Without source access and actual CLI execution, a chatbot can guide you **but cannot build or attest a package**. Also distinguish the delivery file `change.polis` from the `.polis/` configuration folder and `.polis/policy.json`; an external policy can be passed through `--policy`.

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

## Step 3 — Implement and choose the destination

Edit only authorized paths and preserve captured tests. **If this is the checkout under review**, validate locally without producing a delivery package:

```bash
polis workspace validate --repo /repo \
  --contract /outside/locked-v6.json \
  --policy /outside/policy-v3.json \
  --regression-patch /outside/regression.patch \
  --out-report /outside/workspace-validation.json
```

This completes the **local** validation path; its report is not a transferable package. You may generate an optional contract-bound Implementation Plan after `start`. If used, pass the exact same plan bytes to subsequent commands that require them.

## Step 4 — Only for another checkout: build and verify the artifact

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

`--out` must resolve to a directory **physically outside** the producer repository. The package is disposable and is never retained under `.polis/artifacts/packages/`. Read the actual generated filename from command output; `artifact.polis` is illustrative. This Red-to-Green example is not required for local validation.

## Step 5 — Remote delivery only: consume in another repository

```bash
polis preflight --repo /consumer /outside/output/artifact.polis

# Only after review and explicit authorization:
polis apply --repo /consumer /outside/output/artifact.polis
```

`preflight` does not apply changes to the consumer; `apply` revalidates before mutation. See [Safe application](../safe-application/) and [Baseline modes](../baseline-modes/).

## Repository isolation

Policy, locked contract, Red proof, workspace report, package, and signature belong **outside the worktree** in the recommended workflow. Optional `.polis/artifacts/` retention covers selected records, contracts and evidence, **never new delivery packages**. See the [official retention reference](https://github.com/MarcosAlves90/polis/blob/main/docs/retention.md).

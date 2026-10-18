---
slug: local-workspace-validation
title: Local workspace validation
description: Validate changes in the agent's checkout without creating a delivery package.
group: Fluxo de entrega
order: 3
source: docs/workflows/local-agent-workspace.md
---

**Running an AI coding agent on your computer, editing that same repository? This is the recommended path.** The agent needs access to the checkout, POLIS CLI, Git, and the tools required by project gates. POLIS locks the contract, checks required proof, and runs the policy gates on the local change. **`workspace validate` neither creates nor verifies a delivery `.polis` file.** Do not run `build`, `preflight`, or `apply` merely to validate the same checkout.

Even if the conversation started in a web chat, when an agent with checkout access implements and validates **there**, this local workflow applies. Use [Remote delivery](../remote-delivery/) only if the change must cross to another checkout as a package.

## Prepare external inputs

Start from a clean committed Git baseline. Keep external policy, contract, optional plan, Red proof, and report **outside the repository**. If the project uses `.polis/policy.json`, that is policy configuration, not a delivery package.

The `.polis/` folder may also hold `.polis/policy-provenance.json`. Neither file is a `change.polis` delivery package, which belongs to **the other workflow**. Here, `polis init --dry-run` creates the JSON policy outside the checkout; later commands use the **same file** through `--policy`.

```bash
polis doctor
POLIS_OUTSIDE="${POLIS_OUTSIDE:-$(mktemp -d)}"
mkdir -p "$POLIS_OUTSIDE"
polis init --repo . --profile auto --dry-run > "$POLIS_OUTSIDE/policy.json"
polis doctor --repo . --policy "$POLIS_OUTSIDE/policy.json"
polis plan --repo . --policy "$POLIS_OUTSIDE/policy.json"
```

`POLIS_OUTSIDE` must resolve physically outside the checkout. Prepare a valid schema-v5 Change Contract draft for the actual change and lock it **before modifying production code**:

```bash
polis start --repo . --policy "$POLIS_OUTSIDE/policy.json" \
  --contract "$POLIS_OUTSIDE/draft-v5.json" \
  --out "$POLIS_OUTSIDE/locked-v6.json"
```

## Prove and validate

For Red-to-Green changes, add only the scoped failing test first. Check its path and capture proof before implementation:

```bash
polis check-red-scope --repo . \
  --contract "$POLIS_OUTSIDE/locked-v6.json" --path path/to/regression_test.go
polis capture-red --repo . --contract "$POLIS_OUTSIDE/locked-v6.json" \
  --out "$POLIS_OUTSIDE/regression.patch"
```

After implementing, validate with the identical policy and locked contract bytes:

```bash
polis workspace validate --repo . --policy "$POLIS_OUTSIDE/policy.json" \
  --contract "$POLIS_OUTSIDE/locked-v6.json" \
  --regression-patch "$POLIS_OUTSIDE/regression.patch" \
  --out-report "$POLIS_OUTSIDE/workspace-validation.json" --format json
```

Omit `--regression-patch` for a valid Green-to-Green characterization. If using an Implementation Plan, supply the same bytes to the operations that require it. Successful validation reports `workspace_validated: true`, while `delivery_artifact_built` and `delivery_artifact_verified` are false.

The `workspace-validation.json` report is an **external checkpoint**, not a transferable package, a signature, or producer authentication. The successful result refers to that validated state, not subsequent changes.

## Resume from a checkpoint

```bash
polis status --repo . --policy "$POLIS_OUTSIDE/policy.json" \
  --contract "$POLIS_OUTSIDE/locked-v6.json" \
  --regression-patch "$POLIS_OUTSIDE/regression.patch" \
  --report "$POLIS_OUTSIDE/workspace-validation.json" --format json
```

`status` compares evidence and identities. A saved report does not prove that subsequent source changes were validated; rerun `workspace validate` for current evidence. See the [official local workflow](https://github.com/MarcosAlves90/polis/blob/main/docs/workflows/local-agent-workspace.md) for complete prerequisites and [remote handoff](../remote-delivery/) for delivery to a different checkout.

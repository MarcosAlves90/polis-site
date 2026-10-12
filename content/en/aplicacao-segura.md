---
slug: safe-application
title: Safe application
description: Understand consumer preflight, apply revalidation, and explicitly authorized local commit modes.
group: Fluxo de entrega
order: 5
source: docs/usage.md
---

Consumers must verify a delivery against **their own current Git state and environment**. A producer PASS or past preflight PASS is not permanent authorization to modify files.

## 1. Verify the package

```bash
polis verify artifact.polis
polis inspect artifact.polis
```

Review the scope, patch contents, and configured policy commands. Such commands may have external effects. Worktree isolation is not a security sandbox for untrusted code.

## 2. Run preflight

```bash
polis preflight --repo /target /outside/artifact.polis
```

`preflight` verifies the package, baseline admission, isolated target, development proof, and applicable gates—including those deferred by the producer. It **does not apply the patch to the consumer**.

If the repository changes afterwards, that earlier PASS cannot establish that application is still safe.

## 3. Apply only after authorization

```bash
polis apply --repo /target /outside/artifact.polis
```

`apply` repeats validation before changing files and verifies target-tree identity after application. In canonical apply-only mode, it preserves HEAD and the real Git index. Transactional checks and rollback exist for failures, but operators must investigate errors and verify reported recovery state.

## Commit modes

The default is `--commit-mode none`: apply content without a commit. When the artifact contains valid commit intent, two explicit options are available:

```bash
# Requires interactive terminal and approval:
polis apply --repo /target --commit-mode prompt /outside/artifact.polis

# Explicitly authorizes a local commit without prompting:
polis apply --repo /target --commit-mode auto /outside/artifact.polis
```

`auto` is **explicit local authorization**, not a workaround for an agent without a terminal. Neither mode automatically runs `git push`, signs a commit, or publishes a release.

## Different baselines

The default `--baseline-mode strict` requires exact locked base commit equality. `compatible` admits proven clean descendants after full validation. `permissive` permits a broader attempt with warnings, without ignoring real conflicts. Read [Baseline modes](../baseline-modes/) before relaxing the default.

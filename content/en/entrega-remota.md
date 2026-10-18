---
slug: remote-delivery
title: Remote delivery between checkouts
description: Produce and transfer a disposable .polis package for another consumer checkout.
group: Fluxo de entrega
order: 4
source: docs/workflows/web-agent-delivery.md
---

Use this workflow when a web agent, CI job, or developer must deliver a change **to another checkout**. The producer needs actual access to the source repository, Git, and a POLIS runtime. Chat text alone does not establish that a package was built or verified.

**Using a web chatbot or AI?** It can help describe changes and prepare files or instructions. But without repository access and the ability to run Git and POLIS, it **cannot produce or verify a package itself**. An authorized developer, tool-equipped web agent, or CI job must run the commands in the producer checkout. This workflow uses a `.polis` file **because delivery crosses checkouts**, not simply because AI runs in a browser.

## Producer: external disposable package

Start from a clean committed baseline. Keep policy, contract, proof, signature, and package outside the worktree. `polis build` rejects output paths that resolve inside the repository; retention does not copy new packages into `.polis/artifacts/packages/`.

The `change.polis` file is the **transferable build output**. The `.polis/` directory may exist inside the repository for configuration/evidence, including `.polis/policy.json` and `.polis/policy-provenance.json`. In this example `/outside/policy.json` is an **external policy**. None of these policy files is the delivery package.

After preparing and locking contracts and capturing the appropriate proof as described in [Delivery workflow](../delivery-workflow/), run:

```bash
polis build --repo /producer --policy /outside/policy.json \
  --project project-slug --change change-slug \
  --contract /outside/locked-v6.json \
  --regression-patch /outside/regression.patch \
  --out /outside/packages
```

For Green-to-Green work, omit `--regression-patch` and supply the required characterization proof. `build` reports the actual package path and filename; replace the illustrative filename below with the **reported path** rather than assuming its name:

```bash
PACKAGE=/outside/packages/filename-reported-by-build.polis
polis verify "$PACKAGE"
polis inspect "$PACKAGE"
```

As of `v6.12.0`, the producer validates the final output's file identity and SHA-256 before success. Another process with filesystem access can still relocate the output after the final check; verify the actual transferred bytes on the consumer side. An optional Ed25519 signature establishes origin only against an independently trusted public key.

## Consumer: review and authorization

```bash
polis verify /outside/received/change.polis
polis preflight --repo /consumer /outside/received/change.polis
# Only after review and authorization:
polis apply --repo /consumer /outside/received/change.polis
```

`preflight` is read-only and does not grant permission to `apply`. Consumers choose their target repository and trust policy. Once no longer needed for transfer or audit, the owner may delete the external package; POLIS does not delete it automatically.

The `.polis` delivery package is different from the offline runtime ZIP produced by `polis export`. See the [official remote delivery guide](https://github.com/MarcosAlves90/polis/blob/main/docs/workflows/web-agent-delivery.md) and [local validation](../local-workspace-validation/) if the agent already edits the target checkout.

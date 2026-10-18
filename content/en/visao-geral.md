---
slug: overview
title: Overview
description: Learn what POLIS is, who it is for, and what it means to deliver changes backed by evidence.
group: Comece aqui
order: 1
source: README.md
---

POLIS is a **Go CLI and a software-change delivery protocol**. It brings together behavioral specifications, change boundaries, tests, validation, and artifact integrity into a verifiable process.

Designed for AI-assisted engineering, its mechanisms also work for human-led delivery. It is **not** an AI model, code generator, or cloud service: it **validates local changes and, when transfer is needed, packages and controls their acceptance**.

## The problem it addresses

A change may work on the producer's machine and still be incompatible with its destination repository. It can also be difficult to answer basic questions: which requirements does the change satisfy, which tests ran, which files were allowed to change, and what is the exact identity of the resulting tree?

POLIS makes these questions auditable through contracts, development proof, and project policies. An agent editing the target checkout can run `workspace validate` without creating a package; delivery to another checkout adds independent producer and consumer validation.

## Three foundations

1. **Explicit scope.** The Change Contract defines authorized changes, acceptance criteria, and mandatory proof.
2. **Verifiable evidence.** Local validation creates an externally saved checkpoint tied to observed state; remote delivery uses a `.polis` package whose exact bytes can be verified independently.
3. **Deliberate application.** When there is a consumer, it runs `preflight` before `apply`; `apply` repeats validation against current state and requires authorization.

## What POLIS does not promise

- It does not replace human review or guarantee the absence of defects or vulnerabilities.
- It does not sandbox arbitrary project commands; those commands may still interact with external systems.
- A passing test is not universal proof that the software is correct.
- Artifact integrity does not establish producer authenticity: that requires a detached signature and independently trusted consumer-supplied key.
- `apply` does not implicitly push commits or publish releases.

## Roles and responsibilities

| Role | Responsibility | Examples |
| --- | --- | --- |
| Local agent | Specify, prove, and validate changes in the same checkout | `start`, `capture-red`, `workspace validate` |
| Remote producer | Build a disposable package for another checkout | `build`, `verify` |
| Reader | Verify and inspect an artifact | `verify`, `inspect` |
| Consumer | Validate against its own state and apply when authorized | `preflight`, `apply` |

## Where to begin

Start with [Installation](../installation/) and [Quickstart](../quickstart/). Choose [Local workspace validation](../local-workspace-validation/) or [Remote delivery](../remote-delivery/) based on whether the change crosses checkouts. [Delivery workflow](../delivery-workflow/) explains the shared contracts and proof requirements.

The [V6 Specification](https://github.com/MarcosAlves90/polis/blob/main/spec/POLIS-SPEC-v6.md) governs machine contracts. The [official usage index](https://github.com/MarcosAlves90/polis/blob/main/docs/usage.md) links to the [command reference](https://github.com/MarcosAlves90/polis/blob/main/docs/commands.md) and focused operational guides.

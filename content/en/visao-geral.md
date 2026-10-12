---
slug: overview
title: Overview
description: Learn what POLIS is, who it is for, and what it means to deliver changes backed by evidence.
group: Comece aqui
order: 1
source: README.md
---

POLIS is a **Go CLI and a software-change delivery protocol**. It brings together behavioral specifications, change boundaries, tests, validation, and artifact integrity into a verifiable process.

Designed for AI-assisted engineering, its mechanisms also work for human-led delivery. It is **not** an AI model, code generator, or cloud service: its role is to **validate, package, and control the acceptance of changes**.

## The problem it addresses

A change may work on the producer's machine and still be incompatible with its destination repository. It can also be difficult to answer basic questions: which requirements does the change satisfy, which tests ran, which files were allowed to change, and what is the exact identity of the resulting tree?

POLIS makes these questions auditable through contracts, development proof, project policies, and validation performed both by the producer and the consumer.

## Three foundations

1. **Explicit scope.** The Change Contract defines authorized changes, acceptance criteria, and mandatory proof.
2. **Verifiable evidence.** The producer creates a `.polis` package carrying validation information, identity, and traceability; its exact bytes can be checked independently.
3. **Deliberate application.** The consumer runs `preflight` before `apply`; `apply` repeats validation against the current state and requires authorization.

## What POLIS does not promise

- It does not replace human review or guarantee the absence of defects or vulnerabilities.
- It does not sandbox arbitrary project commands; those commands may still interact with external systems.
- A passing test is not universal proof that the software is correct.
- Artifact integrity does not establish producer authenticity: that requires a detached signature and independently trusted consumer-supplied key.
- `apply` does not implicitly push commits or publish releases.

## Roles and responsibilities

| Role | Responsibility | Examples |
| --- | --- | --- |
| Producer | Specify, prove, implement, and package | `start`, `capture-red`, `build` |
| Reader | Verify and inspect an artifact | `verify`, `inspect` |
| Consumer | Validate against its own state and apply when authorized | `preflight`, `apply` |

## Where to begin

Start with [Installation](../installation/) and [Quickstart](../quickstart/). For the complete lifecycle, read [Delivery workflow](../delivery-workflow/).

The [V6 Specification](https://github.com/MarcosAlves90/polis/blob/main/spec/POLIS-SPEC-v6.md) governs machine contracts. The [official usage guide](https://github.com/MarcosAlves90/polis/blob/main/docs/usage.md) provides the complete operational command reference.

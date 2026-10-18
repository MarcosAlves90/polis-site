---
slug: core-concepts
title: Core concepts
description: A glossary of the main POLIS objects, responsibilities, and result states.
group: Comece aqui
order: 4
source: spec/POLIS-SPEC-v6.md
---

Before validating a checkout or packaging a change for another consumer, distinguish the core objects of the protocol.

## Glossary

| Concept | Meaning |
| --- | --- |
| **Specification** | Defines expected behavior, requirements, and acceptance criteria. |
| **Project Policy** | Defines applicable project commands and quality gates. |
| **Change Contract** | Defines behavior, change scope, tests, proof requirements, and baseline identity. |
| **Locked baseline** | Git state and policy associated with a contract locked by `polis start`. |
| **Red-to-Green** | Observed proof of a relevant baseline failure followed by success after implementation. |
| **Green-to-Green** | Characterization that passes both before and after a behavior-preserving change. |
| **Evidence** | Bounded structured records of commands, proof, and validation decisions. |
| **Gate** | A policy-configured check with explicit prerequisites and outcomes. |
| **Workspace checkpoint** | Externally saved local validation report tied to observed identities, without a delivery package. |
| **`.polis`** | A verifiable delivery package, distinct from the offline runtime bundle. |
| **Preflight** | Validation against the consumer environment without applying a change. |

## PASS, FAIL, and BLOCKED are different

**PASS** means an applicable check was completed successfully. **FAIL** indicates a validation failure actually observed. **BLOCKED** means prerequisites or environment prevented the intended validation from running. A test that never ran cannot count as Red proof.

## Integrity versus authenticity

Hashes and checksums detect changes to package bytes. To associate those bytes with a trusted producer, the consumer must verify a detached signature against an **independently supplied trusted public key**. See [Security and trust](../security/).

## Who defines what?

The Engineering Guide defines process. The V6 Specification defines machine-level contracts. The Go CLI implements the protocol. See [Architecture](../architecture/) for details.

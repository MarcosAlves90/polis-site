---
slug: artifacts-and-verification
title: Artifacts and verification
description: Understand .polis packages, V6 formats, inspection, and detached digital signatures.
group: Fluxo de entrega
order: 4
source: spec/POLIS-SPEC-v6.md
---

A `.polis` file is the output of a validated delivery. It packages the change, contracts, and evidence required for verification and consumption within the specification's schemas and size limits.

## Build a delivery package

The producer uses `polis build` only after locking a baseline and satisfying mandatory development proof. Then check the resulting artifact independently:

```bash
polis verify /outside/output/artifact.polis
polis inspect --format json /outside/output/artifact.polis
```

`verify` checks package bytes, required members, checksums, schemas, and supported proof consistency. `inspect` exposes validated metadata without applying the change.

## Package formats in POLIS V6

| Produced artifact | Package format | Key property |
| --- | --- | --- |
| Delivery without explicit plan | `format v5` | Eight canonical members, including the embedded baseline. |
| Delivery with an Implementation Plan | `format v6` | Nine members; the plan is bound to the package and its evidence. |

**POLIS V6** names the protocol and CLI generation. It does **not** mean every new package necessarily uses format 6. The presence of an Implementation Plan selects the package format. Supported historical formats remain readable under their compatibility rules.

## Checksums do not identify producers

A checksum validates a relationship between bytes and digest, but does not prove who created them. Optional authenticity uses an **Ed25519 detached signature** verified using a consumer-supplied, independently trusted public key.

```bash
polis sign --key private.pem \
  --out artifact.polis.sig artifact.polis

polis verify \
  --signature artifact.polis.sig \
  --trusted-key public.pem \
  artifact.polis
```

Protect the private key. Consumers must not simply trust a public key selected by the package itself.

## Plans and traceability

With an Implementation Plan, `inspect` can report relationships between requirements, acceptance criteria, implementation steps, and proof. Plan presence never replaces execution of required validation.

## Reading is not applying

`verify` and `inspect` operate on the artifact alone. To determine whether it can safely be used against **a specific target repository**, run consumer [preflight](../safe-application/) before authorized application.

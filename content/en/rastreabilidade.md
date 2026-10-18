---
slug: traceability
title: Traceability and evidence
description: Connect requirements, plans, and proof without mistaking metadata for observed execution.
group: Conceitos e segurança
order: 5
source: spec/POLIS-SPEC-v6.md
---

POLIS evidence describes **what ran, against which identities, and with what results**. It makes deliveries auditable without persisting arbitrary full command-output dumps in the package.

## Traceability chain

A strict change connects:

1. Identifiable requirements in the Specification.
2. Acceptance criteria linked to those requirements.
3. Development proof and gates prescribed by the contract and policy.
4. An identified Git target tree and a workspace checkpoint, or a verifiable package when handing off to another checkout.

With an optional Implementation Plan, test and implementation steps link to requirements and acceptance criteria; the plan becomes part of a format-v6 package.

## What evidence records

Structured evidence includes command identity, exit code, duration, SHA-256 digests, byte counts, truncation flags, and declared environment metadata. It **does not persist complete raw stdout/stderr streams** as proof.

This limits size and potentially sensitive output exposure, but means full execution logs cannot necessarily be reconstructed from the package alone.

## Historical records are not current validation

`polis gates` run manifests and workspace checkpoints help resume work, but an old report cannot substitute for validation of changed source. Input and declared environment identities must be re-evaluated.

`polis status` uses `proven`, `stale_or_unproven`, and `missing` to distinguish verified evidence from historical or absent information. The `source`/`reason` provenance in `polis plan` JSON v4 explains policy, dependency, and guarantee decisions; it is not an authorship signature.

## Inspect traceability

```bash
polis inspect --format json artifact.polis
polis status --repo /repo --package /outside/artifact.polis
```

Available fields depend on artifact format and supplied inputs. See the [V6 Specification](https://github.com/MarcosAlves90/polis/blob/main/spec/POLIS-SPEC-v6.md) for normative record semantics.

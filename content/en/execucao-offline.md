---
slug: offline-runtime
title: Offline runtime
description: Distribute POLIS to agents and machines without installing Go or requiring network access.
group: Fluxo de entrega
order: 8
source: spec/POLIS-OFFLINE.md
---

POLIS V6 offers a **platform-specific portable offline runtime**. The ZIP contains the native executable, specification, JSON schemas, manifest, and supporting files needed by the CLI. It is distinct from a `.polis` code-change delivery package.

## Download an offline bundle

Choose the ZIP matching your operating system and architecture from [official releases](https://github.com/MarcosAlves90/polis/releases/latest):

```text
polis-<tag>-offline-<GOOS>-<GOARCH>.zip
```

After extraction, run `bin/polis` on Unix-like systems or `bin/polis.exe` on Windows. **Go is not required** to run the included binary.

## Dependencies and limits

- Git must be installed and available on `PATH`.
- The executable must match the host operating system and CPU architecture.
- Project Policy commands may still require project-specific compilers, runtimes, network access, or tooling.
- The bundle **does not include a target repository or its Project Policy**.

## Export a local bundle

From an installed POLIS CLI:

```bash
polis export --out /outside/polis-v6-offline.zip
```

Export produces a deterministic ZIP with a manifest and checksums, without reading target repository data. `--executable` and `--runtime` let release tooling include externally built target binaries without executing them on the exporting host.

## Using the kit with agents

Give an offline agent the appropriate bundle and only the contracts and artifacts it is **explicitly authorized** to access. The agent still needs the project's policy and clear boundaries between read-only checks, validation, and mutation.

Consult the [offline runtime specification](https://github.com/MarcosAlves90/polis/blob/main/spec/POLIS-OFFLINE.md) before distribution.

---
slug: installation
title: Installation
description: Install POLIS V6 using Go, or download the offline kit for your platform.
group: Comece aqui
order: 2
source: docs/installation.md
---

The recommended installation requires **Go 1.23 or newer** and **Git**. These instructions follow the official installation guide.

## Prerequisites

Make sure both executables are available:

```bash
go version
git --version
```

## Install with Go

On Linux, macOS, or Windows:

```bash
go install github.com/MarcosAlves90/polis/v6/cmd/polis@latest
polis help
polis doctor
```

For a reproducible installation, replace `@latest` with a specific V6 module tag:

```bash
go install github.com/MarcosAlves90/polis/v6/cmd/polis@v6.11.1
```

> This version was documented in the README consulted for this site. It is not a claim that this tag will always be the newest release; check GitHub Releases.

## Configure PATH

Go installs binaries into `GOBIN`, or into `GOPATH/bin` if `GOBIN` is unset. If the terminal cannot find `polis`, add that directory to `PATH`.

Linux or macOS:

```bash
go env GOBIN
go env GOPATH
```

Windows PowerShell:

```powershell
$goBin = (go env GOBIN).Trim()
if (-not $goBin) { $goBin = Join-Path ((go env GOPATH).Trim()) 'bin' }
$env:Path = "$env:Path;$goBin"
polis doctor
```

See the [official platform-specific installation guide](https://github.com/MarcosAlves90/polis/blob/main/docs/installation.md) to persist the PATH setting.

## Install from source

To develop POLIS or use an explicitly checked-out revision:

```bash
git clone https://github.com/MarcosAlves90/polis.git
cd polis
go install ./cmd/polis
polis doctor
```

## Alternative: offline runtime

The offline kit does **not require Go to execute POLIS**. Download `polis-<tag>-offline-<GOOS>-<GOARCH>.zip` for your OS and architecture from [GitHub Releases](https://github.com/MarcosAlves90/polis/releases/latest), extract it, then run `bin/polis` or `bin/polis.exe`.

Git is still required, and project-specific validation commands may require other tools. See [Offline runtime](../offline-runtime/).

## Confirm the installation

```bash
polis help
polis doctor
```

A `BLOCKED` diagnostic indicates that a required condition prevented operation. Fix the reported prerequisite or environment issue rather than treating it as a passed test.

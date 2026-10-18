---
title: Instalação
description: Instale o POLIS V6 com Go ou use o pacote offline adequado à sua plataforma.
group: Comece aqui
order: 2
source: docs/installation.md
---

A forma recomendada de instalar o POLIS é com **Go 1.23 ou superior** e **Git**. As instruções abaixo são baseadas no guia oficial de instalação do projeto.

## Pré-requisitos

Confirme que os executáveis estão disponíveis:

```bash
go version
git --version
```

## Instalar com Go

Em Linux, macOS ou Windows, execute:

```bash
go install github.com/MarcosAlves90/polis/v6/cmd/polis@latest
polis help
polis doctor
```

Para instalar uma versão fixa e reproduzível, substitua `@latest` por uma tag do módulo V6:

```bash
go install github.com/MarcosAlves90/polis/v6/cmd/polis@v6.12.0
```

> `v6.12.0` é a release estável confirmada em 18 de outubro de 2026. Para versões posteriores, consulte [GitHub Releases](https://github.com/MarcosAlves90/polis/releases/latest).

## Configurar o PATH

Go instala binários em `GOBIN`, ou no diretório `bin` de `GOPATH` quando `GOBIN` não está definido. Caso o terminal não reconheça `polis`, inclua esse caminho no `PATH`.

Linux ou macOS:

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

Para instruções de persistência do `PATH`, consulte o [guia oficial por plataforma](https://github.com/MarcosAlves90/polis/blob/main/docs/installation.md).

## Instalar de um checkout

Para desenvolver o próprio POLIS ou utilizar a revisão clonada:

```bash
git clone https://github.com/MarcosAlves90/polis.git
cd polis
go install ./cmd/polis
polis doctor
```

## Alternativa: runtime offline

O kit offline não exige Go para **executar o POLIS**. Baixe o arquivo `polis-<tag>-offline-<GOOS>-<GOARCH>.zip` correspondente ao seu sistema e arquitetura em [GitHub Releases](https://github.com/MarcosAlves90/polis/releases/latest), extraia e execute `bin/polis` ou `bin/polis.exe`. A distribuição inclui variantes Linux amd64 e Windows amd64, além da plataforma nativa de publicação.

Ele ainda exige Git, e os comandos próprios do projeto que você validar podem exigir outras ferramentas. Consulte [Execução offline](../execucao-offline/).

## Verificar a instalação

```bash
polis help
polis doctor
```

O diagnóstico `BLOCKED` significa que uma condição necessária impediu a operação. Resolva a dependência ou o ambiente reportado, em vez de tratá-lo como um teste aprovado.

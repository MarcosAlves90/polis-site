---
title: Primeiros passos
description: Um caminho inicial para instalar, diagnosticar e inspecionar a validação de um repositório.
group: Comece aqui
order: 3
source: docs/usage.md
---

Este tutorial apresenta os comandos iniciais e distingue **inspeção de configuração** de **entrega verificada**. Uma execução bem-sucedida de `plan` ou `gates` não significa que um pacote `.polis` tenha sido criado.

## 1. Instale e diagnostique

```bash
go install github.com/MarcosAlves90/polis/v6/cmd/polis@latest
polis doctor
```

O comando `doctor` verifica os pré-requisitos da CLI. Consulte [Instalação](../instalacao/) caso o binário não esteja no `PATH`.

## 2. Escolha um repositório Git

Use um repositório que você possa inspecionar. O POLIS identifica o estado do Git e a política que governa os comandos de validação.

```bash
cd /caminho/do/seu-projeto
git status --short
```

Não descarte alterações locais para satisfazer a CLI. O fluxo de bloqueio do POLIS existe justamente para impedir que um estado ambíguo seja aceito silenciosamente.

## 3. Inspecione a política sem escrever arquivos

Em um módulo Go raiz, o perfil automático pode gerar uma política adequada ao ambiente. Para visualizar sua geração sem persistir arquivos:

```bash
polis init --repo . --profile auto --dry-run
```

A detecção automática do perfil `auto` reconhece módulos Go na raiz. Para outros ecossistemas, o perfil `custom` exige configuração explícita dos comandos.

Se você optar por criar a política no repositório, execute `init` sem `--dry-run` e **revise o resultado antes de versioná-lo**:

```bash
polis init --repo . --profile auto
```

## 4. Veja o plano de validação

```bash
polis plan --repo .
```

`plan` é somente leitura: apresenta os gates habilitados, dependências, comandos e garantias ou limitações da política efetiva. Para executá-los localmente:

```bash
polis gates --repo .
```

> `gates` valida comandos do projeto, mas não cria nem verifica artefatos de entrega. Para isso, é necessário passar pelo contrato bloqueado, pelas provas exigidas e por `build` + `verify`.

## 5. Avance para uma entrega

Uma entrega completa exige especificação de comportamento, Change Contract, escopo autorizado e estratégia de prova. Esses arquivos têm esquemas e pré-condições definidos na especificação; não devem ser improvisados a partir de um trecho isolado.

Siga o [Fluxo de entrega](../fluxo-de-entrega/) e depois [SDD e TDD](../sdd-tdd/). Os exemplos de CLI dessa documentação são **modelos de sintaxe**, não substituem contratos reais válidos.

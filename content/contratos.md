---
title: Change Contract
description: Como um contrato define o comportamento, os limites da mudança, as provas e a linha de base bloqueada.
group: Conceitos e segurança
order: 1
source: spec/POLIS-SPEC-v6.md
---

O **Change Contract** é a fonte estruturada das obrigações de uma entrega específica. Ele torna os limites da mudança verificáveis e liga requisitos a critérios de aceite e provas.

## O que um contrato estrito representa

- **Specification:** descrição versionada do comportamento esperado.
- **Requirements e acceptance criteria:** a relação rastreável entre intenção e aceitação.
- **Change scope:** conjunto de caminhos de código que podem mudar.
- **Test scope:** caminhos autorizados para testes que serão capturados como prova.
- **Proof commands:** comandos e oráculos que validam o desenvolvimento.
- **Baseline lock:** identidade do estado Git e hash da política efetiva vinculada ao contrato bloqueado.

## Rascunho e bloqueio

No fluxo novo, um contrato rascunho de schema v5 é usado com `polis start`, que produz um contrato **bloqueado schema v6**. A compatibilidade com draft schema v3 → locked schema v4 é preservada.

```bash
polis start --repo /repo \
  --policy /outside/policy-v3.json \
  --contract /outside/draft-v5.json \
  --out /outside/locked-v6.json
```

O bloqueio precisa ocorrer sobre uma base Git limpa antes de implementar a mudança. Não reescreva um contrato bloqueado para acomodar uma implementação divergente; quando o contrato muda, é necessário estabelecer novo bloqueio de forma legítima.

## Escopo é uma restrição executável

`scope.allowed_paths` delimita alterações de implementação. Os arquivos dos testes também devem pertencer ao escopo de testes permitido. Antes de criar testes Red:

```bash
polis check-red-scope --repo /repo \
  --contract /outside/locked-v6.json \
  --path tests/feature_test.go
```

O comando aceita caminhos que **ainda não existem**, pois valida a proposta, não o conteúdo de um arquivo. A captura posterior verifica o delta de testes real.

## Intenção de commit é opcional

O rascunho schema v5 pode incluir uma mensagem de commit que se torna parte do contrato bloqueado e do pacote. Ela só produz commit quando o consumidor invoca explicitamente `apply` com `--commit-mode prompt` ou `auto`.

## Schema: onde buscar a verdade

O contrato possui regras de serialização, limites, validações e migração detalhados. **Não use um exemplo parcial de interface como template de produção.** Consulte a [Specification V6](https://github.com/MarcosAlves90/polis/blob/main/spec/POLIS-SPEC-v6.md), os [schemas versionados](https://github.com/MarcosAlves90/polis/tree/main/spec/schemas) e a CLI para criar arquivos válidos.

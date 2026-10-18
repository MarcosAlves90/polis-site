---
title: Rastreabilidade e evidências
description: Como requisitos, planos e provas se relacionam sem confundir metadados com execução demonstrada.
group: Conceitos e segurança
order: 5
source: spec/POLIS-SPEC-v6.md
---

A evidência do POLIS documenta **o que foi executado, sob quais identidades e com qual resultado**. Ela serve para tornar uma entrega auditável sem carregar dumps arbitrários de saída de comandos no pacote.

## Cadeia de rastreabilidade

Uma mudança estrita conecta:

1. Requisitos identificados na Specification.
2. Critérios de aceite vinculados a esses requisitos.
3. Provas de desenvolvimento e gates definidos pelo contrato e política.
4. Um alvo Git identificado e um checkpoint do workspace, ou um pacote verificável se houver entrega remota.

Quando há Implementation Plan opcional, etapas de testes e implementação são relacionadas aos requisitos e critérios, e o plano se torna parte do artefato formato v6.

## O que a evidência guarda

O protocolo usa registros estruturados com dados como identidade do comando, código de saída, duração, digest SHA-256, contagem de bytes, estado de truncamento e metadados declarados de ambiente. **Não armazena o fluxo bruto completo de stdout/stderr** como prova persistida.

Isso ajuda a limitar tamanho e exposição de dados, mas significa que uma pessoa não recupera a íntegra de todos os logs apenas a partir do pacote.

## Registros históricos não são estado atual

Manifestos de `polis gates` e checkpoints do workspace podem ajudar a retomar trabalho, mas um relatório histórico não substitui a validação de um alvo que mudou. A identidade das entradas e do ambiente precisa ser reavaliada.

`polis status` identifica estados `proven`, `stale_or_unproven` e `missing` para diferenciar prova verificada de informação histórica ou ausente. Em `polis plan`, a proveniência `source`/`reason` do JSON v4 explica decisões de política, dependências e garantias; não é uma assinatura de autoria.

## Consultar a rastreabilidade

```bash
polis inspect --format json artifact.polis
polis status --repo /repo --package /outside/artifact.polis
```

Os campos disponíveis dependem do formato do pacote e das entradas fornecidas. Para a semântica exata de cada registro, consulte a [Specification V6](https://github.com/MarcosAlves90/polis/blob/main/spec/POLIS-SPEC-v6.md).

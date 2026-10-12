---
title: Fluxo de entrega
description: Como o produtor prepara, prova, empacota e entrega mudanças para um consumidor independente.
group: Fluxo de entrega
order: 1
source: docs/usage.md
---

O ciclo do POLIS é intencionalmente dividido em **produção de uma entrega** e **aceitação pelo consumidor**. O consumidor não deve herdar confiança do ambiente do produtor.

## Etapa 1 — Preparar a mudança

Revise comportamento esperado, escopo autorizado, testes, política do projeto e linha de base Git. O Change Contract é um documento versionado e validado, não apenas uma descrição livre.

Com um rascunho estrito válido e um repositório limpo, `start` bloqueia o contrato e as identidades relevantes:

```bash
polis start --repo /repo \
  --policy /outside/policy-v3.json \
  --contract /outside/draft-v5.json \
  --out /outside/locked-v6.json
```

Um rascunho schema v5 é bloqueado em schema v6. O projeto também preserva a compatibilidade de entrada com o fluxo schema v3 → v4.

## Etapa 2 — Estabelecer a prova

Para funcionalidades e defeitos estritos, o fluxo é **Red-to-Green**. Antes de alterar a implementação, verifique os caminhos permitidos para testes e capture uma falha real do comportamento exigido:

```bash
polis check-red-scope --repo /repo \
  --contract /outside/locked-v6.json \
  --path internal/example_test.go

polis capture-red --repo /repo \
  --contract /outside/locked-v6.json \
  --out /outside/regression.patch
```

`capture-red` requer um delta que altere somente os testes e uma falha que corresponda ao oráculo definido no contrato. Mudanças `behavior_preserving` usam Green-to-Green; não fabricam uma falha para atender a um ritual.

## Etapa 3 — Implementar e validar

Implemente apenas arquivos dentro do escopo e preserve os testes capturados. A validação pode ser executada no espaço de trabalho sem criar um pacote:

```bash
polis workspace validate --repo /repo \
  --contract /outside/locked-v6.json \
  --policy /outside/policy-v3.json \
  --regression-patch /outside/regression.patch
```

Um Implementation Plan vinculado ao contrato pode ser gerado após `start`. É opcional, mas, se utilizado, os mesmos bytes devem ser fornecidos às etapas que os exigem.

## Etapa 4 — Construir e verificar o pacote

```bash
polis build --repo /repo \
  --policy /outside/policy-v3.json \
  --project aplicativo --change corrigir-validacao \
  --contract /outside/locked-v6.json \
  --regression-patch /outside/regression.patch \
  --out /outside/output

polis verify /outside/output/artifact.polis
polis inspect /outside/output/artifact.polis
```

Os caminhos e nomes de saída devem ser confirmados na execução real. O exemplo descreve um fluxo Red-to-Green não planejado, não um comando universal para qualquer mudança.

## Etapa 5 — Consumir em outro repositório

```bash
polis preflight --repo /consumer /outside/output/artifact.polis

# Somente após revisão e autorização explícita:
polis apply --repo /consumer /outside/output/artifact.polis
```

Preflight não modifica o código consumidor; `apply` repete a validação antes de aplicar. Consulte [Aplicação segura](../aplicacao-segura/) e [Modos de baseline](../baseline/).

## Princípio de isolamento

No fluxo canônico, a política, o contrato bloqueado, a prova Red, o pacote e a assinatura ficam **fora do worktree** do projeto. O POLIS também oferece retenção opcional em `.polis/artifacts/`, configurada explicitamente. Veja a [documentação operacional oficial](https://github.com/MarcosAlves90/polis/blob/main/docs/usage.md#repository-artifact-retention).

---
title: Validação e gates
description: Execute políticas de qualidade, entenda pré-requisitos e diferencie validação local de um artefato de entrega.
group: Fluxo de entrega
order: 3
source: docs/usage.md
---

Um **gate** é uma verificação definida pela Project Policy. Pode representar testes, cobertura, lint ou outro comando configurado. A política controla os checks do projeto; os invariantes de integridade e segurança do protocolo continuam obrigatórios.

## Inspecione antes de executar

```bash
polis plan --repo .
```

`plan` não executa os gates. Ele apresenta ordem, comandos, dependências, habilitações e limitações da política efetiva.

## Execute a validação local

```bash
polis gates --repo .
```

Para validar somente um conjunto explícito ou as verificações afetadas pelas mudanças Git:

```bash
polis gates --repo . --gate lint --gate coverage
polis gates --repo . --affected
```

Dependências necessárias são adicionadas à seleção. `--jobs` aceita de 1 a 16; gates só podem concorrer quando a política declara sua execução paralela segura. Cobertura permanece exclusiva.

> `gates` não é uma sandbox. Executa comandos configurados no repositório real. A validação pode produzir caches ou efeitos externos conforme os comandos do projeto.

## Reutilização e replay

Uma execução pode salvar um manifesto de resultados. O POLIS permite inspecionar, reutilizar resultados aprovados sob condições estritas ou reproduzir a seleção executando-a novamente.

```bash
polis gates --repo . --environment-id toolchain-v1 \
  --out-run /outside/first.json

polis gates --inspect-run /outside/first.json

polis gates --repo . --environment-id toolchain-v1 \
  --reuse /outside/first.json
```

O identificador de ambiente é **declarado por quem executa**; não prova isolamento hermético nem que o ambiente físico realmente corresponde ao nome. Sem identificador, não há reutilização. Resultados prévios não são prova permanente de um estado alterado.

## PASS, FAIL, BLOCKED e DEFERRED

| Estado | Significado |
| --- | --- |
| `PASS` | A checagem aplicável foi concluída com sucesso. |
| `FAIL` | A checagem executada identificou um problema. |
| `BLOCKED` | Uma condição impediu a execução esperada. |
| `DEFERRED` | Um gate habilitado foi adiado no produtor, mas continua obrigação do consumidor em formatos compatíveis. |

## Strict, standard e minimal

`strict` é o nível padrão. `standard` mantém `test.complete` e desabilita cobertura gerada por padrão. `minimal` desabilita gates gerados de qualidade de projeto por padrão. Nenhuma dessas escolhas relaxa as exigências estruturais, de integridade, escopo ou aplicação do protocolo.

Consulte [Política do projeto](../politica-de-projeto/) para configurar gates e [Artefatos](../artefatos/) para ver como a validação se vincula à entrega.

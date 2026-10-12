---
title: Comandos da CLI
description: Referência prática dos principais comandos do POLIS V6, organizada por fase do fluxo.
group: Referência
order: 1
source: docs/usage.md
---

Esta página reúne um índice orientado por propósito. Para parâmetros completos, use **`polis help <comando>`**, `polis <comando> --help` ou a [referência oficial de uso](https://github.com/MarcosAlves90/polis/blob/main/docs/usage.md#command-reference).

## Descoberta e preparação

| Comando | Para que serve |
| --- | --- |
| `help` | Mostra sintaxe e orientação operacional sem executar ações de entrega. |
| `doctor` | Avalia dependências e ambiente da CLI. |
| `init` | Gera uma política de projeto a partir do perfil escolhido. |
| `plan` | Expõe a política efetiva, gates, dependências e garantias, sem executar. |
| `status` | Resume o estado e próximo passo do fluxo a partir dos arquivos fornecidos. |

```bash
polis help
polis help start
polis doctor --format json
polis init --repo . --dry-run
polis plan --repo .
```

## Validação e planejamento

| Comando | Para que serve |
| --- | --- |
| `gates` | Executa gates da Project Policy, inclusive subconjuntos ou afetados. |
| `workspace validate` | Valida uma alteração bloqueada, sem criar pacote `.polis`. |
| `workspace status` | Compara identidade de snapshot com checkpoint não autenticado. |
| `implementation-plan` | Gera um plano opcional derivado do contrato bloqueado. |

```bash
polis gates --repo . --affected
polis implementation-plan --repo /repo \
  --contract /outside/locked-v6.json \
  --out /outside/implementation-plan.json
```

## Construção de entrega

| Comando | Para que serve |
| --- | --- |
| `start` | Bloqueia o contrato contra uma baseline e política efetiva. |
| `check-red-scope` | Confere se arquivos de teste propostos são autorizados. |
| `capture-red` | Captura prova Red genuína para fluxos Red-to-Green. |
| `build` | Valida e cria um pacote verificável de mudança. |

```bash
polis start --repo /repo --policy /outside/policy-v3.json \
  --contract /outside/draft-v5.json \
  --out /outside/locked-v6.json
```

## Leitura e consumo

| Comando | Para que serve |
| --- | --- |
| `verify` | Verifica integridade e consistência de um pacote. |
| `inspect` | Lê metadados após validar o pacote. |
| `preflight` | Verifica um pacote no consumidor sem aplicar a alteração. |
| `apply` | Revalida e aplica o pacote, após autorização. |
| `sign` | Cria uma assinatura destacada sobre o pacote. |
| `export` | Gera um runtime offline, diferente do pacote de entrega. |

```bash
polis verify artifact.polis
polis inspect --format json artifact.polis
polis preflight --repo /consumer artifact.polis
```

## Saiba qual comando não resolve seu problema

- Para ver como seria a validação, use `plan`; para **executar** gates locais, use `gates`.
- Para validar a implementação sem pacote, use `workspace validate`; para produzir um artefato, use `build`.
- Para verificar bytes, use `verify`; para validar contra um destino específico, use `preflight`.
- Para alterar os arquivos do consumidor, use `apply` com autorização.

As flags e a semântica de cada operação podem evoluir dentro da linha V6. Consulte o `polis help` da versão instalada para confirmar o contrato exato.

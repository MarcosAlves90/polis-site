---
title: Comandos da CLI
description: Referência prática dos principais comandos do POLIS V6, organizada por fase do fluxo.
group: Referência
order: 1
source: docs/commands.md
---

Esta página reúne um índice orientado por propósito. Para parâmetros completos, use **`polis help <comando>`**, `polis <comando> --help` ou a [referência oficial dos comandos](https://github.com/MarcosAlves90/polis/blob/main/docs/commands.md#agent-command-instructions), também incorporada ao help da CLI.

Os exemplos usam um **checkout Git com módulo Go na raiz** e uma política externa. Mantenha `POLIS_OUTSIDE` fisicamente fora do repositório (inclusive se configurar a variável manualmente). Os caminhos de contrato e pacote nas seções seguintes pressupõem arquivos válidos criados pelas etapas anteriores; não são nomes gerados automaticamente.

## Descoberta e preparação

| Comando | Para que serve |
| --- | --- |
| `help` | Mostra sintaxe e orientação operacional sem executar ações de entrega. |
| `doctor` | Avalia o ambiente da CLI; `--repo` acrescenta diagnóstico estático do repositório, com `--policy` opcional. |
| `init` | Gera a política de projeto e, sem `--dry-run`, um manifesto de proveniência. |
| `plan` | Expõe gates, garantias e origem/razão das decisões, sem executar. JSON de plano v4. |
| `status` | Projeta provas e próximo passo a partir de entradas externas (`proven`, `stale_or_unproven`, `missing`). |

```bash
polis help
polis help start
polis doctor --format json
POLIS_OUTSIDE="${POLIS_OUTSIDE:-$(mktemp -d)}"
mkdir -p "$POLIS_OUTSIDE"
polis init --repo . --profile auto --dry-run > "$POLIS_OUTSIDE/policy.json"
polis doctor --repo . --policy "$POLIS_OUTSIDE/policy.json"
polis plan --repo . --policy "$POLIS_OUTSIDE/policy.json" --format json
```

## Validação e planejamento

| Comando | Para que serve |
| --- | --- |
| `gates` | Executa gates da Project Policy, inclusive subconjuntos ou afetados, com replay/reuso condicionado. |
| `workspace validate` | Valida uma alteração bloqueada, sem criar pacote `.polis`; aceita `--jobs 1..16`. |
| `workspace status` | Compara identidade de snapshot com checkpoint não autenticado. |
| `implementation-plan` | Gera um plano opcional derivado do contrato bloqueado. |

`implementation-plan` requer um **contrato previamente bloqueado por `polis start`** (mostrado na próxima seção), além da mesma política que foi usada no bloqueio. Os blocos abaixo ilustram comandos por finalidade, não uma sequência que dispense pré-requisitos.

```bash
polis gates --repo . --policy "$POLIS_OUTSIDE/policy.json" --affected
polis implementation-plan --repo . \
  --policy "$POLIS_OUTSIDE/policy.json" \
  --contract "$POLIS_OUTSIDE/locked-v6.json" \
  --out "$POLIS_OUTSIDE/implementation-plan.json"
```

## Construção de entrega

| Comando | Para que serve |
| --- | --- |
| `start` | Bloqueia o contrato contra uma baseline e política efetiva. |
| `check-red-scope` | Confere se arquivos de teste propostos são autorizados. |
| `capture-red` | Captura prova Red genuína para fluxos Red-to-Green. |
| `build` | Valida e cria um pacote verificável em diretório fisicamente externo, com `--jobs 1..16`. |

```bash
polis start --repo . --policy "$POLIS_OUTSIDE/policy.json" \
  --contract "$POLIS_OUTSIDE/draft-v5.json" \
  --out "$POLIS_OUTSIDE/locked-v6.json"
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

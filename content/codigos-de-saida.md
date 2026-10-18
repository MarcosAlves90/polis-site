---
title: Códigos de saída
description: Interprete o exit status da CLI e saiba quando uma verificação foi bloqueada ou falhou.
group: Referência
order: 2
source: docs/commands.md
---

O POLIS mantém categorias estáveis de saída para automação, sem transformar causas diferentes em uma aprovação genérica.

## Tabela de categorias

| Código | Categoria | Interpretação prática |
| --- | --- | --- |
| `0` | `PASS` | Operação concluída conforme seu contrato. |
| `2` | Uso inválido | Sintaxe, flags ou argumentos incorretos. |
| `3` | Artefato/assinatura inválidos | Pacote ou verificação criptográfica rejeitados. |
| `4` | Ambiente ou autorização bloqueados | Uma pré-condição impediu execução ou commit autorizado. |
| `5` | Baseline divergente | O estado do consumidor não satisfaz o modo selecionado. |
| `6` | Falha de validação | Prova, gate, contrato ou condição verificada não passou. |
| `7` | Falha de aplicação | Erro durante aplicação, commit ou rollback. |

## Como diagnosticar

Um exit status é apenas o nível mais compacto da informação. Sempre leia a mensagem contextual e, quando apropriado, a saída estruturada:

Os comandos abaixo são **exemplos independentes**, não uma sequência completa. Para `plan`, prepare antes uma política JSON válida fora do checkout (ou omita `--policy` apenas se `.polis/policy.json` já estiver inalterado e commitado em `HEAD`). Para `preflight`, obtenha primeiro um pacote real e um repositório consumidor.

```bash
polis doctor --format json
polis plan --repo . --policy /outside/policy.json --format json
polis preflight --repo /consumer --format json artifact.polis
```

Não assuma que todo comando usa todos os códigos para exatamente os mesmos erros. A referência operacional da própria CLI descreve os resultados por comando.

## Diferencie falha de teste de falha de ambiente

Se um compilador ou executável necessário está ausente, o teste esperado **não rodou**. Em um fluxo Red-to-Green, essa situação não satisfaz a prova de que o comportamento da base falha pelo motivo especificado.

Para CI, trate `BLOCKED` como uma entrega não aceita até que a condição seja resolvida, e não como um sucesso com aviso.

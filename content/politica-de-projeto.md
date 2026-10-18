---
title: Política do projeto
description: Configure validações explícitas com Project Policy schema v3 e entenda os níveis strict, standard e minimal.
group: Conceitos e segurança
order: 2
source: docs/policy-and-validation.md
---

A **Project Policy** descreve como o POLIS valida um projeto: seus comandos, gates, dependências, ambientes e decisões de habilitação. A política efetiva é ligada por digest ao Change Contract bloqueado.

## Comece pela inspeção

Execute em um checkout Git com módulo Go na raiz. Escolha um diretório externo ao repositório; se definir `POLIS_OUTSIDE` manualmente, confirme que ele também está fora do checkout:

```bash
POLIS_OUTSIDE="${POLIS_OUTSIDE:-$(mktemp -d)}"
mkdir -p "$POLIS_OUTSIDE"
polis init --repo . --profile auto --dry-run > "$POLIS_OUTSIDE/policy.json"
polis plan --repo . --policy "$POLIS_OUTSIDE/policy.json"
```

`auto` detecta módulos Go na raiz. Outros ecossistemas usam `--profile custom` e comandos explícitos. Não copie cegamente gates de uma linguagem para outra. `--dry-run` emite a política sem instalá-la no repositório: o plano acima recebe o arquivo gerado explicitamente.

## Proveniência das decisões

Desde `v6.11.1`, `polis plan --format json` (plano versão 4) informa `source` e `reason` para nível de validação, gates, dependências, decisões do produtor/consumidor e garantias. `polis init` sem `--dry-run` também grava `.polis/policy-provenance.json`: revise e versione **esse manifesto junto de `.polis/policy.json`**. A atribuição a um perfil gerado vale apenas enquanto os digests persistidos coincidirem. Alterações de política e políticas legadas são classificadas conservadoramente; proveniência declarada não é autenticação de autoria.

## Níveis de validação

| Nível | Comportamento |
| --- | --- |
| `strict` | Padrão; mantém os gates gerados de projeto mais rigorosos. |
| `standard` | Mantém `test.complete` e desliga cobertura gerada por padrão. |
| `minimal` | Desliga gates gerados de qualidade de projeto por padrão. |

Nenhum nível desativa os invariantes estruturais, de integridade, escopo, baseline e aplicação do protocolo. Gates desabilitados devem ficar visíveis com sua razão.

## Comandos são argv, não strings de shell

Comandos de política são executados por argumentos diretos. O POLIS rejeita formas reconhecidas de sintetizar shell, como `bash -lc` ou `sh -c` para envolver comandos. Para validação complexa, crie um runner versionado no próprio projeto e declare a chamada direta a esse executável.

Exemplo conceitual do campo de comando:

```json
{
  "argv": ["python", "scripts/validate_project.py"],
  "cwd": ".",
  "timeout_seconds": 600,
  "environment": {
    "mode": "clean",
    "pass": ["PATH", "HOME"]
  }
}
```

> O exemplo acima mostra **apenas um objeto de comando**, não um documento completo de Project Policy válido. Consulte o schema para criar um arquivo.

## Ambiente herdado ou limpo

`environment.mode=inherit` passa o ambiente do processo. `clean` começa de uma base controlada e repassa apenas variáveis nomeadas, além das variáveis mínimas de inicialização de Windows aplicáveis. Valores de ambiente não são persistidos no artefato ou evidência.

## Dependências e concorrência

Os gates podem declarar `depends_on`. O POLIS valida o grafo de dependências e computa ordem determinística. Paralelismo só ocorre com declarações de segurança de execução concorrente; cobertura mantém execução exclusiva.

Gates de comando podem declarar `input_paths_complete: true` **somente se** os `input_paths` abrangerem todas as entradas utilizadas, permitindo reúso vinculado ao subconjunto. Essa declaração é responsabilidade do autor da política: não detecta dependências externas ocultas. Gates de cobertura continuam com identidade global e leitores antigos estritos da política podem rejeitar esse campo novo. Consulte [Validação e gates](../validacao/).

## Mudanças de política exigem novo contrato

Se um contrato já bloqueou o digest de uma política, alterá-la invalida aquela identidade. Não diminua gates somente para forçar aprovação de um pacote: revise a política, estabeleça nova linha de base e crie o contrato correspondente.

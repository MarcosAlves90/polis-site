---
title: Primeiros passos
description: Primeiro fluxo do POLIS 6.12.0 para validar um checkout local ou entregar a outro checkout.
group: Comece aqui
order: 3
source: docs/quickstart.md
---

Este tutorial começa pela verificação do ambiente e separa duas possibilidades: **validar o checkout em que você já trabalha** ou **entregar um pacote a outro checkout**. Uma execução bem-sucedida de `plan` ou `gates` não significa que um pacote `.polis` tenha sido criado.

## Primeiro, escolha como a IA trabalha

- **Agente de IA instalado na sua máquina, com acesso ao mesmo checkout:** siga [Validação local](../validacao-local/). Após preparar contrato, prova e implementação, use `polis workspace validate`; **não é preciso criar um arquivo `.polis`**.
- **Chatbot ou IA na web para entregar alterações a outro checkout:** siga [Entrega remota](../entrega-remota/). Alguém com acesso real ao checkout, ao Git e ao POLIS executa `build` e `verify`; o consumidor decide sobre `preflight` e `apply`. Só uma conversa na web não produz o pacote.

O pacote `alteracao.polis` é um arquivo de transferência; a pasta `.polis/` e `.polis/policy.json` são configuração do projeto. O exemplo a seguir usa **política JSON externa** e serve aos dois caminhos. Os comandos usam Bash (Git Bash no Windows); consulte [Instalação](../instalacao/) para opções de sistema.

## 1. Instale e diagnostique

```bash
go install github.com/MarcosAlves90/polis/v6/cmd/polis@latest
polis doctor
```

O comando `doctor` sem `--repo` verifica os pré-requisitos da CLI, mesmo antes de existir uma política. Depois de preparar a política, `doctor --repo . --policy <arquivo>` acrescenta verificações estáticas de política e ferramentas, sem executar gates. Consulte [Instalação](../instalacao/) caso o binário não esteja no `PATH`.

## 2. Escolha um repositório Git

Use um repositório que você possa inspecionar. O POLIS identifica o estado do Git e a política que governa os comandos de validação.

```bash
cd /caminho/do/seu-projeto
git status --short
```

Não descarte alterações locais para satisfazer a CLI. O fluxo de bloqueio do POLIS existe justamente para impedir que um estado ambíguo seja aceito silenciosamente.

## 3. Prepare a política externa, sem alterar o checkout

Em um módulo Go raiz, o perfil automático pode gerar uma política adequada ao ambiente. Para visualizar sua geração sem persistir arquivos:

```bash
# Mantenha saídas temporárias fora do worktree.
POLIS_OUTSIDE="${POLIS_OUTSIDE:-$(mktemp -d)}"
mkdir -p "$POLIS_OUTSIDE"
polis init --repo . --profile auto --dry-run > "$POLIS_OUTSIDE/policy.json"
polis doctor --repo . --policy "$POLIS_OUTSIDE/policy.json"
```

A detecção automática do perfil `auto` reconhece módulos Go na raiz. Para outros ecossistemas, o perfil `custom` exige configuração explícita dos comandos.

Se você optar por versionar a política no repositório, execute `init` sem `--dry-run` e **revise a política e `.polis/policy-provenance.json` antes de commitá-los**:

```bash
polis init --repo . --profile auto
```

## 4. Veja o plano de validação

```bash
polis plan --repo . --policy "$POLIS_OUTSIDE/policy.json"
```

`plan` é somente leitura: apresenta os gates habilitados, dependências, comandos e garantias ou limitações da política efetiva. Para executá-los localmente:

```bash
polis gates --repo . --policy "$POLIS_OUTSIDE/policy.json"
```

> `gates` executa verificações locais, mas não cria nem verifica artefatos de entrega. `--affected` e `--reuse` podem executar somente parte dos gates; para uma entrega continuam obrigatórios os checks completos e as provas do contrato.

## 5. Escolha o caminho de validação

Os dois caminhos exigem Specification, Change Contract bloqueado, escopo autorizado e prova de desenvolvimento adequada. Esses arquivos têm esquemas e pré-condições definidos na especificação; não devem ser improvisados a partir de um trecho isolado.

- **Mesmo checkout:** siga [Validação local](../validacao-local/) com `polis workspace validate`, que produz um checkpoint externo, sem pacote.
- **Outro checkout:** siga [Entrega remota](../entrega-remota/) com `polis build`, `verify`, `preflight` e `apply`, criando um pacote externo e descartável.

Veja também [SDD e TDD](../sdd-tdd/). Os comandos mostrados são exemplos de sintaxe, não contratos completos prontos para produção.

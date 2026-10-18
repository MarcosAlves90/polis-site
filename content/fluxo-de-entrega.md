---
title: Fluxo de entrega
description: Contratos e provas comuns aos caminhos local e remoto do POLIS 6.12.0.
group: Fluxo de entrega
order: 1
source: docs/quickstart.md
---

O POLIS oferece **dois fluxos**. No checkout em que um agente já trabalha, a validação gera um relatório externo com `workspace validate`, sem pacote. Para transferir a mudança a outro checkout, o produtor cria um pacote `.polis` externo, e o consumidor decide se o aceita. Confira [Validação local](../validacao-local/) e [Entrega remota](../entrega-remota/).

## Qual caminho escolher para a IA?

| Situação | Última etapa do produtor | Entrega |
| --- | --- | --- |
| Agente de IA local, trabalhando no checkout do usuário | `polis workspace validate` após o contrato e a prova | Checkpoint externo opcional; **nenhum pacote `.polis`**. |
| Chatbot/IA na web que precisa entregar a outro checkout | Um produtor com checkout, Git e CLI executa `polis build` e `polis verify` | **Arquivo `.polis` externo**; o consumidor faz `preflight` e `apply` somente após autorização. |

A interface do chat não altera essas regras. Sem acesso ao código e execução efetiva da CLI, o chatbot pode orientar, **mas não gerar ou atestar o pacote**. Também não confunda o arquivo de entrega `mudanca.polis` com a pasta de configuração `.polis/` ou com `.polis/policy.json`; esta política pode ser externa via `--policy`.

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

## Etapa 3 — Implementar e escolher o destino

Implemente apenas arquivos dentro do escopo e preserve os testes capturados. **Se a alteração será revisada neste mesmo checkout**, valide-a no workspace sem criar pacote:

```bash
polis workspace validate --repo /repo \
  --contract /outside/locked-v6.json \
  --policy /outside/policy-v3.json \
  --regression-patch /outside/regression.patch \
  --out-report /outside/workspace-validation.json
```

Esse é o fim da validação **local**; o relatório não é um pacote transferível. Um Implementation Plan vinculado ao contrato pode ser gerado após `start`. É opcional, mas, se utilizado, os mesmos bytes devem ser fornecidos às etapas que os exigem.

## Etapa 4 — Somente para outro checkout: construir e verificar pacote

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

`--out` precisa resolver para um diretório **fisicamente externo** ao repositório produtor. O pacote é descartável e nunca é retido em `.polis/artifacts/packages/`. Os nomes gerados devem ser lidos da saída real; `artifact.polis` é apenas ilustrativo. Este exemplo Red-to-Green não é uma etapa obrigatória do fluxo local.

## Etapa 5 — Somente no fluxo remoto: consumir em outro repositório

```bash
polis preflight --repo /consumer /outside/output/artifact.polis

# Somente após revisão e autorização explícita:
polis apply --repo /consumer /outside/output/artifact.polis
```

Preflight não modifica o código consumidor; `apply` repete a validação antes de aplicar. Consulte [Aplicação segura](../aplicacao-segura/) e [Modos de baseline](../baseline/).

## Princípio de isolamento

Política, contrato bloqueado, prova Red, relatório de workspace, pacote e assinatura devem permanecer **fora do worktree** no fluxo recomendado. A retenção opcional em `.polis/artifacts/` cobre alguns registros, contratos e evidências, **nunca novos pacotes de entrega**. Leia a [referência oficial de retenção](https://github.com/MarcosAlves90/polis/blob/main/docs/retention.md).

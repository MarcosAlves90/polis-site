---
title: Solução de problemas
description: Diagnostique instalação, configuração de gates, escopo, baseline e aplicação rejeitada.
group: Referência
order: 3
source: docs/usage.md
---

Os bloqueios do POLIS normalmente indicam que uma identidade, pré-condição ou prova precisa ser corrigida. A melhor resposta depende **da causa reportada**, não apenas do código de saída.

## `polis: command not found`

Após `go install`, confira `go env GOBIN` e `go env GOPATH`. Adicione o diretório do binário ao `PATH` e teste `polis doctor`. Veja o [guia de instalação](../instalacao/).

## Gate BLOCKED por ferramenta ausente

Leia a mensagem do gate e valide a dependência no ambiente esperado. `BLOCKED` não equivale à falha de uma asserção. Não altere um oráculo Red para aceitar falta de ferramenta como se fosse regressão real.

## `start` rejeita a linha de base

Confirme o worktree, índice, identidade da política e schema do contrato. `start` foi projetado para ocorrer **antes** de implementar uma mudança. Não esconda alterações do usuário com `reset`, `stash` ou exclusão para satisfazer uma checagem.

## `check-red-scope` rejeita um caminho

O caminho proposto precisa caber no escopo autorizado para testes e no escopo geral do contrato. Revise `test_scope.allowed_paths` e `scope.allowed_paths` antes de editar arquivos ou mudar o contrato.

## Reutilização de gates recusada

`--reuse` exige identidades de entrada correspondentes e um `--environment-id` explícito. Esse valor descreve uma declaração do operador; não garante igualdade real do ambiente. Para obter nova evidência, reexecute os gates em vez de forçar reuso incorreto.

## Preflight falha por baseline

O modo padrão `strict` exige commit base exato. Investigue o histórico Git e só considere `compatible` ou `permissive` quando os riscos forem compreendidos e a mudança ainda passar por todas as verificações exigidas. Veja [Modos de baseline](../baseline/).

## Apply encontra uma falha

Pare novas mutações. Inspecione a mensagem da CLI, `git status`, o índice e a árvore de destino. A lógica transacional tenta restaurar o estado em falhas, mas o operador deve verificar o resultado reportado antes de tentar novamente.

## Obter ajuda normativa

```bash
polis help
polis help preflight
polis help apply
```

Consulte também o [guia completo de uso](https://github.com/MarcosAlves90/polis/blob/main/docs/usage.md) e abra uma [issue no repositório](https://github.com/MarcosAlves90/polis/issues) ao identificar divergência reproduzível.

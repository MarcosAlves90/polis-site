---
title: Solução de problemas
description: Diagnostique instalação, configuração de gates, escopo, baseline e aplicação rejeitada.
group: Referência
order: 3
source: docs/commands.md
---

Os bloqueios do POLIS normalmente indicam que uma identidade, pré-condição ou prova precisa ser corrigida. A melhor resposta depende **da causa reportada**, não apenas do código de saída.

## Diagnóstico do repositório antes dos gates

Use `polis doctor --repo /repo` para inspecionar estaticamente a política, os diretórios de trabalho, caminhos de saída e executáveis disponíveis; inclua `--policy /outside/policy.json` quando a política não estiver versionada no checkout. Resultados `PASS`, `BLOCKED` ou `FAIL` do diagnóstico **não** significam que os testes foram executados.

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

Quando um gate usa `input_paths_complete: true`, verifique também arquivos ignorados, diretórios e dependências declaradas. A opção só é segura se os caminhos descrevem todas as entradas; condições externas continuam responsabilidade de quem executa.

## Resultado de `status` indica evidência incompleta

`polis status` pode classificar entradas como `proven`, `stale_or_unproven` ou `missing`. Um exit status de sucesso não transforma relatório histórico em validação atual nem comprova conclusão da implementação. Confira as identidades das entradas e reexecute `workspace validate` quando o checkout tiver mudado.

## `build` rejeita a saída

Confira se `--out` aponta para um diretório fisicamente externo ao worktree e se não existe colisão com um arquivo anterior. Pacotes `.polis` não podem ser criados dentro do repositório ou retidos nele; a limpeza e a verificação final também podem revelar substituição do arquivo ou mudança do diretório de saída.

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

Consulte também a [referência de comandos](https://github.com/MarcosAlves90/polis/blob/main/docs/commands.md) e abra uma [issue no repositório](https://github.com/MarcosAlves90/polis/issues) ao identificar divergência reproduzível.

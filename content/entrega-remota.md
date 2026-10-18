---
title: Entrega remota entre checkouts
description: Produza e transfira um pacote .polis descartável para outro repositório consumidor.
group: Fluxo de entrega
order: 4
source: docs/workflows/web-agent-delivery.md
---

Use este fluxo quando um agente web, CI ou desenvolvedor precisa entregar uma alteração **a outro checkout**. O produtor deve ter acesso real ao repositório de origem, ao Git e ao runtime POLIS; somente texto de uma conversa não comprova que um pacote foi construído ou verificado.

## Produtor: pacote externo e descartável

Parta de uma baseline limpa e commitada. A política, o contrato, a prova, a assinatura e o pacote devem ficar fora do worktree. O `polis build` rejeita saídas resolvidas dentro do repositório, e a retenção do projeto não copia novos pacotes para `.polis/artifacts/packages/`.

Depois de preparar e bloquear os contratos e capturar a prova apropriada conforme [Fluxo de entrega](../fluxo-de-entrega/), execute:

```bash
polis build --repo /producer --policy /outside/policy.json \
  --project project-slug --change change-slug \
  --contract /outside/locked-v6.json \
  --regression-patch /outside/regression.patch \
  --out /outside/packages
```

Para Green-to-Green, omita `--regression-patch` com a prova de caracterização correspondente. O caminho e o nome efetivos do pacote são informados pelo comando; use **o arquivo retornado**, não um nome suposto:

```bash
polis verify /outside/packages/<arquivo-gerado>.polis
polis inspect /outside/packages/<arquivo-gerado>.polis
```

O produtor de `v6.12.0` verifica a identidade e o SHA-256 da saída final antes de reportar sucesso. Isso não impede que outro processo com acesso ao sistema de arquivos desloque o pacote depois da última verificação. Verifique os bytes efetivamente transferidos no consumidor. A assinatura Ed25519 é opcional conforme a política de confiança e só autentica a origem quando conferida com uma chave pública confiável obtida independentemente.

## Consumidor: revisão e autorização

```bash
polis verify /outside/received/change.polis
polis preflight --repo /consumer /outside/received/change.polis
# Somente depois de revisão e autorização:
polis apply --repo /consumer /outside/received/change.polis
```

`preflight` é somente leitura; não autoriza `apply` automaticamente. O consumidor escolhe o repositório alvo e seus critérios de confiança. Após a transferência e quando não for mais necessário, o operador pode descartar o pacote externo; o POLIS não o apaga automaticamente.

O pacote `.polis` de entrega é diferente do ZIP de runtime offline gerado por `polis export`. Consulte o [guia oficial de entrega remota](https://github.com/MarcosAlves90/polis/blob/main/docs/workflows/web-agent-delivery.md) e a [validação local](../validacao-local/) quando o agente já trabalha no checkout de destino.

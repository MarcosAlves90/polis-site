---
title: Entrega remota entre checkouts
description: Produza e transfira um pacote .polis descartável para outro repositório consumidor.
group: Fluxo de entrega
order: 4
source: docs/workflows/web-agent-delivery.md
---

Use este fluxo quando um agente web, CI ou desenvolvedor precisa entregar uma alteração **a outro checkout**. O produtor deve ter acesso real ao repositório de origem, ao Git e ao runtime POLIS; somente texto de uma conversa não comprova que um pacote foi construído ou verificado.

**Usando um chatbot ou IA pela web?** Ele pode ajudar a descrever a mudança e preparar arquivos e instruções. Porém, se não tiver acesso ao repositório e não puder executar Git e POLIS, **não consegue produzir nem verificar o pacote por conta própria**. Um desenvolvedor, agente web com ferramentas ou CI autorizado deve executar os comandos no checkout produtor. Esse fluxo usa um arquivo `.polis` **porque a entrega vai para outro checkout**, não simplesmente porque a IA está no navegador.

## Produtor: pacote externo e descartável

Parta de uma baseline limpa e commitada. A política, o contrato, a prova, a assinatura e o pacote devem ficar fora do worktree. O `polis build` rejeita saídas resolvidas dentro do repositório, e a retenção do projeto não copia novos pacotes para `.polis/artifacts/packages/`.

O arquivo `alteracao.polis` é o **resultado transportável do build**. A pasta `.polis/` pode existir no repositório somente como configuração/evidência, incluindo `.polis/policy.json` e `.polis/policy-provenance.json`. Neste exemplo a política `/outside/policy.json` é **externa**. Nenhuma dessas políticas é o pacote de entrega.

Depois de preparar e bloquear os contratos e capturar a prova apropriada conforme [Fluxo de entrega](../fluxo-de-entrega/), execute:

```bash
polis build --repo /producer --policy /outside/policy.json \
  --project project-slug --change change-slug \
  --contract /outside/locked-v6.json \
  --regression-patch /outside/regression.patch \
  --out /outside/packages
```

Para Green-to-Green, omita `--regression-patch` com a prova de caracterização correspondente. O caminho e o nome efetivos do pacote são informados pelo comando; substitua abaixo o nome ilustrativo pelo **caminho retornado**, sem presumir o nome:

```bash
PACKAGE=/outside/packages/nome-retornado-pelo-build.polis
polis verify "$PACKAGE"
polis inspect "$PACKAGE"
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

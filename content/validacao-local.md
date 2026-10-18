---
title: Validação no workspace local
description: Valide a alteração no checkout do agente, sem criar um pacote de entrega.
group: Fluxo de entrega
order: 3
source: docs/workflows/local-agent-workspace.md
---

**Tem um agente de IA rodando na sua máquina e editando o próprio repositório? Este é o caminho recomendado.** O agente deve ter acesso ao checkout, à CLI POLIS, ao Git e às ferramentas exigidas pelos gates. O POLIS bloqueia o contrato, verifica a prova exigida e executa os gates da política sobre a alteração local. **`workspace validate` não produz nem verifica um arquivo de entrega `.polis`.** Não use `build`, `preflight` ou `apply` apenas para validar esse mesmo checkout.

Se o trabalho começou numa conversa na web, mas um agente com acesso ao checkout faz a implementação e a validação **ali mesmo**, continua sendo este fluxo. Só use [Entrega remota](../entrega-remota/) quando for necessário transferir a alteração como pacote para outro checkout.

## Preparar a área externa

Comece com uma baseline Git limpa e commitada. Mantenha política externa, contrato, plano opcional, prova Red e relatório **fora do repositório**. Caso o projeto utilize `.polis/policy.json`, esse arquivo é configuração de política, não um pacote de entrega.

A pasta `.polis/` pode guardar essa política e o manifesto `.polis/policy-provenance.json`. Nenhum desses arquivos tem o papel de um `alteracao.polis`, que é um pacote de entrega **de outro fluxo**. Neste exemplo, `polis init --dry-run` gera a política JSON fora do checkout, e os comandos seguintes recebem **o mesmo arquivo** via `--policy`.

```bash
polis doctor
POLIS_OUTSIDE="${POLIS_OUTSIDE:-$(mktemp -d)}"
mkdir -p "$POLIS_OUTSIDE"
polis init --repo . --profile auto --dry-run > "$POLIS_OUTSIDE/policy.json"
polis doctor --repo . --policy "$POLIS_OUTSIDE/policy.json"
polis plan --repo . --policy "$POLIS_OUTSIDE/policy.json"
```

O diretório informado por `POLIS_OUTSIDE` precisa estar fisicamente fora do checkout. Prepare um rascunho de Change Contract schema v5 adequado à mudança e bloqueie-o **antes de modificar o código de produção**:

```bash
polis start --repo . --policy "$POLIS_OUTSIDE/policy.json" \
  --contract "$POLIS_OUTSIDE/draft-v5.json" \
  --out "$POLIS_OUTSIDE/locked-v6.json"
```

## Provar e validar a mudança

Em mudanças Red-to-Green, adicione primeiro somente o teste permitido que falha pelo motivo esperado. Verifique seu caminho e capture a prova antes de implementar:

```bash
polis check-red-scope --repo . \
  --contract "$POLIS_OUTSIDE/locked-v6.json" --path path/to/regression_test.go
polis capture-red --repo . --contract "$POLIS_OUTSIDE/locked-v6.json" \
  --out "$POLIS_OUTSIDE/regression.patch"
```

Depois de implementar, valide mantendo os mesmos bytes de política e contrato:

```bash
polis workspace validate --repo . --policy "$POLIS_OUTSIDE/policy.json" \
  --contract "$POLIS_OUTSIDE/locked-v6.json" \
  --regression-patch "$POLIS_OUTSIDE/regression.patch" \
  --out-report "$POLIS_OUTSIDE/workspace-validation.json" --format json
```

Para mudanças Green-to-Green com caracterização válida, omita `--regression-patch`. Quando houver Implementation Plan, forneça os mesmos bytes nas operações que o exigirem. Uma validação concluída informa `workspace_validated: true`, enquanto `delivery_artifact_built` e `delivery_artifact_verified` permanecem falsos.

O relatório `workspace-validation.json` é um **checkpoint externo**, não um pacote transportável, assinatura nem autenticação da autoria. O resultado comprova a validação efetuada naquele estado, não mudanças futuras.

## Retomar a partir de um checkpoint

```bash
polis status --repo . --policy "$POLIS_OUTSIDE/policy.json" \
  --contract "$POLIS_OUTSIDE/locked-v6.json" \
  --regression-patch "$POLIS_OUTSIDE/regression.patch" \
  --report "$POLIS_OUTSIDE/workspace-validation.json" --format json
```

Esse comando compara evidências e identidades; um relatório salvo não comprova que mudanças posteriores foram validadas. Para evidência atual, execute `workspace validate` novamente. Consulte a [referência oficial do workflow local](https://github.com/MarcosAlves90/polis/blob/main/docs/workflows/local-agent-workspace.md) para as pré-condições completas e o [fluxo remoto](../entrega-remota/) quando houver outro checkout consumidor.

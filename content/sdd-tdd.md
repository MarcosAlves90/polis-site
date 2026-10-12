---
title: SDD e TDD
description: Como especificações e provas Red-to-Green ou Green-to-Green estruturam o desenvolvimento estrito.
group: Fluxo de entrega
order: 2
source: spec/POLIS-SPEC-v6.md
---

O POLIS separa duas preocupações complementares. **Specification-Driven Development (SDD)** explicita o contrato de comportamento antes de implementar. **Test-Driven Development (TDD)** produz evidência observada do caminho de desenvolvimento.

## Primeiro, especifique

Um Change Contract estrito liga requisitos identificáveis a critérios de aceite, escopos de implementação e testes e comandos de prova. A identidade da Specification e da política efetiva é bloqueada na linha de base antes das edições.

Uma boa especificação responde:

- Qual comportamento deve passar a existir ou permanecer invariável?
- Quais arquivos podem ser alterados?
- Qual observação concreta prova o comportamento esperado?
- Quais condições devem bloquear a entrega?

## Red-to-Green

Para funcionalidades e defeitos estritos, o produtor deve demonstrar que o teste relevante **falhava na base** e **passa após a mudança**. O POLIS captura uma prova Red real antes de alterações de produção:

```bash
polis check-red-scope --repo /repo \
  --contract /outside/locked-v6.json \
  --path internal/behavior_test.go

polis capture-red --repo /repo \
  --contract /outside/locked-v6.json \
  --out /outside/regression.patch
```

A falha deve corresponder ao comando, código de saída e oráculo previsto; falta de executável não equivale a uma regressão. Os testes capturados são preservados e revalidados nas etapas seguintes.

## Green-to-Green

Mudanças estritamente preservadoras de comportamento usam uma caracterização que já **passa na base** e continua passando no destino. Nesse caso não há justificativa para produzir artificialmente um Red.

## Plano de implementação opcional

```bash
polis implementation-plan --repo /repo \
  --policy /outside/policy-v3.json \
  --contract /outside/locked-v6.json \
  --out /outside/implementation-plan.json
```

O plano é derivado deterministicamente de um contrato bloqueado e deve permanecer subordinado a ele. Quando utilizado em um pacote, altera o formato de entrega para **format v6**, incluindo o plano autenticado como membro adicional.

## Limite importante

A validação consegue provar requisitos observáveis definidos no contrato e executados sob condições concretas. Ela não consegue comprovar uma cronologia de implementação que não foi registrada, nem substituir revisão de segurança ou correção semântica.

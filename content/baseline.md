---
title: Modos de baseline
description: Como strict, compatible e permissive controlam a admissibilidade de um pacote em diferentes estados Git.
group: Conceitos e segurança
order: 3
source: docs/development-proof.md
---

Um pacote é produzido contra uma linha de base bloqueada. O consumidor pode estar em um commit igual ou diferente, e o POLIS permite escolher explicitamente como essa diferença deve ser tratada.

## Strict — padrão

```bash
polis preflight --repo /consumer \
  --baseline-mode strict artifact.polis
```

Exige que o `HEAD` do consumidor corresponda **exatamente** ao commit base bloqueado do artefato. É a opção mais restritiva e o padrão da CLI.

## Compatible — descendente validado

```bash
polis preflight --repo /consumer \
  --baseline-mode compatible artifact.polis
```

Permite um `HEAD` limpo diferente quando há **ancestralidade descendente comprovada** e todas as verificações necessárias de contexto, provas, escopo, política e árvore de destino são aprovadas. Não é uma resolução automática de conflitos.

## Permissive — ancestralidade não comprovada

```bash
polis preflight --repo /consumer \
  --baseline-mode permissive artifact.polis
```

Pode tentar bases sem relação de descendência, ainda exigindo validação de patch, escopo, política e árvore de destino. A ausência de prova de ancestralidade é reportada como risco. Não equivale a ignorar conflitos.

## Prova histórica incorporada

Os formatos mais novos incluem um snapshot autenticado da baseline bloqueada para repetir provas de desenvolvimento quando os objetos Git originais não estão presentes. A opção permissiva pode permitir um waiver **explícito** para prova histórica indisponível, com garantias reduzidas reportadas:

```bash
polis preflight --repo /consumer \
  --baseline-mode permissive \
  --allow-missing-baseline-proof artifact.polis
```

Essa exceção não está disponível nos demais modos. Seu uso precisa de decisão consciente sobre as garantias ausentes.

## Preflight e apply são separados

O modo escolhido para `preflight` não é automaticamente transferido para `apply`. Repita a intenção de forma explícita no comando de aplicação autorizado, e espere uma nova validação.

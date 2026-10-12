---
title: Visão geral
description: Entenda o que é o POLIS, para quem ele foi criado e o que significa entregar mudanças com evidências.
group: Comece aqui
order: 1
source: README.md
---

POLIS é uma **CLI escrita em Go e um protocolo de entrega de mudanças de software**. Ele conecta especificação de comportamento, limites da mudança, testes, validação e integridade do artefato em um processo verificável.

Foi projetado para engenharia assistida por IA, mas seus mecanismos também podem ser usados em entregas conduzidas por pessoas. Não é um modelo de IA, um gerador de código ou um serviço em nuvem: seu papel é **validar, empacotar e controlar a aceitação de alterações**.

## O problema que resolve

Uma mudança pode parecer correta no ambiente de quem a produziu e ainda ser incompatível com o repositório de destino. Também pode ser difícil responder perguntas básicas: quais requisitos ela atende, quais testes foram executados, quais arquivos poderiam ser alterados e qual é a identidade exata do resultado?

O POLIS procura tornar essas perguntas verificáveis por meio de contratos, provas de desenvolvimento, políticas e validação tanto no produtor quanto no consumidor.

## Três fundamentos

1. **Escopo explícito.** O Change Contract delimita o que pode mudar e quais critérios e provas são exigidos.
2. **Evidência verificável.** O produtor cria um pacote `.polis` com dados de validação, identidade e rastreabilidade; os bytes do pacote podem ser verificados independentemente.
3. **Aplicação deliberada.** O consumidor faz `preflight` antes de `apply`; a aplicação repete as verificações sobre o estado atual e exige autorização.

## O que o POLIS não promete

- Não substitui revisão humana nem garante ausência de bugs ou vulnerabilidades.
- Não transforma comandos de projeto em sandbox de segurança; eles ainda podem acessar o ambiente externo.
- Não considera um teste aprovado prova universal do software.
- Não confunde integridade do pacote com autenticidade do autor: autenticidade exige assinatura destacada e chave confiável fornecida pelo consumidor.
- Não faz `push` ou publica releases como efeito implícito de `apply`.

## Entenda as responsabilidades

| Papel | Responsabilidade | Exemplos |
| --- | --- | --- |
| Produtor | Especificar, provar, implementar e empacotar | `start`, `capture-red`, `build` |
| Leitor | Verificar e inspecionar o artefato | `verify`, `inspect` |
| Consumidor | Validar contra seu estado e aplicar quando autorizado | `preflight`, `apply` |

## Por onde começar

Para uma introdução prática, siga [Instalação](../instalacao/) e [Primeiros passos](../primeiros-passos/). Para entender a operação de ponta a ponta, leia [Fluxo de entrega](../fluxo-de-entrega/).

A [Especificação V6](https://github.com/MarcosAlves90/polis/blob/main/spec/POLIS-SPEC-v6.md) é a referência normativa dos contratos de máquina. O [guia de uso oficial](https://github.com/MarcosAlves90/polis/blob/main/docs/usage.md) reúne a referência operacional extensa.

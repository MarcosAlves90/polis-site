---
title: Visão geral
description: Entenda o que é o POLIS, para quem ele foi criado e o que significa entregar mudanças com evidências.
group: Comece aqui
order: 1
source: README.md
---

POLIS é uma **CLI escrita em Go e um protocolo de entrega de mudanças de software**. Ele conecta especificação de comportamento, limites da mudança, testes, validação e integridade do artefato em um processo verificável.

Foi projetado para engenharia assistida por IA, mas seus mecanismos também podem ser usados em entregas conduzidas por pessoas. Não é um modelo de IA, um gerador de código ou um serviço em nuvem: seu papel é **validar mudanças locais e, quando houver transferência, empacotar e controlar sua aceitação**.

## O problema que resolve

Uma mudança pode parecer correta no ambiente de quem a produziu e ainda ser incompatível com o repositório de destino. Também pode ser difícil responder perguntas básicas: quais requisitos ela atende, quais testes foram executados, quais arquivos poderiam ser alterados e qual é a identidade exata do resultado?

O POLIS procura tornar essas perguntas verificáveis por meio de contratos, provas de desenvolvimento e políticas. Para trabalho no próprio checkout, `workspace validate` registra um checkpoint externo sem pacote; para entregar a outro checkout, o produtor constrói um pacote e o consumidor o valida independentemente.

## Três fundamentos

1. **Escopo explícito.** O Change Contract delimita o que pode mudar e quais critérios e provas são exigidos.
2. **Evidência verificável.** A validação local gera um relatório vinculado ao estado observado; uma entrega remota usa um pacote `.polis` cujos bytes podem ser verificados independentemente.
3. **Aplicação deliberada.** Quando há consumidor, ele faz `preflight` antes de `apply`; a aplicação repete as verificações sobre o estado atual e exige autorização.

## O que o POLIS não promete

- Não substitui revisão humana nem garante ausência de bugs ou vulnerabilidades.
- Não transforma comandos de projeto em sandbox de segurança; eles ainda podem acessar o ambiente externo.
- Não considera um teste aprovado prova universal do software.
- Não confunde integridade do pacote com autenticidade do autor: autenticidade exige assinatura destacada e chave confiável fornecida pelo consumidor.
- Não faz `push` ou publica releases como efeito implícito de `apply`.

## Entenda as responsabilidades

| Papel | Responsabilidade | Exemplos |
| --- | --- | --- |
| Agente local | Especificar, provar e validar no próprio checkout, sem pacote | `start`, `capture-red`, `workspace validate` |
| Produtor remoto | Construir um pacote descartável para outro checkout | `build`, `verify` |
| Leitor | Verificar e inspecionar o artefato | `verify`, `inspect` |
| Consumidor | Validar contra seu estado e aplicar quando autorizado | `preflight`, `apply` |

## Por onde começar

Para uma introdução prática, siga [Instalação](../instalacao/) e [Primeiros passos](../primeiros-passos/). Escolha [Validação local](../validacao-local/) ou [Entrega remota](../entrega-remota/) conforme exista ou não transferência entre checkouts. O [Fluxo de entrega](../fluxo-de-entrega/) apresenta o contrato e as provas compartilhadas.

A [Especificação V6](https://github.com/MarcosAlves90/polis/blob/main/spec/POLIS-SPEC-v6.md) é a referência normativa dos contratos de máquina. O [índice oficial de uso](https://github.com/MarcosAlves90/polis/blob/main/docs/usage.md) aponta para a [referência de comandos](https://github.com/MarcosAlves90/polis/blob/main/docs/commands.md) e guias especializados.

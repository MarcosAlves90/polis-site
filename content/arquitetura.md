---
title: Arquitetura
description: Entenda como o guia de engenharia, a especificação normativa e a CLI Go trabalham juntos.
group: Projeto
order: 1
source: docs/usage.md
---

A arquitetura do POLIS separa **processo de engenharia**, **contratos verificáveis** e **implementação executável**. Essa divisão é importante para evitar que instruções narrativas alterem silenciosamente o significado dos pacotes.

## Camadas do projeto

| Camada | Diretório | Responsabilidade |
| --- | --- | --- |
| Engineering Guide | `guide/` | Processo, escopo, obrigações de evidência e práticas de entrega. |
| POLIS Specification | `spec/` | Regras normativas de schemas, pacote, hashing, evidência, assinatura e aplicação. |
| CLI | `cmd/polis/` | Interface de linha de comando e operação das funcionalidades. |
| Implementação | `internal/` | Código Go de suporte à execução e validação. |
| Documentação | `docs/` | Guias operacionais, instalação, exemplos e decisões. |

## Fonte normativa

Se uma explicação do guia de engenharia divergir de uma regra de pacote da Specification, a **Specification versionada** governa a semântica de máquina. A CLI é a implementação de referência, mas seu comportamento observável deve ser verificado por testes e execução.

## Produtor e consumidor

O produtor executa provas de desenvolvimento e produz uma árvore alvo e um `.polis`. O consumidor recebe bytes não confiáveis, verifica a integridade e as regras aplicáveis e executa sua própria validação antes de permitir mutações.

Essa separação limita o valor de uma afirmação como “passou na máquina do autor”: o estado e os comandos efetivos do consumidor importam.

## Dependências e distribuição

A CLI é escrita em Go e usa Git para identidade e aplicação de mudanças. O módulo V6 está publicado no caminho `github.com/MarcosAlves90/polis/v6`. Além da instalação com Go, o projeto oferece kits offline com binário e recursos necessários à CLI, específicos por sistema e arquitetura.

## Manutenção deste site

As páginas deste site são arquivos Markdown em `content/`. O gerador estático `build.py` produz HTML, navegação e índice de busca. O estilo visual está em `assets/styles.css` e as interações em `assets/app.js`. O conteúdo explicativo pode evoluir independentemente do código da CLI.

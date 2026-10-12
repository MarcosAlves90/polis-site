---
title: Contribuição e evolução
description: Encontre as fontes de verdade do projeto e saiba como reportar problemas na documentação.
group: Projeto
order: 2
source: README.md
---

O código-fonte e o histórico do POLIS são mantidos no GitHub. Para propor mudanças, comece verificando a especificação vigente e o comportamento da CLI em sua revisão atual.

## Repositório e documentos principais

- [Código-fonte do POLIS](https://github.com/MarcosAlves90/polis)
- [README e entrada do projeto](https://github.com/MarcosAlves90/polis/blob/main/README.md)
- [Specification V6](https://github.com/MarcosAlves90/polis/blob/main/spec/POLIS-SPEC-v6.md)
- [Guia operacional](https://github.com/MarcosAlves90/polis/blob/main/docs/usage.md)
- [Histórico de mudanças](https://github.com/MarcosAlves90/polis/blob/main/CHANGELOG.md)
- [Issues e discussão de problemas](https://github.com/MarcosAlves90/polis/issues)

## Ao propor uma correção

Prefira relatar comportamento observado, revisão/versão, passos de reprodução, resultado esperado, resultado efetivo e evidências relevantes. Para mudanças que afetam a semântica do protocolo, confirme primeiro a especificação aplicável.

## Contribuir com este site

Esta documentação foi organizada para crescer com alterações isoladas:

1. Crie um arquivo `.md` em `content/` com `title`, `description`, `group`, `order` e `source` no cabeçalho.
2. Escreva as seções com Markdown e vincule a origem oficial do assunto.
3. Execute `python build.py` para gerar HTML estático em `dist/`.
4. Verifique rotas, busca, responsividade, links internos e se o conteúdo continua alinhado ao repositório POLIS.

O site é um guia de apresentação e uso; não cria uma segunda especificação normativa.

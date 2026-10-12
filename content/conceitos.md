---
title: Conceitos fundamentais
description: Um glossário para reconhecer os principais objetos, responsabilidades e estados do POLIS.
group: Comece aqui
order: 4
source: docs/usage.md
---

Antes de produzir um pacote, vale distinguir os objetos centrais do protocolo.

## Glossário

| Conceito | Significado |
| --- | --- |
| **Specification** | Define o comportamento esperado, os requisitos e critérios de aceite. |
| **Project Policy** | Define os comandos e gates de qualidade aplicáveis ao projeto. |
| **Change Contract** | Delimita comportamento, escopo da mudança, provas, testes e identidade da linha de base. |
| **Locked baseline** | Estado Git e política associados a um contrato bloqueado por `polis start`. |
| **Red-to-Green** | Prova observada de falha relevante na base e sucesso após a correção ou funcionalidade. |
| **Green-to-Green** | Caracterização que permanece aprovada antes e depois de uma mudança preservadora de comportamento. |
| **Evidence** | Registros estruturados e limitados de comandos, provas e decisões de validação. |
| **Gate** | Verificação específica configurada pela política, com dependências e estado explícitos. |
| **`.polis`** | Pacote de entrega verificável, diferente do kit offline do runtime. |
| **Preflight** | Validação do pacote no ambiente consumidor, sem aplicar a mudança. |

## PASS, FAIL e BLOCKED não são equivalentes

**PASS** informa que a verificação relevante foi concluída e aprovada. **FAIL** informa uma falha observada de validação. **BLOCKED** indica que uma pré-condição ou ambiente impediu a verificação esperada. Não se deve tratar um comando que não executou o teste como prova de Red.

## Integridade versus autenticidade

Hashes e checksums podem detectar alterações nos bytes de um pacote. Para associar o artefato a um produtor confiável, o consumidor precisa verificar uma assinatura destacada usando uma **chave pública fornecida fora do pacote**. Veja [Segurança e confiança](../seguranca/).

## Quem define o quê?

O guia de engenharia define o processo. A Specification V6 define os contratos de máquina. A CLI implementa o protocolo em Go. Para detalhes, consulte [Arquitetura](../arquitetura/).

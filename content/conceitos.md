---
title: Conceitos fundamentais
description: Um glossário para reconhecer os principais objetos, responsabilidades e estados do POLIS.
group: Comece aqui
order: 4
source: spec/POLIS-SPEC-v6.md
---

Antes de validar um checkout ou produzir um pacote para outro consumidor, vale distinguir os objetos centrais do protocolo.

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
| **Workspace checkpoint** | Relatório externo da validação local, vinculado a identidades observadas e sem pacote de entrega. |
| **Arquivo `mudanca.polis`** | Pacote de entrega verificável gerado por `polis build` para transferência a outro checkout; não é necessário na validação local. |
| **Diretório `.polis/`** | Pasta de configuração do repositório, diferente do pacote transportável. Pode conter política e evidências opcionais. |
| **`.polis/policy.json`** | Project Policy JSON versionada no repositório; alternativamente pode-se usar uma política externa com `--policy`. |
| **`.polis/policy-provenance.json`** | Manifesto opcional de origem das configurações geradas por `polis init`, não uma assinatura nem um pacote. |
| **Preflight** | Validação do pacote no ambiente consumidor, sem aplicar a mudança. |

## PASS, FAIL e BLOCKED não são equivalentes

**PASS** informa que a verificação relevante foi concluída e aprovada. **FAIL** informa uma falha observada de validação. **BLOCKED** indica que uma pré-condição ou ambiente impediu a verificação esperada. Não se deve tratar um comando que não executou o teste como prova de Red.

## Integridade versus autenticidade

Hashes e checksums podem detectar alterações nos bytes de um pacote. Para associar o artefato a um produtor confiável, o consumidor precisa verificar uma assinatura destacada usando uma **chave pública fornecida fora do pacote**. Veja [Segurança e confiança](../seguranca/).

## Quem define o quê?

O guia de engenharia define o processo. A Specification V6 define os contratos de máquina. A CLI implementa o protocolo em Go. Para detalhes, consulte [Arquitetura](../arquitetura/).

---
title: Segurança e confiança
description: Entenda limites de confiança, assinaturas, entradas não confiáveis e garantias reais do consumidor.
group: Conceitos e segurança
order: 4
source: spec/POLIS-SPEC-v6.md
---

POLIS foi projetado para **falhar de forma conservadora** diante de entradas inválidas e estados incompatíveis. Ainda assim, é importante distinguir quais garantias são oferecidas e o que permanece sob responsabilidade do operador.

## Fronteiras de confiança

O pacote `.polis` deve ser tratado como **entrada não confiável**. O verificador aplica regras de inventário, tamanho, schema, checksums e consistência de evidência antes de permitir o consumo. O Change Contract limita caminhos autorizados e o consumidor valida a árvore alvo.

## Autenticidade exige chave externa

Assinaturas Ed25519 destacadas podem vincular os bytes exatos do pacote a uma identidade confiável **somente quando o consumidor fornece uma chave pública previamente confiável**. Chaves encontradas dentro do próprio artefato não podem se autodeclarar autoridade.

```bash
polis verify --signature artifact.polis.sig \
  --trusted-key producer-public.pem \
  artifact.polis
```

## Isolamento não é sandbox

`build`, `preflight` e `apply` usam validação em repositórios ou worktrees isolados em etapas relevantes. Isso protege o estado Git, mas **não isola necessariamente processos do sistema operacional, rede ou credenciais**. Revise comandos de política e provas antes de executar artefatos não confiáveis.

## O estado presente importa

- `preflight` é uma inspeção atual, não uma aprovação que vale para sempre.
- `apply` repete a validação sobre o estado consumidor antes de modificar arquivos.
- Um código de saída não-zero por pré-requisito ausente não prova que um teste identificou um defeito.
- Um hash confere integridade de bytes, não segurança semântica do código.

## Autorizações irreversíveis

`apply` deve ser solicitado explicitamente para o repositório correto. `--commit-mode auto` exige intenção explícita de criar commit local. O POLIS não deve inferir permissão de publicação de um sucesso de validação.

## Onde a confiança termina

Mesmo com verificação correta, um patch pode ser funcionalmente inseguro em circunstâncias não cobertas pelos testes. Validação verificável **aumenta a auditabilidade**, mas não substitui revisão, threat modeling e testes pertinentes ao projeto.

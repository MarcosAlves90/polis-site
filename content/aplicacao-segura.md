---
title: Aplicação segura
description: Entenda o preflight, a revalidação em apply e os modos explícitos de commit no consumidor.
group: Fluxo de entrega
order: 5
source: docs/usage.md
---

O consumidor precisa verificar a entrega **no próprio estado Git e ambiente**. Um PASS obtido pelo produtor ou por um preflight anterior não é uma autorização permanente para alterar arquivos.

## 1. Verifique o pacote

```bash
polis verify artifact.polis
polis inspect artifact.polis
```

Revise o escopo, o conteúdo do patch e os comandos de política que serão executados. Os comandos configurados podem produzir efeitos externos; isolamento de worktree não substitui sandbox para código não confiável.

## 2. Faça preflight

```bash
polis preflight --repo /destino /outside/artifact.polis
```

`preflight` verifica o pacote, as condições de baseline, o alvo em ambiente isolado, as provas e os gates aplicáveis, incluindo os adiados pelo produtor. **Não aplica o patch ao consumidor**.

Se o estado do repositório mudar depois desse comando, o PASS não pode ser reutilizado como prova de que a aplicação continua válida.

## 3. Aplique apenas após autorização

```bash
polis apply --repo /destino /outside/artifact.polis
```

`apply` repete a validação antes de mutar arquivos e confere a identidade do resultado. Na execução canônica sem commit, preserva HEAD e o índice Git real. O protocolo tem verificação e rollback para falhas de aplicação, mas erros devem ser investigados e o estado restaurado deve ser conferido.

## Modos de commit

O padrão é `--commit-mode none`, que aplica o conteúdo sem criar commit. Quando o artefato contém intenção de commit válida, há alternativas explícitas:

```bash
# Requer terminal interativo e confirmação:
polis apply --repo /destino --commit-mode prompt /outside/artifact.polis

# Autoriza criar um commit local sem perguntar:
polis apply --repo /destino --commit-mode auto /outside/artifact.polis
```

O modo `auto` é uma **autorização local explícita**, não uma substituição para a ausência de terminal de um agente. Nenhum modo executa automaticamente `git push`, assina o commit ou publica uma release.

## Baselines diferentes

O padrão é `--baseline-mode strict`, que exige igualdade do commit base. `compatible` aceita descendentes limpos sujeitos a provas completas. `permissive` admite tentativa mais ampla com avisos e sem eliminar conflitos reais. Leia [Modos de baseline](../baseline/) antes de relaxar o padrão.

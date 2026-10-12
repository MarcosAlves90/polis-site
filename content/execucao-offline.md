---
title: Execução offline
description: Distribua o runtime do POLIS para agentes e máquinas sem instalar Go ou acessar a rede.
group: Fluxo de entrega
order: 6
source: spec/POLIS-OFFLINE.md
---

O POLIS V6 possui um **runtime offline portátil por plataforma**. O bundle contém o executável nativo, a especificação, schemas, manifesto e arquivos necessários à operação da CLI. Ele é diferente de um pacote de mudança `.polis`.

## Obter um bundle

Baixe um ZIP correspondente ao seu sistema operacional e arquitetura nas [releases oficiais](https://github.com/MarcosAlves90/polis/releases/latest):

```text
polis-<tag>-offline-<GOOS>-<GOARCH>.zip
```

Após extrair, execute `bin/polis` no Unix/macOS ou `bin/polis.exe` no Windows. O bundle **não precisa de Go** para executar a CLI.

## Dependências e limites

- O Git precisa estar instalado e acessível no `PATH`.
- O binário precisa corresponder exatamente ao sistema operacional e à arquitetura da máquina.
- Comandos declarados na Project Policy podem exigir compiladores, runtimes, rede e ferramentas do projeto de destino.
- O bundle **não contém o repositório alvo nem sua política específica**.

## Exportar um kit local

A partir de uma CLI POLIS instalada:

```bash
polis export --out /outside/polis-v6-offline.zip
```

A exportação gera um ZIP determinístico, com manifesto e checksums, sem ler dados do repositório de destino. Os argumentos `--executable` e `--runtime` permitem incorporar binários construídos externamente para um alvo específico, sem executá-los no host exportador.

## Usar com agentes

Para um agente offline, entregue o bundle adequado e uma cópia dos artefatos/contratos **explicitamente autorizados**. O agente deve conhecer a política do projeto e a fronteira entre comandos de leitura, validação e mutação.

Leia a [especificação do kit offline](https://github.com/MarcosAlves90/polis/blob/main/spec/POLIS-OFFLINE.md) antes de distribuí-lo.

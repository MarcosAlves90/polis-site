---
title: Artefatos e verificação
description: Conheça o pacote .polis, os formatos V6, a inspeção e o papel das assinaturas destacadas.
group: Fluxo de entrega
order: 6
source: docs/artifact-trust.md
---

O arquivo `.polis` é o produto de uma entrega validada. Ele reúne a mudança, os contratos e a evidência necessária para verificação e consumo, dentro de limites e esquemas definidos pela especificação.

**Um agente de IA que já trabalha no checkout do usuário não precisa desse arquivo**: usa `polis workspace validate` e pode guardar um checkpoint externo. Um chatbot na web que só conversa também não produz o arquivo; quando é necessária uma entrega entre checkouts, um produtor com Git, código-fonte e POLIS executa o `build`.

**Arquivo `mudanca.polis` não é diretório `.polis/`.** O segundo guarda configuração como `.polis/policy.json` e `.polis/policy-provenance.json` e eventualmente evidências em `.polis/artifacts/`; uma política JSON pode igualmente ser externa via `--policy`. Um novo pacote de entrega nunca é retido dentro do diretório de configuração.

## Criar um pacote

O produtor usa `polis build` somente para entregar mudanças a **outro checkout**, depois de bloquear a base e cumprir as provas obrigatórias de desenvolvimento. `--out` exige diretório fisicamente externo ao repositório. O comando retorna o nome real do pacote criado; os nomes abaixo são ilustrativos:

```bash
polis verify /outside/output/artifact.polis
polis inspect --format json /outside/output/artifact.polis
```

`verify` verifica os bytes, os membros obrigatórios, os checksums, schemas e consistência das provas suportadas. `inspect` expõe metadados validados; não aplica a mudança.

Desde `v6.12.0`, o produtor confere SHA-256 e identidade do arquivo final e restringe a limpeza ao arquivo originalmente criado. Processos externos com acesso ao sistema de arquivos ainda podem modificar ou mover o resultado **depois** da última conferência. Proteja o diretório externo e verifique os bytes transferidos. Novos pacotes não são retidos em `.polis/artifacts/packages/`, mesmo quando a retenção de outros tipos de evidência está habilitada.

## Formatos no POLIS V6

| Artefato produzido | Formato de pacote | Característica |
| --- | --- | --- |
| Entrega sem plano explícito | `format v5` | Oito membros canônicos, incluindo baseline incorporada. |
| Entrega com Implementation Plan | `format v6` | Nove membros; o plano é vinculado ao pacote e à evidência. |

O nome **POLIS V6** se refere à versão do protocolo/CLI; não implica que todo pacote novo tenha necessariamente formato 6. A versão de pacote depende da presença do Implementation Plan. Formatos anteriores aceitos continuam legíveis sob as regras de compatibilidade.

## Checksums não identificam o produtor

Um checksum valida a relação entre dados e digest, mas não garante quem criou o pacote. A autenticidade opcional usa assinatura **Ed25519 destacada**, verificada com uma chave pública confiável obtida independentemente do artefato.

```bash
polis sign --key private.pem \
  --out artifact.polis.sig artifact.polis

polis verify \
  --signature artifact.polis.sig \
  --trusted-key public.pem \
  artifact.polis
```

A chave privada deve permanecer protegida. O consumidor não deve confiar em uma chave indicada pelo próprio pacote sem uma cadeia de confiança externa.

## Plano e rastreabilidade

Quando há plano de implementação, `inspect` pode relatar a relação entre requisitos, critérios de aceite, etapas e provas. A presença do plano não substitui a execução das validações previstas.

## A leitura não é a aplicação

`verify` e `inspect` operam sobre o artefato. Para saber se ele pode ser aplicado a **um repositório específico**, execute [preflight](../aplicacao-segura/) no consumidor antes da aplicação autorizada.

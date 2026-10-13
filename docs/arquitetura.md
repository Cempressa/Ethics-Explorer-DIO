# Arquitetura do Ethics Explorer

## Visão Geral

O **Ethics Explorer** é uma plataforma educacional em linha de comando (CLI) estruturada em camadas bem definidas, seguindo o princípio da separação de responsabilidades.

---

## Diagrama de Camadas

```
┌─────────────────────────────────────────────────────┐
│                   INTERFACE                          │
│                                                      │
│   CLI (src/main.py)        MCP Server (mcp/)         │
│   commands/trilha.py       mcp/server.py             │
│   commands/desafio.py      mcp/tools.py              │
│   commands/certificado.py                            │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│                 LÓGICA DE NEGÓCIO                    │
│                                                      │
│   src/services.py                                    │
│   (get_trilha, get_desafios, generate_certificado)   │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│                   MODELOS DE DADOS                   │
│                                                      │
│   src/models.py                                      │
│   (Trilha, Modulo, Desafio, Certificado, Categoria)  │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│                  FONTE DE DADOS                      │
│                                                      │
│   data/trilhas.json                                  │
│   data/desafios.json        (futuro: Appwrite)       │
│   data/categorias.json                               │
└─────────────────────────────────────────────────────┘
```

---

## Descrição das Camadas

### 1. Interface (commands/ e mcp/)

Responsável por receber entradas do usuário (CLI) ou de agentes de IA (MCP) e apresentar resultados formatados.

- **`commands/`**: Comandos Click para uso em terminal. Cada arquivo é um comando independente.
- **`mcp/`**: Servidor MCP que expõe as mesmas funcionalidades como tools para LLMs e agentes.

**Princípio:** A interface nunca contém lógica de negócio — ela apenas delega para `src/services.py`.

---

### 2. Lógica de Negócio (src/services.py)

Contém toda a lógica da aplicação:
- Busca e filtragem de trilhas e desafios
- Geração de certificados (código de verificação, renderização, persistência)
- Listagens de categorias

**Princípio:** Esta camada não sabe como os dados chegam (JSON local ou API Appwrite) nem como são exibidos (CLI ou MCP). Ela opera apenas com modelos de dados.

---

### 3. Modelos de Dados (src/models.py)

Define as estruturas de dados usando `dataclasses` Python:
- `Trilha`, `Modulo` — estruturas de planos de estudo
- `Desafio` — questão de múltipla escolha
- `Certificado` — dados de emissão de certificado
- `Categoria` — metadados dos temas

---

### 4. Fonte de Dados (data/)

Atualmente: arquivos JSON locais.
Futuro: collections no Appwrite.

A migração exige alteração **apenas** em `src/services.py`, sem impacto em nenhuma outra camada.

---

## Fluxo de uma Chamada CLI

```
Usuário
  │
  ▼
python src/main.py desafio --tema lgpd --nivel iniciante
  │
  ▼
commands/desafio.py :: cmd_desafio()
  │
  ▼
src/services.py :: get_desafios("lgpd", "iniciante")
  │
  ▼
src/utils.py :: load_json("desafios.json")
  │
  ▼
data/desafios.json
  │
  ▼
[Desafio filtrado] → formatado e exibido no terminal
```

---

## Fluxo de uma Chamada MCP

```
Agente de IA
  │
  ▼
tool: get_desafio { tema: "lgpd", nivel: "iniciante" }
  │
  ▼
mcp/tools.py :: handle_tool_call("get_desafio", {...})
  │
  ▼
src/services.py :: get_desafios("lgpd", "iniciante")
  │
  ▼
[Resultado JSON retornado ao agente]
```

---

## Decisões de Design

| Decisão | Justificativa |
|---|---|
| Click para CLI | Biblioteca madura, auto-documentada, suporte a subcomandos |
| dataclasses Python puras | Sem dependência pesada; substituto leve para Pydantic na v1 |
| JSON local como fonte de dados | Zero dependências externas; migração futura para Appwrite sem refatoração |
| Camada de serviços isolada | Reutilizável por CLI e MCP sem duplicação de código |
| Certificados em texto puro | Portabilidade máxima; substituto por PDF/imagem em versões futuras |

---

## Roadmap de Evolução

| Versão | Funcionalidade |
|---|---|
| v1.0 | CLI com trilhas, desafios e certificados via JSON local |
| v1.1 | Integração com Appwrite (banco de dados e storage) |
| v1.2 | Servidor MCP completo com SDK oficial |
| v2.0 | Interface web (FastAPI + frontend) |
| v2.1 | Progresso do usuário e histórico de desafios |
| v3.0 | Certificados em PDF com assinatura digital |

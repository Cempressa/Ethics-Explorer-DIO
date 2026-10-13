# Modelo de Dados — Ethics Explorer

## Visão Geral

Os dados da plataforma são armazenados em três arquivos JSON no diretório `data/`.
Esta documentação descreve a estrutura de cada arquivo.

---

## data/categorias.json

Define as categorias temáticas disponíveis e os níveis de dificuldade.

### Estrutura

```json
{
  "categorias": [
    {
      "id": "string",           // Identificador único (snake_case)
      "nome": "string",         // Nome de exibição
      "descricao": "string",    // Descrição da categoria
      "nivel_minimo": "string", // Nível mínimo recomendado
      "icone": "string"         // Emoji representativo
    }
  ],
  "niveis": ["string"]          // Lista de níveis disponíveis
}
```

### Categorias disponíveis

| id | nome |
|---|---|
| `etica_profissional` | Ética Profissional |
| `compliance` | Compliance |
| `lgpd` | LGPD |
| `seguranca_informacao` | Segurança da Informação |
| `conduta_organizacional` | Conduta Organizacional |
| `combate_corrupcao` | Combate à Corrupção |

### Níveis disponíveis

`iniciante` · `intermediario` · `avancado`

---

## data/trilhas.json

Define os planos de estudo por categoria, com módulos e recursos.

### Estrutura

```json
{
  "trilhas": [
    {
      "id": "string",              // Identificador único (ex: "trilha_lgpd")
      "categoria": "string",       // Referência ao id em categorias.json
      "titulo": "string",          // Título da trilha
      "descricao": "string",       // Descrição resumida
      "duracao_estimada": "string", // Ex: "6 horas"
      "modulos": [
        {
          "ordem": 1,              // Posição do módulo na trilha
          "titulo": "string",
          "objetivo": "string",    // O que o aluno aprenderá
          "topicos": ["string"],   // Lista de tópicos cobertos
          "recursos": ["string"]   // Materiais de apoio
        }
      ]
    }
  ]
}
```

### Regras

- Cada trilha possui exatamente uma categoria (relacionamento 1:1).
- Os módulos devem ser ordenados pelo campo `ordem` (inteiro crescente).
- O campo `categoria` deve corresponder a um `id` válido em `categorias.json`.

---

## data/desafios.json

Define as questões de múltipla escolha por categoria e nível.

### Estrutura

```json
{
  "desafios": [
    {
      "id": "string",             // Identificador único (ex: "d001")
      "categoria": "string",      // Referência ao id em categorias.json
      "nivel": "string",          // "iniciante" | "intermediario" | "avancado"
      "pergunta": "string",       // Enunciado da questão
      "alternativas": [           // Exatamente 4 alternativas (A, B, C, D)
        "A) ...",
        "B) ...",
        "C) ...",
        "D) ..."
      ],
      "resposta_correta": "string", // "A" | "B" | "C" | "D"
      "explicacao": "string"       // Justificativa da resposta correta
    }
  ]
}
```

### Regras

- O campo `id` deve ser único em todo o arquivo.
- O campo `categoria` deve corresponder a um `id` válido em `categorias.json`.
- O campo `nivel` deve ser um dos valores: `iniciante`, `intermediario`, `avancado`.
- O campo `resposta_correta` deve ser exatamente `"A"`, `"B"`, `"C"` ou `"D"`.
- Cada desafio deve ter exatamente 4 alternativas.

---

## Relacionamentos

```
categorias.json
      │
      ├──── trilhas.json (campo: categoria → id)
      │
      └──── desafios.json (campo: categoria → id)
```

---

## Migração para Appwrite (futuro)

| Arquivo JSON | Collection Appwrite |
|---|---|
| `categorias.json` | `categorias` |
| `trilhas.json` | `trilhas` + `modulos` (sub-collection) |
| `desafios.json` | `desafios` |
| `certificates/` | Storage: bucket `certificados` |

A migração exigirá alterações apenas em `src/services.py`:
- Substituir `load_json()` por chamadas ao SDK do Appwrite.
- Adicionar autenticação e controle de acesso.

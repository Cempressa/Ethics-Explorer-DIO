# Guia de Uso — Ethics Explorer

## Instalação

```bash
git clone https://github.com/seu-usuario/Ethics-Explorer.git
cd Ethics-Explorer
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux / macOS
pip install -r requirements.txt
```

---

## Comando: trilha

Exibe o plano de estudos completo de um tema.

### Sintaxe

```bash
python src/main.py trilha --tema <TEMA>
python src/main.py trilha --listar
```

### Opções

| Opção | Atalho | Descrição |
|---|---|---|
| `--tema` | `-t` | ID do tema a exibir |
| `--listar` | `-l` | Lista todas as trilhas disponíveis |

### Exemplos

```bash
# Listar todas as trilhas disponíveis
python src/main.py trilha --listar

# Exibir trilha de LGPD
python src/main.py trilha --tema lgpd

# Exibir trilha de Compliance
python src/main.py trilha --tema compliance

# Exibir trilha de Ética Profissional
python src/main.py trilha --tema etica_profissional
```

### Saída esperada

```
════════════════════════════════════════════════════════════
  📚  LGPD — LEI GERAL DE PROTEÇÃO DE DADOS
════════════════════════════════════════════════════════════
  Entenda a LGPD, seus princípios, direitos dos titulares...
  ⏱  Duração estimada: 6 horas
════════════════════════════════════════════════════════════

  MÓDULO 1: Fundamentos da LGPD
  ────────────────────────────────────────────────────────
  🎯 Objetivo: Conhecer a estrutura e os princípios da Lei 13.709/2018.

  📌 Tópicos:
     • O que é a LGPD e por que ela existe?
     • Conceitos: dado pessoal, dado sensível, titular...
     ...
```

---

## Comando: desafio

Gera questões de múltipla escolha por tema e nível.

### Sintaxe

```bash
python src/main.py desafio --tema <TEMA> --nivel <NIVEL>
python src/main.py desafio --aleatorio
python src/main.py desafio --tema <TEMA> --nivel <NIVEL> --todos
```

### Opções

| Opção | Atalho | Descrição |
|---|---|---|
| `--tema` | `-t` | ID do tema |
| `--nivel` | `-n` | Nível: `iniciante`, `intermediario`, `avancado` |
| `--aleatorio` | `-a` | Gera desafio aleatório |
| `--todos` | — | Apresenta todos os desafios em sequência |

### Exemplos

```bash
# Desafio iniciante sobre LGPD
python src/main.py desafio --tema lgpd --nivel iniciante

# Desafio avançado sobre compliance
python src/main.py desafio --tema compliance --nivel avancado

# Desafio completamente aleatório
python src/main.py desafio --aleatorio

# Desafio aleatório de tema específico
python src/main.py desafio --tema seguranca_informacao --aleatorio

# Todos os desafios de ética profissional nível intermediário
python src/main.py desafio --tema etica_profissional --nivel intermediario --todos
```

### Saída esperada

```
  ══════════════════════════════════════════════════════════
  🏷️  Tema: Lgpd
  📊 Nível: Iniciante
  ══════════════════════════════════════════════════════════

  ❓ O que são dados pessoais sensíveis segundo a LGPD?

     A) Dados de clientes armazenados fora do Brasil.
     B) Dados que revelam origem racial, convicção religiosa...
     C) Dados financeiros de pessoas jurídicas.
     D) Qualquer dado armazenado em formato digital.

  Sua resposta (A/B/C/D): B

  ──────────────────────────────────────────────────────────
  ✅ CORRETO! Muito bem!

  💡 Explicação:
  A LGPD define dados sensíveis como aqueles que revelam...
```

---

## Comando: certificado

Gera e salva um certificado fictício de conclusão.

### Sintaxe

```bash
python src/main.py certificado --nome "<NOME>" --tema <TEMA>
```

### Opções

| Opção | Atalho | Descrição |
|---|---|---|
| `--nome` | `-n` | Nome completo do participante (obrigatório) |
| `--tema` | `-t` | ID do tema concluído (obrigatório) |

### Exemplos

```bash
python src/main.py certificado --nome "Maria Silva" --tema lgpd
python src/main.py certificado --nome "João Oliveira" --tema compliance
python src/main.py certificado -n "Ana Costa" -t combate_corrupcao
```

### Saída esperada

```
  🎓 Gerando certificado para: Maria Silva
  📚 Trilha: lgpd

  ╔══════════════════════════════════════════════════════════════╗
  ║                    CERTIFICADO DE CONCLUSÃO                  ║
  ║                        Ethics Explorer                       ║
  ╠══════════════════════════════════════════════════════════════╣
  ║                                                              ║
  ║                      Certificamos que                        ║
  ║                                                              ║
  ║                        MARIA SILVA                           ║
  ║                                                              ║
  ║                 concluiu com êxito a trilha:                 ║
  ║             LGPD — Lei Geral de Proteção de Dados            ║
  ║                                                              ║
  ║        Data: 13/10/2026  |  Código: EE-2026-A1B2C3D4        ║
  ║                                                              ║
  ╚══════════════════════════════════════════════════════════════╝

  ✅ Certificado salvo em:
  📁 certificates/certificado_maria_silva_lgpd.txt
```

---

## Servidor MCP

Para usar o Ethics Explorer como servidor MCP com agentes de IA:

```bash
# Verificar informações do servidor
python mcp/server.py --info

# Iniciar servidor em modo stdio
python mcp/server.py
```

### Tools disponíveis

| Tool | Parâmetros | Descrição |
|---|---|---|
| `get_trilha` | `tema` | Retorna trilha completa |
| `list_trilhas` | — | Lista todas as trilhas |
| `get_desafio` | `tema`, `nivel`, `aleatorio` | Retorna um desafio |
| `generate_certificado` | `nome`, `tema` | Gera certificado |
| `list_categorias` | — | Lista todas as categorias |

---

## Temas Disponíveis

| ID | Nome |
|---|---|
| `etica_profissional` | Ética Profissional |
| `compliance` | Compliance |
| `lgpd` | LGPD |
| `seguranca_informacao` | Segurança da Informação |
| `conduta_organizacional` | Conduta Organizacional |
| `combate_corrupcao` | Combate à Corrupção |

Antes de ler: Esse é um projeto feito para o curso de Ciência de Dados da Faculdade FIAP(Brazil) com propósito educacional. 


# 🚀 Missão Aurora Siger — MGPEB

> **Módulo de Gerenciamento de Pouso e Estabilização de Base**  
> Protótipo em Python — Simulação de Pouso Espacial

---

## 📋 Sobre o Projeto

O **MGPEB** é uma simulação computacional do gerenciamento autônomo de pouso de módulos espaciais em uma base extraterrestre. O sistema coordena a sequência de aterrissagem, avalia condições ambientais e operacionais em tempo real, e autoriza ou nega o pouso de forma autônoma — priorizando a segurança da tripulação e a continuidade da missão.

A arquitetura é inspirada em sistemas reais como o **Apollo Guidance Computer (NASA)**, o **Sky Crane do Curiosity (Mars)** e o sistema de pouso do **Falcon 9 (SpaceX)**, com paralelos diretos a sistemas operacionais de tempo real (RTOS).

---

## Arquivos da pasta descrição desse repositório

- FIAP_Aurora_Siger_MGPEB - PDF com a explicação do projeto - Português
- MGPEBPortugues – Versão em Python do projeto - Português
- MGPEBEnglish – Versão em Python do projeto - Inglês
- [README_MGPEB_English.md](./README_MGPEB_English.md) – Versão em inglês do README



## 🛸 Módulos de Pouso Simulados

| Módulo | Prioridade | Crítico | TCA (h) |
|---|---|---|---|
| Módulo Habitacional | 1 | ✅ Sim | 2 |
| Módulo de Energia Solar | 2 | ✅ Sim | 4 |
| Módulo de Suprimentos Médicos | 2 | ✅ Sim | 5 |
| Módulo de Laboratório Científico | 3 | ❌ Não | 6 |
| Módulo de Suprimentos | 4 | ❌ Não | 8 |

> Combustível (20–99%) e peso (5–35t) são gerados aleatoriamente a cada execução via `random.uniform()`, simulando variabilidade real de missão.

---

## ⚙️ Funcionalidades

- **Ordenação por prioridade** via *Insertion Sort* antes do processamento da fila
- **Autorização de pouso** com lógica booleana AND/OR por criticidade do módulo
- **Fila FIFO** (`collections.deque`) para processamento eficiente dos módulos
- **Pilha LIFO** para gerenciamento de alertas em ordem de urgência
- **Busca linear** pelo módulo de menor combustível e maior prioridade
- **Modelagem de consumo** com decaimento exponencial `C(t) = C₀ · e^(−k·t)`
- **Relatório de missão** completo em 5 fases no console

---

## 🔐 Regras de Decisão — Lógica Booleana

### Módulos Críticos — AND Total
O pouso só é autorizado quando **todas** as condições são verdadeiras simultaneamente:

```
C1 (Combustível ≥ 40%) AND C2 (Atmosfera OK) AND C3 (Área livre) AND C4 (Sensores OK)
```

### Módulos Não-Críticos — AND + OR
Lógica mais flexível, permitindo pouso em condições parcialmente adversas:

```
C1 (Combustível ≥ 40%) AND C4 (Sensores OK) AND (C2 OR C3)
```

---

## 📐 Modelagem Matemática

O consumo de combustível durante a descida é modelado por **decaimento exponencial**:

```
C(t) = C₀ · e^(−k·t)
```

| Parâmetro | Descrição |
|---|---|
| `C₀` | Combustível inicial (%) |
| `k` | Taxa de consumo por hora (padrão: `0.08`) |
| `t` | Tempo decorrido em horas |

> Valores maiores de `k` simulam descidas mais rápidas com maior consumo.

---

## 🏗️ Arquitetura em Camadas

| Camada | Componente | Função |
|---|---|---|
| 1 — Dados | Dicionários Python | Representação dos módulos |
| 2 — Decisão | Funções Booleanas | Avalia AND/OR das condições de pouso |
| 3 — Busca | Busca Linear O(n) | Localiza menor combustível / maior prioridade |
| 4 — Ordenação | Insertion Sort | Reordena fila por prioridade |
| 5 — Modelagem | Decaimento Exponencial | Prevê consumo `C(t) = C₀·e^(−kt)` |
| 6 — Estruturas | Lista / Fila / Pilha | Controla fluxo FIFO e alertas LIFO |
| 7 — Saída | Console | Relatório de missão e diagnósticos |

---

## 📊 Estruturas de Dados Utilizadas

| Estrutura | Implementação | Operação Principal | Complexidade | Uso no MGPEB |
|---|---|---|---|---|
| Lista | `list` | `append()` / acesso `[i]` | O(1) amort. | Módulos pousados e em espera |
| Fila (FIFO) | `collections.deque` | `popleft()` | O(1) | Fila de pouso ordenada |
| Pilha (LIFO) | `list` | `append()` / `pop()` | O(1) | Pilha de alertas de negação |

> **Por que `deque` e não `list` para a fila?**  
> A remoção da frente em listas convencionais é O(n). O `collections.deque` oferece `popleft()` em O(1) — essencial em sistemas de tempo real onde o atraso de escalonamento deve ser mínimo.

---

## 🖥️ Fases da Simulação

```
FASE 1 — Reorganizando fila por prioridade (Insertion Sort)
FASE 2 — Processando autorizações de pouso (lógica booleana)
FASE 3 — Relatório de status (pousados vs. em espera)
FASE 4 — Alertas pendentes (exibição LIFO)
FASE 5 — Buscas analíticas + previsão de consumo de combustível
```

---

## 🚀 Como Executar

**Pré-requisitos:** Python 3.x (sem dependências externas)

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/missao-aurora-siger.git
cd missao-aurora-siger

# Execute o simulador
python MGPEBPortugues.py
```

> Como combustível, peso e condições atmosféricas são gerados aleatoriamente, cada execução produz um resultado diferente.

---

## 📦 Bibliotecas Utilizadas

```python
import math        # Cálculo do decaimento exponencial
import random      # Geração de variáveis aleatórias de missão
from collections import deque  # Fila FIFO de alta performance
```

Apenas bibliotecas nativas do Python — **sem instalação adicional necessária**.

---

## 🌱 ESG e Governança

| Dimensão | Princípio | Implementação no MGPEB |
|---|---|---|
| Ambiental | Eficiência energética | `C(t)=C₀·e^(−kt)` + busca do menor combustível |
| Social | Segurança humana prioritária | Habitacional (prio.1) + Médico (prio.2) críticos |
| Governança | Auditabilidade | Diagnóstico explícito + pilha de alertas LIFO |
| Governança | Tolerância a falhas | Sensores independentes com falha aleatória simulada |
| Governança | Critérios objetivos | Lógica AND/OR sem intervenção humana subjetiva |

---

## 👤 Autor

**Renato Levy do Valle**  
FIAP — 2026

---

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos na FIAP.

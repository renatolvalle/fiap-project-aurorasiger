Antes de ler: Esse é um projeto feito para o curso de Ciência de Dados da Faculdade FIAP(Brazil) com propósito educacional. Apesar dos nomes dos arquivos estarem em ingles, o conteúdo dos assets estão em português. 

# Projeto Aurora-Siger - Versão em português

Sistema de simulação de verificação pré-lançamento que gera dados aleatórios de telemetria e autonomia energética, avalia cada parâmetro contra limiares operacionais e emite uma decisão de lançamento automatizada.

---

## Arquivos da pasta "assets" e descrição desse repositório

### `assets/docs`

aurora_siger_report_prompt.txt – Prompt utilizado para gerar o relatório de análise assistido por IA 
AuroraSiger-AI-Analysis.pdf – Análise gerada por IA incluindo classificação, identificação de dados, anomalias e riscos do projeto
AuroraSiger-PythonCode.pdf – Código Python completo em formato PDF
CriticalReflection.txt – Reflexão crítica sobre os benefícios e tecnologias gerados pelo projeto
pseudocode.txt – Pseudocódigo exigido pelo avaliador

### `assets/images`

Flowchart.png – Imagem do fluxograma exigido
Screenshot1.png – Captura de tela da saída de execução
Screenshot2.png – Captura de tela da saída de execução

### `Arquivos raiz`

FIAP_Aurora_Siger_Project_English.ipynb – Versão em notebook do projeto - Inglês
FIAP_Aurora_Siger_Project_Portuguese.ipynb – Versão em notebook do projeto - Português
[README.md](http://README.md) – Versão em português do README
[README-English.md](http://README-English.md) – Versão em inglês do README

## Sumário do projeto

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Estrutura do Código](#estrutura-do-código)
- [Parâmetros e Limiares](#parâmetros-e-limiares)
- [Lógica de Decisão](#lógica-de-decisão)
- [Como Executar](#como-executar)
- [Requisitos](#requisitos)

---

## Visão Geral

O Aurora-Siger simula o ciclo completo de verificação pré-lançamento de uma aeronave. A cada execução, valores aleatórios são gerados para variáveis de telemetria de bordo e autonomia energética. Cada variável é comparada com sua faixa operacional nominal e recebe um status individual. A decisão final de lançamento só é liberada se **todos** os parâmetros estiverem dentro dos limiares.

---

## Funcionalidades

- Geração aleatória de dados de telemetria (temperatura, pressão, integridade estrutural, módulos críticos)
- Cálculo de autonomia energética com base em capacidade, carga atual, consumo e perdas
- Avaliação individual de cada parâmetro com status `[ OK ]` ou falha
- Decisão automatizada de lançamento: `PRONTO PARA DECOLAR` ou `DECOLAGEM ABORTADA`
- Exibição interativa no terminal com pausas entre etapas

---

## Estrutura do Código

```
FIAP_Aurora_Siger_Project.ipynb
├── gerar_telemetria() - Gera e avalia os parâmetros de telemetria
├── calcular_autonomia() - Gera e avalia os parâmetros energéticos
└── Programa principal  - Chama as funções, decide e exibe os resultados
```

### `gerar_telemetria()`

Gera aleatoriamente variáveis de bordo e avalia cada uma contra seus limiares operacionais.

Retorna dois dicionários: `dados_telemetria` e `status_telemetria`.

---

### `calcular_autonomia()`

Calcula a autonomia energética da aeronave com base em valores sorteados e derivados.

Retorna dois dicionários: `dados_autonomia` e `status_autonomia`.

---

## Parâmetros e Limiares

Resumo completo de todos os parâmetros monitorados e suas condições de aprovação:

| Parâmetro               | Condição de aprovação  |
|-------------------------|------------------------|
| Temperatura interna     | 21 °C <= valor <= 30 °C|
| Temperatura externa     | -5 °C <= valor <= 30 °C|
| Integridade estrutural  | valor == 1             |
| Pressão dos tanques     | 95 <= valor <= 145 bar |
| Módulos críticos        | valor == 1             |
| Carga da bateria        | >= 80%                 |
| Energia útil            | >= 10 kWh              |
| Perda energética        | <= 5%                  |
| Autonomia               | >= 10 meses            |

---

## Lógica de Decisão

Após a avaliação de todos os parâmetros, os dicionários `status_telemetria` e `status_autonomia` são combinados. Se **todos** os valores forem `[ OK ]`, o lançamento é liberado. Qualquer falha resulta em no cancelamento da decolagem.

```python
decisao = 'PRONTO PARA DECOLAR' if all(
    s == '[ OK ]' for s in {**status_telemetria, **status_autonomia}.values()
) else 'DECOLAGEM ABORTADA'
```

---

## Como Executar

Nenhuma dependência externa é necessária. Apenas Python 3.6 ou superior.

```bash
python FIAP_Aurora_Siger_Project_Portuguese.ipynb
```

O programa solicita confirmações do usuário via `Enter` entre cada etapa, simulando um fluxo de verificação interativo.

---


## Requisitos

- Python 3.6+
- Módulo `random` (biblioteca padrão — nenhuma instalação necessária)

## Prints da execução
<<<<<<< HEAD:Phase1/README-Portuguese.md
![Screenshot1](./assets/images/Screenshot1.png)  
![Screenshot2](./assets/images/Screenshot2.png)  
=======
![Print1](./assets/Prints1.png)
![Print2](./assets/Prints2.png)
>>>>>>> 542636b0bc255b1be8bfe25b03b8a65692e6637f:README.md

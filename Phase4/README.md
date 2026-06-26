# SIGIC - Sistema Inteligente de Gerenciamento da Infraestrutura da Colônia

## Informação dos Desenvolvedores 

**Equipe:** ChronoCodex

```text
Nome: Renato Lima do Nascimento     - RM:570266
Nome: Renato Levy do Valle          - RM:572352 
Nome: Alexandre Martins Niewelt     - RM:570614
```

## Colônia Aurora Siger

Este projeto implementa o **SIGIC - Sistema Inteligente de Gerenciamento da Infraestrutura da Colônia**, desenvolvido para representar computacionalmente a infraestrutura energética e operacional da colônia marciana **Aurora Siger**.

O sistema utiliza conceitos de **grafos**, **estruturas de dados em Python**, **algoritmos de redes**, **modelagem matemática**, **otimização computacional**, **armazenamento e distribuição de energia**, **smart grids**, **sustentabilidade** e **governança tecnológica**.

A infraestrutura da colônia é representada por uma rede de módulos interligados. Cada módulo é tratado como um **vértice** do grafo, e cada conexão física entre módulos é tratada como uma **aresta ponderada**.

---

## Objetivo do projeto

O objetivo do SIGIC é simular e analisar o funcionamento da infraestrutura da colônia Aurora Siger, permitindo:

- visualizar a rede da colônia;
- consultar informações dos módulos;
- calcular caminhos mínimos entre módulos;
- explorar a rede por meio de BFS;
- verificar conectividade por meio de DFS;
- identificar conexões críticas da infraestrutura;
- projetar o crescimento do consumo energético;
- calcular a eficiência da distribuição de energia;
- simular falhas operacionais em módulos da base.

Dessa forma, o sistema auxilia na tomada de decisão sobre distribuição de energia, priorização de módulos críticos, planejamento de expansão e redução de desperdícios.

---

## Arquivo principal

O sistema foi desenvolvido em Python no arquivo:

```text
codigo_fonte.py
```

---

## Como executar o sistema

Para executar o projeto, abra o terminal na pasta onde está o arquivo Python e utilize:

```bash
python "codigo_fonte(1).py"
```

Ou, caso o arquivo esteja com o nome padronizado para entrega:

```bash
python codigo_fonte.py
```

O sistema será executado diretamente no terminal e exibirá um menu interativo para navegação.

---

## Menu principal do sistema

O sistema apresenta um menu simples de navegação no terminal:

```text
1  - Visualizar rede da colônia
2  - Consultar módulo
3  - Calcular caminho mínimo (Dijkstra)
4  - Explorar rede por saltos (BFS)
5  - Verificar conectividade e conexões críticas (DFS)
6  - Projetar crescimento do consumo energético
7  - Calcular eficiência da rede de distribuição
8  - Ver status operacional dos módulos
9  - Simular falha de um módulo
10 - Visualizar matriz de adjacência / pesos
0  - Encerrar sistema
```

Cada opção executa uma funcionalidade relacionada ao gerenciamento da infraestrutura da colônia.

---

## Infraestrutura da colônia

A colônia Aurora Siger é composta por 8 módulos principais:

| Módulo | Função principal |
|---|---|
| Habitação | Acomodação da tripulação e suporte básico à sobrevivência |
| Centro de Controle | Monitoramento e gerenciamento das operações da colônia |
| Armazenamento de Energia | Armazenamento e distribuição de energia da base |
| Agricultura | Produção de alimentos e apoio à sustentabilidade |
| Laboratório Científico | Pesquisas e análises de materiais e condições marcianas |
| Comunicação | Troca de dados entre módulos e comunicação com a Terra |
| Suporte Médico | Atendimento médico e monitoramento da saúde da tripulação |
| Produção de Oxigênio | Geração e distribuição de oxigênio para a base |

Cada módulo possui informações operacionais relevantes, como:

- consumo energético;
- prioridade operacional;
- capacidade de armazenamento;
- intervalo de comunicação;
- status operacional.

Esses dados são armazenados em um dicionário de dicionários chamado `modulos`.

---

## Representação da rede por grafos

A infraestrutura da colônia é representada como um **grafo ponderado**.

No código:

- os módulos são os **vértices**;
- as conexões físicas são as **arestas**;
- os pesos representam o custo de transmissão entre módulos;
- a rede é armazenada em uma **lista de adjacência**;
- também é criada uma **matriz de adjacência/pesos**.

A lista de adjacência é representada pela estrutura `grafo_colonia`, no formato:

```python
grafo_colonia = {
    "Modulo": [("Vizinho", peso), ...]
}
```

A matriz de pesos é criada pela função:

```python
criar_matriz_pesos(modulos, conexoes_distancia)
```

Ela permite visualizar as conexões diretas entre todos os pares de módulos.

---

## Fórmula do peso das conexões

O peso de cada conexão combina dois fatores:

1. distância física entre os módulos;
2. consumo energético do módulo de destino.

A fórmula usada no código é:

```text
peso = distancia * FATOR_PERDA + consumo_destino * FATOR_CONSUMO
```

Com os valores:

```text
FATOR_PERDA = 0.05
FATOR_CONSUMO = 0.08
```

Essa fórmula faz com que o sistema considere tanto a distância física quanto o custo energético do módulo atendido. Assim, o caminho calculado pelo Dijkstra não representa apenas o menor trajeto em metros, mas o menor custo operacional considerando energia e distância.

---

## Estruturas de dados utilizadas

O projeto utiliza estruturas nativas do Python, sem bibliotecas avançadas ou frameworks externos.

### Dicionários

Usados para armazenar os módulos e seus atributos:

```python
modulos = {
    "Habitacao": {
        "consumo_kwh": 12.0,
        "prioridade": 5,
        "capacidade_armazenamento_kwh": 20.0,
        "intervalo_comunicacao_seg": 30,
        "status": "ativo"
    }
}
```

A escolha do dicionário permite acessar os dados de cada módulo pelo nome.

### Listas

Usadas para armazenar:

- conexões entre módulos;
- fila do BFS;
- lista de módulos não visitados no Dijkstra;
- projeções de consumo energético;
- linhas da matriz de pesos.

### Tuplas

Usadas para representar informações fixas de conexão, como:

```python
("Centro de Controle", "Habitacao", 40)
```

E também pares de vizinho e peso na lista de adjacência:

```python
("Habitacao", 2.96)
```

### Matrizes

Usadas para representar a matriz de adjacência/pesos da rede.

Cada posição `matriz[i][j]` representa o peso da conexão direta entre dois módulos. Quando o valor é `0`, significa que não existe conexão direta.

### Conjuntos

Usados no DFS para marcar os módulos já visitados, evitando repetição e loops durante a exploração da rede.

---

## Algoritmos implementados

### BFS - Busca em Largura

A função responsável pela BFS é:

```python
bfs_distancia_em_saltos(grafo, origem)
```

Ela percorre a rede a partir de um módulo de origem e calcula quantos saltos são necessários para chegar aos demais módulos.

Essa análise ajuda a entender a estrutura da rede e a distância operacional entre os módulos.

---

### DFS - Busca em Profundidade

As funções relacionadas ao DFS são:

```python
dfs_visitar(grafo, atual, visitados)
verificar_conectividade(grafo, origem)
```

O DFS é usado para verificar se todos os módulos da colônia estão conectados. Se algum módulo não for visitado, significa que existe isolamento na rede.

Além disso, o DFS é usado junto com a remoção temporária de arestas para identificar conexões críticas.

---

### Detecção de conexões críticas

A função responsável por detectar conexões críticas é:

```python
detectar_conexoes_criticas(grafo, conexoes_lista)
```

Uma conexão crítica é uma conexão que, se removida, desconecta parte da rede.

No projeto, esse processo é feito da seguinte forma:

1. uma conexão é removida temporariamente;
2. o DFS verifica se a rede continua conectada;
3. se algum módulo ficar isolado, a conexão é marcada como crítica.

Essa análise é importante para a governança da infraestrutura, pois identifica pontos únicos de falha.

---

### Dijkstra - Caminho mínimo

A função responsável pelo algoritmo de Dijkstra é:

```python
dijkstra(grafo, origem)
```

O Dijkstra calcula o menor custo entre um módulo de origem e os demais módulos da rede.

No sistema, ele é usado para encontrar a rota mais eficiente entre dois módulos escolhidos pelo usuário no terminal.

A reconstrução da rota é feita pela função:

```python
reconstruir_rota(caminho_anterior, origem, destino)
```

Exemplo de uso esperado:

```text
Origem: Armazenamento de Energia
Destino: Suporte Médico
Resultado: Armazenamento de Energia -> Suporte Médico
Custo total da rota: calculado automaticamente pelo sistema
```

---

## Modelagem matemática

O projeto apresenta duas modelagens matemáticas principais.

---

### 1. Crescimento do consumo energético

O sistema utiliza um modelo de crescimento exponencial para projetar o consumo energético da colônia ao longo do tempo.

A fórmula utilizada é:

```text
C(t) = C0 * (1 + r)^t
```

Onde:

- `C(t)` é o consumo projetado no mês `t`;
- `C0` é o consumo total atual da colônia;
- `r` é a taxa mensal de crescimento;
- `t` é o tempo em meses.

No código, a taxa adotada é:

```text
r = 0.04
```

Ou seja, o consumo cresce 4% ao mês.

A função responsável pela projeção é:

```python
projetar_consumo(consumo_inicial, taxa, meses)
```

Essa modelagem ajuda a prever se a infraestrutura energética atual será suficiente para suportar a expansão futura da colônia.

---

### 2. Eficiência da distribuição de energia

O sistema também calcula a eficiência da rede de distribuição de energia.

A fórmula utilizada é:

```text
E = (Energia_enviada - Perda_total) / Energia_enviada * 100
```

Onde:

- `Energia_enviada` é a soma do consumo dos módulos atendidos;
- `Perda_total` é a soma dos custos das rotas mínimas calculadas pelo Dijkstra;
- `E` é a eficiência percentual da rede.

A função responsável é:

```python
calcular_eficiencia_rede(grafo, modulos_dict, origem)
```

Quanto mais próximo de 100%, menor é o desperdício de energia na rede.

---

## Simulação operacional

O sistema permite simular a falha completa de um módulo da colônia.

A função responsável é:

```python
simular_falha_modulo(modulos, conexoes_distancia, modulo_falho)
```

Durante a simulação:

1. o módulo escolhido é removido temporariamente da rede;
2. o grafo é reconstruído sem esse módulo;
3. o DFS verifica se a rede continua conectada;
4. o sistema informa se algum módulo ficou isolado.

Essa funcionalidade permite avaliar riscos operacionais e planejar melhorias na infraestrutura.

---

## Sustentabilidade e governança

O SIGIC contribui para uma gestão mais sustentável e responsável da infraestrutura da colônia.

### Uso sustentável de energia

A fórmula de peso das conexões penaliza trajetos longos e módulos de maior consumo. Isso incentiva o uso de rotas mais eficientes e reduz desperdícios energéticos.

### Priorização de sistemas críticos

Os módulos de prioridade máxima recebem atenção especial, pois estão relacionados à sobrevivência da tripulação e à operação essencial da base.

Entre eles estão:

- Habitação;
- Centro de Controle;
- Armazenamento de Energia;
- Suporte Médico;
- Produção de Oxigênio.

### Expansão organizada

A modelagem de crescimento de consumo permite simular o impacto da expansão antes da construção de novos módulos.

### Redução de desperdícios

O cálculo de eficiência da rede mostra o quanto de energia é perdido nas rotas, permitindo analisar a topologia da rede e propor melhorias.

### Governança tecnológica

A detecção de conexões críticas permite identificar pontos vulneráveis da infraestrutura e orientar decisões de manutenção, redundância e expansão.

---

## Exemplos de execução

### Exemplo 1 - Visualizar rede

Ao selecionar a opção `1`, o sistema exibe cada módulo e suas conexões diretas com os respectivos pesos.

```text
[Centro de Controle]
   -> Habitacao (peso: 2.96)
   -> Armazenamento de Energia (peso: 1.58)
   -> Comunicacao (peso: 1.48)
```

### Exemplo 2 - Calcular caminho mínimo

Ao selecionar a opção `3`, o usuário escolhe um módulo de origem e um módulo de destino. O sistema calcula a rota mais eficiente usando Dijkstra.

```text
Rota mais eficiente de 'Armazenamento de Energia' até 'Suporte Medico':
   Armazenamento de Energia -> Suporte Medico
Custo total da rota: 3.47
```

### Exemplo 3 - Explorar rede com BFS

Ao selecionar a opção `4`, o sistema mostra a distância em saltos entre o módulo de origem e os demais módulos.

```text
Distância em saltos a partir de 'Centro de Controle':
   Centro de Controle          -> 0 salto(s)
   Habitacao                   -> 1 salto(s)
   Comunicacao                 -> 1 salto(s)
```

### Exemplo 4 - Verificar conexões críticas

Ao selecionar a opção `5`, o sistema verifica se a rede está conectada e identifica conexões críticas.

```text
A rede está totalmente conectada. Todos os módulos são alcançáveis.
Analisando conexões críticas...
```

### Exemplo 5 - Simular falha

Ao selecionar a opção `9`, o usuário escolhe um módulo e o sistema simula sua falha completa.

```text
Simulando falha completa do módulo 'Agricultura'...
A rede permanece totalmente conectada mesmo após a falha.
```

---

## Bibliotecas utilizadas

O projeto utiliza apenas a biblioteca nativa:

```python
import math
```

A biblioteca `math` é utilizada para representar distâncias infinitas no algoritmo de Dijkstra com `math.inf`.

Não são utilizadas bibliotecas externas, frameworks ou recursos avançados.

---

## Conclusão

O SIGIC demonstra como os conceitos de grafos, estruturas de dados, algoritmos de redes e modelagem matemática podem ser aplicados ao gerenciamento de uma infraestrutura crítica em uma colônia marciana.

Por meio do uso de BFS, DFS e Dijkstra, o sistema permite analisar conectividade, caminhos mínimos, conexões críticas e eficiência operacional. Além disso, a modelagem de consumo energético e o cálculo de eficiência contribuem para decisões mais sustentáveis, organizadas e responsáveis dentro da Aurora Siger.

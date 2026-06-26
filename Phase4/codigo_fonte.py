# =============================================================================
# SIGIC - SISTEMA INTELIGENTE DE GERENCIAMENTO DA INFRAESTRUTURA DA COLONIA
# Colonia: Aurora Siger (Marte)
# Atividade Integradora - FIAP
# =============================================================================
# Este sistema representa computacionalmente a infraestrutura da colonia
# Aurora Siger usando um grafo, onde cada modulo da base e um vertice e cada
# conexao fisica entre modulos (cabo de energia / rede de dados) e uma aresta
# com peso. O peso representa o custo de transmissao entre dois modulos,
# calculado a partir da distancia fisica e da perda energetica do trajeto.
#
# Nao sao utilizadas bibliotecas externas nem classes (orientacao a objetos),
# apenas estruturas nativas do Python: dicionarios, listas e tuplas.
# =============================================================================

import math

# -----------------------------------------------------------------------------
# 1. ESTRUTURA DE DADOS DA REDE
# -----------------------------------------------------------------------------
# Cada modulo e representado como uma chave em um dicionario. O valor associado
# e outro dicionario contendo os atributos do modulo (consumo, prioridade,
# capacidade de armazenamento, status etc). Usamos dicionario (e nao lista)
# porque precisamos acessar os dados de um modulo pelo NOME dele em tempo
# constante O(1), sem precisar percorrer a estrutura toda.
# -----------------------------------------------------------------------------

modulos = {
    "Habitacao": {
        "consumo_kwh": 12.0,
        "prioridade": 5,
        "capacidade_armazenamento_kwh": 20.0,
        "intervalo_comunicacao_seg": 30,
        "status": "ativo"
    },
    "Centro de Controle": {
        "consumo_kwh": 8.0,
        "prioridade": 5,
        "capacidade_armazenamento_kwh": 10.0,
        "intervalo_comunicacao_seg": 5,
        "status": "ativo"
    },
    "Armazenamento de Energia": {
        "consumo_kwh": 1.0,
        "prioridade": 5,
        "capacidade_armazenamento_kwh": 150.0,
        "intervalo_comunicacao_seg": 10,
        "status": "ativo"
    },
    "Agricultura": {
        "consumo_kwh": 15.0,
        "prioridade": 4,
        "capacidade_armazenamento_kwh": 5.0,
        "intervalo_comunicacao_seg": 60,
        "status": "ativo"
    },
    "Laboratorio Cientifico": {
        "consumo_kwh": 10.0,
        "prioridade": 3,
        "capacidade_armazenamento_kwh": 8.0,
        "intervalo_comunicacao_seg": 90,
        "status": "ativo"
    },
    "Comunicacao": {
        "consumo_kwh": 6.0,
        "prioridade": 4,
        "capacidade_armazenamento_kwh": 4.0,
        "intervalo_comunicacao_seg": 5,
        "status": "ativo"
    },
    "Suporte Medico": {
        "consumo_kwh": 9.0,
        "prioridade": 5,
        "capacidade_armazenamento_kwh": 12.0,
        "intervalo_comunicacao_seg": 15,
        "status": "ativo"
    },
    "Producao de Oxigenio": {
        "consumo_kwh": 14.0,
        "prioridade": 5,
        "capacidade_armazenamento_kwh": 6.0,
        "intervalo_comunicacao_seg": 10,
        "status": "ativo"
    }
}

# -----------------------------------------------------------------------------
# 2. REPRESENTACAO DO GRAFO (LISTA DE ADJACENCIA)
# -----------------------------------------------------------------------------
# A rede e representada como uma lista de adjacencia usando dicionario de
# listas de tuplas: { modulo: [(modulo_vizinho, peso), ...], ... }
# Cada tupla guarda (vizinho, peso) - usamos tupla porque essa relacao
# (vizinho, peso) e fixa e nao deve ser alterada depois de criada.
#
# O peso da aresta combina dois fatores, conforme pedido na atividade (item 1.2):
#   - distancia fisica entre os modulos (em metros)
#   - consumo energetico do modulo de destino (em kW)
#
# Formula do peso:
#   peso = distancia * FATOR_PERDA + consumo_kwh * FATOR_CONSUMO
#
# Isso faz com que o Dijkstra nao escolha apenas o caminho mais curto em
# metros, mas o caminho mais barato em termos de energia tambem - ou seja,
# liga modulos proximos E que nao desperdicam energia no trajeto.
# -----------------------------------------------------------------------------

FATOR_PERDA = 0.05      # perda energetica por metro de cabo (kWh por metro)
FATOR_CONSUMO = 0.08    # peso dado ao consumo do modulo de destino

# distancias fisicas reais entre os modulos da base (em metros)
conexoes_distancia = [
    ("Centro de Controle", "Habitacao", 40),
    ("Centro de Controle", "Armazenamento de Energia", 30),
    ("Centro de Controle", "Comunicacao", 20),
    ("Centro de Controle", "Laboratorio Cientifico", 50),
    ("Armazenamento de Energia", "Habitacao", 35),
    ("Armazenamento de Energia", "Agricultura", 60),
    ("Armazenamento de Energia", "Producao de Oxigenio", 45),
    ("Armazenamento de Energia", "Suporte Medico", 55),
    ("Habitacao", "Suporte Medico", 25),
    ("Habitacao", "Producao de Oxigenio", 30),
    ("Laboratorio Cientifico", "Comunicacao", 15),
    ("Suporte Medico", "Laboratorio Cientifico", 35),
]


def calcular_peso(distancia, consumo_destino):
    """Calcula o peso (custo) de uma conexao a partir da distancia fisica
    e do consumo energetico do modulo de destino."""
    return round(distancia * FATOR_PERDA + consumo_destino * FATOR_CONSUMO, 2)


def montar_grafo(modulos_dict, conexoes_lista):
    """Monta a lista de adjacencia do grafo a partir das conexoes fisicas.
    O grafo e nao-direcionado: se A se conecta a B, B tambem se conecta a A,
    pois o cabo de energia transmite nos dois sentidos."""
    grafo = {modulo: [] for modulo in modulos_dict}

    for origem, destino, distancia in conexoes_lista:
        peso_ida = calcular_peso(distancia, modulos_dict[destino]["consumo_kwh"])
        peso_volta = calcular_peso(distancia, modulos_dict[origem]["consumo_kwh"])
        grafo[origem].append((destino, peso_ida))
        grafo[destino].append((origem, peso_volta))

    return grafo


grafo_colonia = montar_grafo(modulos, conexoes_distancia)

# -----------------------------------------------------------------------------
# 2.1 MATRIZ DE ADJACENCIA / MATRIZ DE PESOS
# -----------------------------------------------------------------------------
# Alem da lista de adjacencia, tambem representamos a rede usando uma matriz.
# A matriz permite visualizar as conexoes entre todos os pares de modulos.
#
# Cada linha e cada coluna representam um modulo da colonia.
# Se matriz[i][j] = 0, significa que nao existe conexao direta entre os modulos.
# Se matriz[i][j] > 0, o valor representa o peso da conexao entre eles.
#
# -----------------------------------------------------------------------------

def criar_matriz_pesos(modulos_dict, conexoes_lista):
    """Cria uma matriz de pesos a partir das conexoes da rede.

    Cada posicao matriz[i][j] representa o peso da conexao entre
    o modulo i e o modulo j. Quando nao existe conexao direta,
    o valor fica como 0.
    """

    nomes_modulos = list(modulos_dict.keys())
    tamanho = len(nomes_modulos)

    # Cria uma matriz quadrada preenchida com zero
    matriz = []
    for i in range(tamanho):
        linha = []
        for j in range(tamanho):
            linha.append(0)
        matriz.append(linha)

    # Preenche a matriz com os pesos das conexoes existentes
    for origem, destino, distancia in conexoes_lista:
        indice_origem = nomes_modulos.index(origem)
        indice_destino = nomes_modulos.index(destino)

        peso_ida = calcular_peso(distancia, modulos_dict[destino]["consumo_kwh"])
        peso_volta = calcular_peso(distancia, modulos_dict[origem]["consumo_kwh"])

        matriz[indice_origem][indice_destino] = peso_ida
        matriz[indice_destino][indice_origem] = peso_volta

    return nomes_modulos, matriz


nomes_modulos_matriz, matriz_pesos = criar_matriz_pesos(modulos, conexoes_distancia)


# -----------------------------------------------------------------------------
# 3. ALGORITMO BFS (BUSCA EM LARGURA)
# -----------------------------------------------------------------------------
# Usado para explorar a rede "por camadas", a partir de um modulo de origem.
# Aqui aplicamos o BFS para responder a pergunta operacional:
# "quantos saltos (conexoes) separam o modulo X de todos os outros modulos?"
# Isso e util para avaliar a robustez da rede: modulos muito distantes em
# numero de saltos sao mais vulneraveis a falhas em cascata.
#
# Usamos uma LISTA como fila (fila FIFO manual com pop(0)) para controlar a
# ordem de visita, e um dicionario para guardar a distancia em saltos de
# cada modulo ate a origem.
# -----------------------------------------------------------------------------

def bfs_distancia_em_saltos(grafo, origem):
    """Percorre o grafo em largura a partir da origem e retorna um dicionario
    com o numero de saltos (arestas) ate cada modulo alcancavel."""
    visitados = {origem: 0}
    fila = [origem]

    while fila:
        atual = fila.pop(0)
        for vizinho, peso in grafo[atual]:
            if vizinho not in visitados:
                visitados[vizinho] = visitados[atual] + 1
                fila.append(vizinho)

    return visitados


# -----------------------------------------------------------------------------
# 4. ALGORITMO DFS (BUSCA EM PROFUNDIDADE)
# -----------------------------------------------------------------------------
# Usado para verificar a CONECTIVIDADE da rede, ou seja, se todos os modulos
# estao alcancaveis a partir de um ponto qualquer. Se o DFS nao visitar todos
# os modulos, significa que existe um modulo isolado (sem conexao com o
# restante da base) - uma falha critica de infraestrutura.
#
# Implementado de forma recursiva, usando um conjunto (set) para marcar
# modulos ja visitados e evitar loops infinitos.
# -----------------------------------------------------------------------------

def dfs_visitar(grafo, atual, visitados):
    """Marca o modulo atual como visitado e chama a si mesma recursivamente
    para cada vizinho ainda nao visitado."""
    visitados.add(atual)
    for vizinho, peso in grafo[atual]:
        if vizinho not in visitados:
            dfs_visitar(grafo, vizinho, visitados)
    return visitados


def verificar_conectividade(grafo, origem):
    """Retorna (True, []) se todos os modulos forem alcancaveis a partir da
    origem, ou (False, lista_de_isolados) caso existam modulos isolados."""
    visitados = dfs_visitar(grafo, origem, set())
    isolados = [modulo for modulo in grafo if modulo not in visitados]
    return (len(isolados) == 0, isolados)


# -----------------------------------------------------------------------------
# 5. ALGORITMO DE DIJKSTRA (CAMINHO MINIMO)
# -----------------------------------------------------------------------------
# Calcula a rota de menor custo (energia + distancia) entre o modulo de
# Armazenamento de Energia e qualquer outro modulo da base. E o algoritmo
# central do sistema: e ele que decide por onde a energia deve ser roteada
# para chegar ao destino com o menor desperdicio possivel.
#
# Implementacao manual sem biblioteca externa (sem heapq), usando um
# dicionario de distancias e busca linear pelo menor valor nao visitado a
# cada iteracao - abordagem compativel com o conteudo estudado ate esta fase.
# -----------------------------------------------------------------------------

def dijkstra(grafo, origem):
    """Calcula a menor distancia (custo) da origem ate todos os outros
    modulos, alem do caminho (rota) percorrido para cada um."""
    distancias = {modulo: math.inf for modulo in grafo}
    caminho_anterior = {modulo: None for modulo in grafo}
    distancias[origem] = 0
    nao_visitados = list(grafo.keys())

    while nao_visitados:
        # busca o modulo nao visitado com menor distancia acumulada
        atual = min(nao_visitados, key=lambda modulo: distancias[modulo])
        nao_visitados.remove(atual)

        # se a menor distancia restante e infinita, os modulos restantes
        # sao inalcancaveis a partir da origem
        if distancias[atual] == math.inf:
            break

        for vizinho, peso in grafo[atual]:
            nova_distancia = distancias[atual] + peso
            if nova_distancia < distancias[vizinho]:
                distancias[vizinho] = nova_distancia
                caminho_anterior[vizinho] = atual

    return distancias, caminho_anterior


def reconstruir_rota(caminho_anterior, origem, destino):
    """Reconstroi a rota completa (lista de modulos, na ordem) a partir do
    dicionario de predecessores gerado pelo Dijkstra."""
    rota = []
    atual = destino

    while atual is not None:
        rota.append(atual)
        atual = caminho_anterior[atual]

    rota.reverse()

    if rota[0] != origem:
        return None  # nao existe caminho da origem ate o destino

    return rota


# -----------------------------------------------------------------------------
# 6. DETECCAO DE CONEXOES CRITICAS (PONTES DA REDE)
# -----------------------------------------------------------------------------
# Uma conexao critica (ou "ponte") e aquela que, se removida, desconecta a
# rede em duas partes - ou seja, isola um ou mais modulos. Identificar essas
# conexoes e essencial para a governanca da infraestrutura, pois mostra quais
# cabos NAO podem falhar sem comprometer modulos inteiros.
#
# Estrategia (compativel com o conteudo da fase): para cada aresta da rede,
# removemos ela temporariamente e rodamos o DFS de novo a partir de um modulo
# fixo. Se o numero de modulos alcancados cair, a aresta e uma ponte critica.
# -----------------------------------------------------------------------------

def listar_arestas_unicas(conexoes_lista):
    """Retorna a lista de conexoes fisicas (sem duplicar ida/volta)."""
    return [(origem, destino) for origem, destino, distancia in conexoes_lista]


def remover_aresta_temporariamente(grafo, origem, destino):
    """Cria uma copia do grafo sem a aresta origem-destino (e destino-origem),
    para testar o impacto da remocao sem alterar o grafo original."""
    grafo_temp = {modulo: list(vizinhos) for modulo, vizinhos in grafo.items()}
    grafo_temp[origem] = [(v, p) for v, p in grafo_temp[origem] if v != destino]
    grafo_temp[destino] = [(v, p) for v, p in grafo_temp[destino] if v != origem]
    return grafo_temp


def detectar_conexoes_criticas(grafo, conexoes_lista):
    """Testa cada conexao da rede e retorna a lista das que, se removidas,
    isolam algum modulo (conexoes criticas / pontes)."""
    criticas = []
    modulo_referencia = list(grafo.keys())[0]

    for origem, destino in listar_arestas_unicas(conexoes_lista):
        grafo_sem_aresta = remover_aresta_temporariamente(grafo, origem, destino)
        conectado, isolados = verificar_conectividade(grafo_sem_aresta, modulo_referencia)
        if not conectado:
            criticas.append((origem, destino, isolados))

    return criticas


# -----------------------------------------------------------------------------
# 7. MODELAGEM MATEMATICA - CRESCIMENTO DO CONSUMO ENERGETICO (FOCO PRINCIPAL)
# -----------------------------------------------------------------------------
# Modelo escolhido: crescimento EXPONENCIAL do consumo energetico da colonia
# conforme novos modulos sao adicionados a infraestrutura ao longo do tempo.
#
# Formula:
#   C(t) = C0 * (1 + r) ** t
#
# Onde:
#   C(t) = consumo total estimado da colonia no mes "t" (em kW)
#   C0   = consumo total atual da colonia (soma do consumo de todos os
#          modulos hoje, em kW)
#   r    = taxa mensal de crescimento da infraestrutura (expansao de modulos,
#          chegada de novos colonos, novos equipamentos)
#   t    = tempo em meses, a partir de hoje (t = 0)
#
# Justificativa do modelo: o crescimento de uma colonia espacial nao e linear
# -  cada novo modulo construido tende a exigir suporte de outros modulos
# (ex: mais habitacao => mais producao de oxigenio => mais consumo de energia
# em cascata), entao um modelo exponencial reflete melhor esse efeito composto
# do que um modelo linear simples.
# -----------------------------------------------------------------------------

TAXA_CRESCIMENTO_MENSAL = 0.04  # 4% de crescimento de consumo ao mes


def consumo_total_atual(modulos_dict):
    """Soma o consumo energetico (kW) de todos os modulos ativos da colonia."""
    return sum(dados["consumo_kwh"] for dados in modulos_dict.values()
               if dados["status"] == "ativo")


def projetar_consumo(consumo_inicial, taxa, meses):
    """Aplica o modelo de crescimento exponencial C(t) = C0 * (1 + r)^t e
    retorna uma lista de tuplas (mes, consumo_projetado_kw)."""
    projecao = []
    for t in range(meses + 1):
        consumo_t = consumo_inicial * ((1 + taxa) ** t)
        projecao.append((t, round(consumo_t, 2)))
    return projecao


def mes_em_que_excede_capacidade(projecao, capacidade_maxima_kw):
    """Analisa a projecao e retorna o primeiro mes em que o consumo
    ultrapassa a capacidade maxima de geracao/armazenamento da colonia.
    Retorna None se isso nao ocorrer dentro do periodo projetado."""
    for mes, consumo in projecao:
        if consumo > capacidade_maxima_kw:
            return mes
    return None


# -----------------------------------------------------------------------------
# 8. MODELAGEM MATEMATICA - EFICIENCIA DA DISTRIBUICAO DE ENERGIA (FOCO 2)
# -----------------------------------------------------------------------------
# Modelo escolhido: eficiencia da rede como razao entre a energia que
# efetivamente chega aos modulos e a energia total enviada pelo modulo de
# Armazenamento de Energia, descontando a perda no trajeto (calculada a
# partir do peso das arestas percorridas pelo Dijkstra).
#
# Formula:
#   E = (Energia_enviada - Perda_total) / Energia_enviada * 100
#
# Onde:
#   Energia_enviada = soma do consumo (kW) de todos os modulos atendidos
#   Perda_total      = soma do custo das arestas (peso) das rotas minimas
#                       calculadas pelo Dijkstra ate cada modulo
#   E                = eficiencia da rede, em percentual (%)
#
# Interpretacao: quanto mais proximo de 100%, mais eficiente e a topologia
# da rede (menos energia desperdicada em transmissao). Esse indicador e
# recalculado automaticamente sempre que a rota minima e recalculada,
# permitindo comparar diferentes topologias de rede ou cenarios de falha.
# -----------------------------------------------------------------------------

def calcular_eficiencia_rede(grafo, modulos_dict, origem):
    """Calcula a eficiencia da rede de distribuicao de energia a partir do
    modulo de origem, usando as rotas minimas do Dijkstra."""
    distancias, anteriores = dijkstra(grafo, origem)

    energia_enviada = 0.0
    perda_total = 0.0

    for modulo, dados in modulos_dict.items():
        if modulo == origem:
            continue
        if distancias[modulo] == math.inf:
            continue  # modulo inalcancavel nao entra no calculo
        energia_enviada += dados["consumo_kwh"]
        perda_total += distancias[modulo]

    if energia_enviada == 0:
        return 0.0

    eficiencia = (energia_enviada - perda_total) / energia_enviada * 100
    return round(max(eficiencia, 0.0), 2)


# -----------------------------------------------------------------------------
# 9. SIMULACAO DE SITUACOES OPERACIONAIS
# -----------------------------------------------------------------------------
# Simula um cenario de falha: um modulo cai (status = "em manutencao" ou
# "em alerta") e o sistema recalcula a rede sem ele, avaliando se a colonia
# continua operacional (conectividade mantida) e quais modulos ficam sem
# energia.
# -----------------------------------------------------------------------------

def simular_falha_modulo(modulos_dict, conexoes_lista, modulo_falho):
    """Remove um modulo da rede (simulando falha total) e reconstroi o grafo
    sem ele, retornando o novo grafo e a lista de modulos que ficaram
    isolados como consequencia direta da falha."""
    modulos_restantes = {m: d for m, d in modulos_dict.items() if m != modulo_falho}
    conexoes_restantes = [
        (o, d, dist) for o, d, dist in conexoes_lista
        if o != modulo_falho and d != modulo_falho
    ]

    grafo_simulado = montar_grafo(modulos_restantes, conexoes_restantes)

    if not grafo_simulado:
        return grafo_simulado, []

    referencia = list(grafo_simulado.keys())[0]
    conectado, isolados = verificar_conectividade(grafo_simulado, referencia)

    return grafo_simulado, isolados


def gerar_relatorio_status(modulos_dict):
    """Gera uma lista de strings com o status atual de cada modulo,
    formatada para exibicao no terminal."""
    linhas = []
    for nome, dados in modulos_dict.items():
        linha = (f"{nome:<28} | status: {dados['status']:<8} | "
                  f"consumo: {dados['consumo_kwh']:>5.1f} kWh | "
                  f"prioridade: {dados['prioridade']} | "
                  f"comunicacao: a cada {dados['intervalo_comunicacao_seg']}s")
        linhas.append(linha)
    return linhas



# =============================================================================
# 10. EXIBIR MATRIZ DE ADJACENCIA
# =============================================================================

def menu_matriz_pesos():
    exibir_cabecalho("MATRIZ DE ADJACENCIA / PESOS DA REDE")

    print("Legenda dos indices:")
    for i, nome in enumerate(nomes_modulos_matriz):
        print(f"{i} - {nome}")

    print("\nMatriz de pesos:")
    print("Cada valor representa o peso da conexao direta entre dois modulos.")
    print("Valor 0 significa que nao existe conexao direta.\n")

    print("       ", end="")
    for i in range(len(nomes_modulos_matriz)):
        print(f"{i:^8}", end="")
    print()

    for i, linha in enumerate(matriz_pesos):
        print(f"{i:^7}", end="")
        for valor in linha:
            print(f"{valor:^8}", end="")
        print()



# =============================================================================
# 11. INTERFACE DE TERMINAL (MENU DE NAVEGACAO)
# =============================================================================

def selecionar_modulo_por_numero(titulo="SELECIONAR MODULO"):
    """Exibe os modulos disponiveis numerados e retorna o modulo escolhido.
    O usuario escolhe pelo numero, evitando erros de digitacao no nome
    exato do modulo."""

    exibir_cabecalho(titulo)

    lista_modulos = list(modulos.keys())

    print("Modulos disponiveis:")
    for indice, nome in enumerate(lista_modulos, start=1):
        print(f"{indice} - {nome}")

    try:
        escolha = int(input("\nDigite o numero do modulo: "))
    except ValueError:
        print("\nEntrada invalida. Digite apenas um numero.")
        return None

    if escolha < 1 or escolha > len(lista_modulos):
        print("\nNumero invalido. Escolha uma opcao da lista.")
        return None

    modulo_escolhido = lista_modulos[escolha - 1]
    return modulo_escolhido


def exibir_cabecalho(titulo):
    print("\n" + "=" * 70)
    print(titulo.center(70))
    print("=" * 70)


def menu_visualizar_rede():
    exibir_cabecalho("REDE DA COLONIA AURORA SIGER")
    for modulo, vizinhos in grafo_colonia.items():
        print(f"\n[{modulo}]")
        if not vizinhos:
            print("   (sem conexoes diretas)")
        for vizinho, peso in vizinhos:
            print(f"   -> {vizinho}  (peso: {peso})")


def menu_consultar_modulo():
    escolha = selecionar_modulo_por_numero("CONSULTAR MODULO")

    if escolha is None:
        return

    dados = modulos[escolha]
    
    print(f"\n--- {escolha} ---")
    print(f"Consumo energetico:       {dados['consumo_kwh']} kWh")
    print(f"Prioridade operacional:   {dados['prioridade']} (1 a 5)")
    print(f"Capacidade armazenamento: {dados['capacidade_armazenamento_kwh']} kWh")
    print(f"Intervalo comunicacao:    {dados['intervalo_comunicacao_seg']} segundos")
    print(f"Status:                   {dados['status']}")

    conexoes_diretas = grafo_colonia[escolha]
    print(f"Conexoes diretas:         {len(conexoes_diretas)}")
    for vizinho, peso in conexoes_diretas:
        print(f"   -> {vizinho} (peso {peso})")


def menu_dijkstra():
       
    origem = selecionar_modulo_por_numero("ORIGEM DA ROTA")
    
    if origem is None:
        return

    
    destino = selecionar_modulo_por_numero("DESTINO DA ROTA")
    
    if destino is None:
        return
    
    if origem == destino:
        print("\nOrigem e destino sao o mesmo modulo. O custo da rota e 0.")
        return
    
    distancias, anteriores = dijkstra(grafo_colonia, origem)
    rota = reconstruir_rota(anteriores, origem, destino)

    if rota is None:
        print(f"\nNao existe rota disponivel entre '{origem}' e '{destino}'.")
        return

    print(f"\nRota mais eficiente de '{origem}' ate '{destino}':")
    print("   " + " -> ".join(rota))
    print(f"Custo total da rota (energia + distancia): {distancias[destino]}")


def menu_bfs():
    origem = selecionar_modulo_por_numero("EXPLORACAO DA REDE - BFS (SALTOS ATE CADA MODULO)")

    if origem is None:
        return

    resultado = bfs_distancia_em_saltos(grafo_colonia, origem)
    print(f"\nDistancia em saltos a partir de '{origem}':")
    for modulo, saltos in sorted(resultado.items(), key=lambda item: item[1]):
        print(f"   {modulo:<28} -> {saltos} salto(s)")


def menu_conectividade_e_criticas():
    exibir_cabecalho("CONECTIVIDADE E CONEXOES CRITICAS DA REDE")
    referencia = list(modulos.keys())[0]
    conectado, isolados = verificar_conectividade(grafo_colonia, referencia)

    if conectado:
        print("A rede esta totalmente conectada. Todos os modulos sao alcancaveis.")
    else:
        print("ALERTA: a rede possui modulos isolados:")
        for modulo in isolados:
            print(f"   - {modulo}")

    print("\nAnalisando conexoes criticas (pontes da rede)...")
    criticas = detectar_conexoes_criticas(grafo_colonia, conexoes_distancia)

    if not criticas:
        print("Nenhuma conexao critica encontrada. A rede possui rotas alternativas.")
    else:
        print(f"Foram encontradas {len(criticas)} conexao(oes) critica(s):")
        for origem, destino, isolados_resultantes in criticas:
            print(f"   - {origem} <-> {destino}  | isolaria: {', '.join(isolados_resultantes)}")


def menu_modelagem_consumo():
    exibir_cabecalho("MODELAGEM MATEMATICA - CRESCIMENTO DO CONSUMO")
    c0 = consumo_total_atual(modulos)
    print(f"Consumo total atual da colonia: {c0} kWh")
    print(f"Taxa de crescimento mensal assumida: {TAXA_CRESCIMENTO_MENSAL * 100:.1f}%")
    print("Projetar consumo para quantos meses? (padrao: 6 meses) ")

    try:
        meses = int(input("\nProjetar consumo para quantos meses? "))
    except ValueError:
        print("Valor invalido, usando 6 meses como padrao.")
        meses = 6

    projecao = projetar_consumo(c0, TAXA_CRESCIMENTO_MENSAL, meses)
    print(f"\nProjecao de consumo (C(t) = {c0} * (1 + {TAXA_CRESCIMENTO_MENSAL})^t):")
    for mes, consumo in projecao:
        print(f"   Mes {mes:>2}: {consumo:>8.2f} kWh")

    capacidade_total = sum(d["capacidade_armazenamento_kwh"] for d in modulos.values())
    mes_critico = mes_em_que_excede_capacidade(projecao, capacidade_total)

    print(f"\nCapacidade total de armazenamento da colonia: {capacidade_total} kWh")
    if mes_critico is not None:
        print(f"ALERTA: no mes {mes_critico}, o consumo projetado ultrapassa "
              f"a capacidade de armazenamento da colonia.")
    else:
        print("Dentro do periodo projetado, a capacidade nao e excedida.")


def menu_eficiencia_rede():
    exibir_cabecalho("MODELAGEM MATEMATICA - EFICIENCIA DA REDE")
    origem = "Armazenamento de Energia"
    eficiencia = calcular_eficiencia_rede(grafo_colonia, modulos, origem)
    print(f"Eficiencia atual da rede de distribuicao (a partir de '{origem}'): "
          f"{eficiencia}%")
    print("\nFormula: E = (Energia_enviada - Perda_total) / Energia_enviada * 100")
    print("Quanto mais proximo de 100%, menor o desperdicio de energia na rede.")


def menu_status_geral():
    exibir_cabecalho("STATUS OPERACIONAL DOS MODULOS")
    for linha in gerar_relatorio_status(modulos):
        print(linha)


def menu_simular_falha():
    alvo = selecionar_modulo_por_numero("SIMULACAO DE FALHA DE MODULO")

    if alvo is None:
        return

    if modulos[alvo]["prioridade"] == 5:
        print(f"\nATENCAO: '{alvo}' e um modulo de prioridade maxima (5). "
              f"Sua falha e considerada critica para a sobrevivencia da colonia.")

    grafo_simulado, isolados = simular_falha_modulo(modulos, conexoes_distancia, alvo)

    print(f"\nSimulando falha completa do modulo '{alvo}'...")
    if not isolados:
        print("A rede permanece totalmente conectada mesmo apos a falha.")
    else:
        print("Como consequencia da falha, os seguintes modulos ficaram isolados:")
        for modulo in isolados:
            print(f"   - {modulo}")


def exibir_menu_principal():
    print("\n" + "=" * 70)
    print("SIGIC - SISTEMA INTELIGENTE DE GERENCIAMENTO DA INFRAESTRUTURA".center(70))
    print("COLONIA AURORA SIGER".center(70))
    print("=" * 70)
    print("1 - Visualizar rede da colonia")
    print("2 - Consultar modulo")
    print("3 - Calcular caminho minimo (Dijkstra)")
    print("4 - Explorar rede por saltos (BFS)")
    print("5 - Verificar conectividade e conexoes criticas (DFS)")
    print("6 - Projetar crescimento do consumo energetico")
    print("7 - Calcular eficiencia da rede de distribuicao")
    print("8 - Ver status operacional dos modulos")
    print("9 - Simular falha de um modulo")
    print("10 - Visualizar matriz de adjacencia / pesos")
    print("0 - Encerrar sistema")


def main():
    """Loop principal do sistema: exibe o menu e direciona para a
    funcionalidade escolhida pelo usuario ate que ele opte por sair."""
    opcoes = {
        "1": menu_visualizar_rede,
        "2": menu_consultar_modulo,
        "3": menu_dijkstra,
        "4": menu_bfs,
        "5": menu_conectividade_e_criticas,
        "6": menu_modelagem_consumo,
        "7": menu_eficiencia_rede,
        "8": menu_status_geral,
        "9": menu_simular_falha,
        "10": menu_matriz_pesos,
    }

    while True:
        exibir_menu_principal()
        opcao = input("\nEscolha uma opcao: ").strip().lower()

        if opcao == "0":
            print("\nEncerrando o SIGIC. Ate a proxima transmissao, Aurora Siger.")
            break
        elif opcao in opcoes:
            opcoes[opcao]()
        else:
            print("\nOpcao invalida. Tente novamente.")

        input("\nPressione ENTER para voltar ao menu...")


if __name__ == "__main__":
    main()

"""
# Missão Aurora Siger | Protótipo em Python
# MGPEB - Módulo de Gerenciamento de Pouso e Estabilização de Base
"""
# Importando bibliotecas
import math
import random
from collections import deque


# 1. DEFINIÇÃO DOS MÓDULOS DE POUSO

modulos = [
    {
        "Nome": "Módulo Habitacional",
        "Prioridade": 1,
        "Combustivel": round(random.uniform(20, 99), 1),
        "Peso": round(random.uniform(5, 35), 1),
        "Modulo Critico": True,
        "TCA": 2
    },
    {
        "Nome": "Módulo de Energia Solar",
        "Prioridade": 2,
        "Combustivel": round(random.uniform(20, 99), 1),
        "Peso": round(random.uniform(5, 35), 1),
        "Modulo Critico": True,
        "TCA": 4
    },
    {
        "Nome": "Módulo de Laboratório Científico",
        "Prioridade": 3,
        "Combustivel": round(random.uniform(20, 99), 1),
        "Peso": round(random.uniform(5, 35), 1),
        "Modulo Critico": False,
        "TCA": 6
    },
    {
        "Nome": "Módulo de Suprimentos",
        "Prioridade": 4,
        "Combustivel": round(random.uniform(20, 99), 1),
        "Peso": round(random.uniform(5, 15), 1),
        "Modulo Critico": False,
        "TCA": 8
    },
    {
        "Nome": "Módulo de Suprimentos Médicos",
        "Prioridade": 2,
        "Combustivel": round(random.uniform(20, 99), 1),
        "Peso": round(random.uniform(5, 15), 1),
        "Modulo Critico": True,
        "TCA": 5
    },
]


# 2. FUNÇÕES BOOLEANAS / REGRAS DE DECISÃO

def combustivel_suficiente(modulo):
    return modulo["Combustivel"] >= 40

def condicoes_atmosfericas_ok():
    tempestade = not random.choice([True, False])
    return tempestade

def area_de_pouso():
    area_livre = random.choice([True, False])
    return area_livre

def sensores_de_pouso(sensores_nave):
    sensores = all(sensores_nave.values())
    return sensores

def autorizar_pouso(modulo, tempestade, area_livre, sensores):
# Para módulos COM carga crítica: TODOS os critérios devem ser verdadeiros (AND).
# Para módulos SEM carga crítica: combustível + (atmosfera OU área disponível).
    combustivel_ok = combustivel_suficiente(modulo)
    atm_ok         = tempestade
    area_ok        = area_livre
    sensor_ok      = sensores

    if modulo["Modulo Critico"]:
        autorizado = combustivel_ok and atm_ok and area_ok and sensor_ok
    else:
        autorizado = combustivel_ok and sensor_ok and (atm_ok or area_ok)

    # Diagnóstico
    if not autorizado:
        motivos = []  # Lista com os motivos da negação
        if not combustivel_ok:
            motivos.append("Combustível crítico (<40%)")
        if not atm_ok:
            motivos.append("Tempestade atmosférica ativa")
        if not area_ok:
            motivos.append("Área de pouso obstruída")
        if not sensor_ok:
            motivos.append("Falha nos sensores")
        return False, " | ".join(motivos)

    return True, "Todas condições satisfeitas"


# 3. ALGORITMOS DE BUSCA

def buscar_menor_combustivel(lista_combustivel):

    if not lista_combustivel: # se não houver módulos na lista, retorna None
        return None
    minimo = lista_combustivel[0]
    for m in lista_combustivel[1:]: # percorre a lista a partir do segundo elemento
        if m["Combustivel"] < minimo["Combustivel"]: #  compara o combustível do módulo atual com o mínimo encontrado
            minimo = m
    return minimo

def buscar_maior_prioridade(lista_prioridade):

    if not lista_prioridade:
        return None
    mais_urgente = lista_prioridade[0]
    for m in lista_prioridade[1:]:
        if m["Prioridade"] < mais_urgente["Prioridade"]: # menor número = maior prioridade
            mais_urgente = m
    return mais_urgente


# 4. ALGORITMO DE ORDENAÇÃO

def ordenar_por_prioridade(lista_para_ordenar):

    lista_ordenada = lista_para_ordenar.copy()  # cópia para não modificar o original
    for i in range(1, len(lista_ordenada)): # começa a partir do segundo elemento
        chave = lista_ordenada[i] # elemento para comparação
        j = i - 1 # índice do elemento anterior
        while j >= 0 and lista_ordenada[j]["Prioridade"] > chave["Prioridade"]: # compara a prioridade do elemento atual com os anteriores
            lista_ordenada[j + 1] = lista_ordenada[j] # move o elemento maior para a direita
            j -= 1 # continua comparando com os elementos anteriores
        lista_ordenada[j + 1] = chave # insere o elemento na posição correta
    return lista_ordenada

# ─────────────────────────────────────────────
# 5. MODELAGEM MATEMÁTICA — Consumo de Combustível
# ─────────────────────────────────────────────
# Modelo: consumo decrescente exponencialmente durante a descida
# C(t) = C0 * e^(-k * t)
# onde:
#   C0 = combustível inicial (%)
#   k  = taxa de consumo (por hora)
#   t  = tempo decorrido (horas)
# Quanto maior a velocidade de descida, maior o k.

def consumir_combustivel(c0, k, t):  # Retorna o nível de combustível após t horas de descida
    return c0 * math.exp(-k * t)


# 6. ESTRUTURAS DE DADOS LINEARES

modulos_pousados = []    # Lista para armazenar módulos pousados com sucesso
modulos_em_espera = []   # Lista para armazenar módulos em espera
pilha_alertas = []       # (o último alerta registrado é o primeiro a ser tratado - LIFO)
tempestade_ativa = random.choice([True, False])  # Simulando condições de tempestade atmosférica
area_livre = random.choice([True, False])         # Simulando disponibilidade da área de pouso
fila_pouso = deque()     # Criando a fila de pouso (FIFO) usando deque para remoções eficientes

combustivel_hab = modulos[0]['Combustivel'] # Combustível do módulo habitacional
combustivel_med = modulos[4]['Combustivel'] # Combustível do módulo médico

fila_ordenada = ordenar_por_prioridade(list(fila_pouso)) 
fila_pouso = deque(fila_ordenada)


sensores_nave = {  # Simulando status dos sensores (True=operacional, False=falha)
    "sensor_navegacao":    True,
    "sensor_altitude":     True,
    "sensor_temperatura":  random.choice([True, False]),
    "sensor_pressao":      True,
    "sensor_combustivel":  random.choice([True, False]),
}

for modulo in modulos:
    fila_pouso.append(modulo) # Adicionando os módulos à fila de pouso


# 7. PROCESSO DE SIMULAÇÃO DE POUSO

print("=" * 60)
print("   MGPEB - Missão Aurora Siger")
print("   Módulo de Gerenciamento de Pouso e Estabilização de Base")
print("=" * 60)
print("Carregando módulos na fila de pouso...")
print(f"{len(fila_pouso)} módulos carregados.\n")
print("Iniciando simulação de pouso...\n")

print("─" * 60)
print("FASE 1 — Reorganizando fila por prioridade")
print("─" * 60)


for m in fila_pouso:
    print(f"  [{m['Prioridade']}] {m['Nome']} | Combustível: {m['Combustivel']}% | "
          f"Peso: {m['Peso']}t | Módulo crítico: {m['Modulo Critico']}")

print("\n" + "─" * 60)
print("FASE 2 — Processando autorizações de pouso")
print("─" * 60)

while fila_pouso: # Enquanto houver módulos na fila de pouso
    modulo_escolhido = fila_pouso.popleft()  # retira do início da fila (FIFO)
    autorizado, motivos = autorizar_pouso(modulo_escolhido, tempestade_ativa, area_livre, sensores_nave) # Verifica se o pouso do módulo escolhido é autorizado

    if autorizado:
        modulos_pousados.append(modulo_escolhido)
        print(f"  [Autorizado] {modulo_escolhido['Nome']} -> Pouso autorizado")
    else:
        modulos_em_espera.append(modulo_escolhido) # Adiciona o módulo à lista de espera
        novo_alerta = f"ALERTA: {modulo_escolhido['Nome']} - {motivos}" # Cria um novo alerta com os motivos da negação
        pilha_alertas.append(novo_alerta)  # (LIFO)
        print(f"  [Negado]     {modulo_escolhido['Nome']} -> {motivos}")

print("─" * 60)
print("FASE 3 — Relatório de status")
print("─" * 60)
print(f"  Módulos pousados com sucesso : {len(modulos_pousados)}")
print(f"  Módulos em espera/alerta     : {len(modulos_em_espera)}")

print("─" * 60)
print("FASE 4 — Alertas pendentes")
print("─" * 60)

while pilha_alertas:
    print(f"  >> {pilha_alertas.pop()}") # Exibe o último alerta registrado e o remove da pilha (LIFO)

print("─" * 60)
print("FASE 5 — Buscas no sistema")
print("─" * 60)

print(f"  {'Módulo':<32} | {'Combustível':>10} | {'Prioridade':>8}")
print("  " + "-" * 55)

todos_modulos = modulos_pousados + modulos_em_espera
menor_combustivel = buscar_menor_combustivel(todos_modulos)
maior_prioridade  = buscar_maior_prioridade(todos_modulos)

for m in todos_modulos:
    print(f"  {m['Nome']:<32} | {m['Combustivel']:>10}% | {m['Prioridade']:>6}")

print("  " + "-" * 55)

if menor_combustivel:
    print(f"  {'>> Menor combustível:'} {menor_combustivel['Combustivel']}% - {menor_combustivel['Nome']}")

if maior_prioridade:
    print(f"  {'>> Maior prioridade:'} {maior_prioridade['Prioridade']} - {maior_prioridade['Nome']}")

print("\n")
print("=" * 60)
print("   ***Simulação MGPEB concluída.***")
print("=" * 60)

print("\n")
print("=" * 60)
print("Previsão de Combustível na Descida")
print("─" * 60)
print(f"  {'Hora':>5} | {' Módulo Habitacional':>22} | {'Módulo Médico':>18}")
print(f"  {'(h)':>5} | {'Combustível:':>15} {combustivel_hab} % | {'Combustível:':>15} {combustivel_med} %")
print("  " + "-" * 46)
for t in range(0, 9):
    c_hab = consumir_combustivel(modulos[0]['Combustivel'], 0.08, t)
    c_med = consumir_combustivel(modulos[4]['Combustivel'], 0.08, t)
    print(f"  {t:>5} | {c_hab:>21.2f}% | {c_med:>15.2f}%")

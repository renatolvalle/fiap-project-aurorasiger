"""
# Aurora Siger Mission | Python Prototype
# BLMSM - Base Landing Management and Stabilization Module
"""
# Importing libraries
import math
import random
from collections import deque


# 1. DEFINITION OF LANDING MODULES

modules = [
    {
        "Name": "Habitation Module",
        "Priority": 1,
        "Fuel": round(random.uniform(20, 99), 1),
        "Weight": round(random.uniform(5, 35), 1),
        "Critical Module": True,
        "ETA": 2
    },
    {
        "Name": "Solar Energy Module",
        "Priority": 2,
        "Fuel": round(random.uniform(20, 99), 1),
        "Weight": round(random.uniform(5, 35), 1),
        "Critical Module": True,
        "ETA": 4
    },
    {
        "Name": "Scientific Laboratory Module",
        "Priority": 3,
        "Fuel": round(random.uniform(20, 99), 1),
        "Weight": round(random.uniform(5, 35), 1),
        "Critical Module": False,
        "ETA": 6
    },
    {
        "Name": "Supplies Module",
        "Priority": 4,
        "Fuel": round(random.uniform(20, 99), 1),
        "Weight": round(random.uniform(5, 15), 1),
        "Critical Module": False,
        "ETA": 8
    },
    {
        "Name": "Medical Supplies Module",
        "Priority": 2,
        "Fuel": round(random.uniform(20, 99), 1),
        "Weight": round(random.uniform(5, 15), 1),
        "Critical Module": True,
        "ETA": 5
    },
]


# 2. BOOLEAN FUNCTIONS / DECISION RULES

def sufficient_fuel(module):
    return module["Fuel"] >= 40

def atmospheric_conditions_ok():
    storm = not random.choice([True, False])
    return storm

def landing_area():
    area_free = random.choice([True, False])
    return area_free

def landing_sensors(spaceship_sensors):
    sensors = all(spaceship_sensors.values())
    return sensors

def authorize_landing(module, storm, area_free, sensors):
# For modules WITH critical payload: ALL criteria must be true (AND).
# For modules WITHOUT critical payload: fuel + (atmosphere OR area available).
    fuel_ok   = sufficient_fuel(module)
    atm_ok    = storm
    area_ok   = area_free
    sensor_ok = sensors

    if module["Critical Module"]:
        authorized = fuel_ok and atm_ok and area_ok and sensor_ok
    else:
        authorized = fuel_ok and sensor_ok and (atm_ok or area_ok)

    # Diagnostics
    if not authorized:
        reasons = []  # List containing the reasons
        if not fuel_ok:
            reasons.append("Critical fuel level (<40%)")
        if not atm_ok:
            reasons.append("Active atmospheric storm")
        if not area_ok:
            reasons.append("Landing area obstructed")
        if not sensor_ok:
            reasons.append("Sensor failure")
        return False, " | ".join(reasons)

    return True, "All conditions met"


# 3. SEARCH ALGORITHMS

def search_lowest_fuel(fuel_list):

    if not fuel_list:
        return None
    minimum = fuel_list[0]
    for m in fuel_list[1:]:
        if m["Fuel"] < minimum["Fuel"]:
            minimum = m
    return minimum

def search_highest_priority(priority_list):

    if not priority_list:
        return None
    most_urgent = priority_list[0]
    for m in priority_list[1:]:
        if m["Priority"] < most_urgent["Priority"]:
            most_urgent = m
    return most_urgent


# 4. SORTING ALGORITHM

def sort_by_priority(list_to_sort):

    sorted_list = list_to_sort.copy()  # copy to avoid modifying the original
    for i in range(1, len(sorted_list)):
        key = sorted_list[i]
        j = i - 1
        while j >= 0 and sorted_list[j]["Priority"] > key["Priority"]:
            sorted_list[j + 1] = sorted_list[j]
            j -= 1
        sorted_list[j + 1] = key
    return sorted_list

# ─────────────────────────────────────────────
# 5. MATHEMATICAL MODELING — Fuel Consumption
# ─────────────────────────────────────────────
# Model: exponentially decreasing consumption during descent
# C(t) = C0 * e^(-k * t)
# where:
#   C0 = initial fuel (%)
#   k  = consumption rate (per hour)
#   t  = elapsed time (hours)
# The higher the descent speed, the greater the k.

def consume_fuel(c0, k, t):  # Returns the fuel level after t hours of descent
    return c0 * math.exp(-k * t)


# 6. LINEAR DATA STRUCTURES

landed_modules = []   # List to store successfully landed modules
on_hold_modules = []  # List to store waiting modules
alert_stack = []      # (last recorded alert is the first to be handled - LIFO)
storm_active = random.choice([True, False])  # Simulating atmospheric storm conditions
area_free = random.choice([True, False])      # Simulating landing area availability
landing_queue = deque()  # Creating the landing queue (FIFO) using deque for efficient pops from the front

fuel_hab = modules[0]['Fuel']
fuel_med = modules[4]['Fuel']

sorted_queue = sort_by_priority(list(landing_queue))
landing_queue = deque(sorted_queue)


spaceship_sensors = {  # Simulating sensor status (True=operational, False=failure)
    "navigation_sensor":  True,
    "altitude_sensor":    True,
    "temperature_sensor": random.choice([True, False]),
    "pressure_sensor":    True,
    "fuel_level_sensor":  random.choice([True, False]),
}

for module in modules:
    landing_queue.append(module)


# 7. LANDING SIMULATION PROCESS

print("=" * 60)
print("   BLMSM - Aurora Siger Mission")
print("   Base Landing Management and Stabilization Module")
print("=" * 60)
print("Loading modules into landing queue...")
print(f"{len(landing_queue)} modules loaded.\n")
print("Starting landing simulation...\n")

print("─" * 60)
print("PHASE 1 — Reorganizing queue by priority")
print("─" * 60)

for m in landing_queue:
    print(f"  [{m['Priority']}] {m['Name']} | Fuel: {m['Fuel']}% | "
          f"Weight: {m['Weight']}t | Critical module: {m['Critical Module']}")

print("\n" + "─" * 60)
print("PHASE 2 — Processing landing authorizations")
print("─" * 60)

while landing_queue:
    chosen_module = landing_queue.popleft()  # (FIFO)
    authorized, reasons = authorize_landing(chosen_module, storm_active, area_free, spaceship_sensors)

    if authorized:
        landed_modules.append(chosen_module)
        print(f"  [Authorized] {chosen_module['Name']} -> Landing authorized")
    else:
        on_hold_modules.append(chosen_module)
        new_alert = f"ALERT: {chosen_module['Name']} - {reasons}"
        alert_stack.append(new_alert)  # (LIFO)
        print(f"  [Denied]     {chosen_module['Name']} -> {reasons}")

print("─" * 60)
print("PHASE 3 — Status report")
print("─" * 60)
print(f"  Successfully landed modules : {len(landed_modules)}")
print(f"  Modules on hold/alert       : {len(on_hold_modules)}")

print("─" * 60)
print("PHASE 4 — Pending alerts")
print("─" * 60)

while alert_stack:
    print(f"  >> {alert_stack.pop()}")

print("─" * 60)
print("PHASE 5 — System searches")
print("─" * 60)

print(f"  {'Module':<32} | {'Fuel':>10} | {'Priority':>8}")
print("  " + "-" * 55)

all_modules = landed_modules + on_hold_modules
less_fuel    = search_lowest_fuel(all_modules)
top_priority = search_highest_priority(all_modules)

for m in all_modules:
    print(f"  {m['Name']:<32} | {m['Fuel']:>10}% | {m['Priority']:>6}")

print("  " + "-" * 55)

if less_fuel:
    print(f"  {'>> Lowest fuel:'} {less_fuel['Fuel']}% - {less_fuel['Name']}")

if top_priority:
    print(f"  {'>> Highest priority:'} {top_priority['Priority']} - {top_priority['Name']}")

print("\n")
print("=" * 60)
print("   ***BLMSM simulation complete.***")
print("=" * 60)

print("\n")
print("=" * 60)
print("Fuel Forecast During Descent")
print("─" * 60)
print(f"  {'Time':>5} | {'  Habitation Module':>22} | {'Medical Module':>18}")
print(f"  {'(h)':>5} | {'Fuel:':>15} {fuel_hab} % | {'Fuel:':>15} {fuel_med} %")
print("  " + "-" * 46)
for t in range(0, 9):
    c_hab = consume_fuel(modules[0]['Fuel'], 0.08, t)
    c_med = consume_fuel(modules[4]['Fuel'], 0.08, t)
    print(f"  {t:>5} | {c_hab:>21.2f}% | {c_med:>15.2f}%")

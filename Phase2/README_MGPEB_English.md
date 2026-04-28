Before reading: This is a project developed for a Data Science degree at FIAP College(Brazil) for educational purposes. 
Only this README and the file MGPEBEnglish.py are in english


# 🚀 Aurora Siger Mission — MGPEB

> **Landing and Base Stabilization Management Module**  
> Python Prototype — Space Landing Simulation

---

## 📋 About the Project

**MGPEB** is a computational simulation of the autonomous landing management of space modules on an extraterrestrial base. The system coordinates the landing sequence, evaluates environmental and operational conditions in real time, and autonomously authorizes or denies landings — prioritizing crew safety and mission continuity.

The architecture is inspired by real-world systems such as the **Apollo Guidance Computer (NASA)**, the **Curiosity Sky Crane (Mars)** and the **Falcon 9 landing system (SpaceX)**, with direct parallels to real-time operating systems (RTOS).

---


## Files from this repository

- FIAP_Aurora_Siger_MGPEB - PDF with all MGPEB project and explanation - Portuguese 
- MGPEBPortugues – Python version of the project - Portuguese
- MGPEBEnglish – Python version of the project - English
- [README_MGPEB.md](./README_MGPEB.md) – Portuguese version of the README


## 🛸 Simulated Landing Modules

| Module | Priority | Critical | ETA (h) |
|---|---|---|---|
| Habitation Module | 1 | ✅ Yes | 2 |
| Solar Energy Module | 2 | ✅ Yes | 4 |
| Medical Supplies Module | 2 | ✅ Yes | 5 |
| Scientific Laboratory Module | 3 | ❌ No | 6 |
| Supplies Module | 4 | ❌ No | 8 |

> Fuel (20–99%) and weight (5–35t) are randomly generated at each run via `random.uniform()`, simulating real mission variability.

---

## ⚙️ Features

- **Priority-based sorting** via *Insertion Sort* before queue processing
- **Landing authorization** with AND/OR boolean logic based on module criticality
- **FIFO queue** (`collections.deque`) for efficient module processing
- **LIFO stack** for alert management in order of urgency
- **Linear search** for the module with lowest fuel and highest priority
- **Fuel consumption modeling** with exponential decay `C(t) = C₀ · e^(−k·t)`
- **Full mission report** across 5 phases printed to the console

---

## 🔐 Decision Rules — Boolean Logic

### Critical Modules — Full AND
Landing is authorized only when **all** conditions are simultaneously true:

```
C1 (Fuel ≥ 40%) AND C2 (Clear atmosphere) AND C3 (Landing area free) AND C4 (Sensors OK)
```

### Non-Critical Modules — AND + OR
More flexible logic, allowing landing under partially adverse conditions:

```
C1 (Fuel ≥ 40%) AND C4 (Sensors OK) AND (C2 OR C3)
```

---

## 📐 Mathematical Modeling

Fuel consumption during descent is modeled by **exponential decay**:

```
C(t) = C₀ · e^(−k·t)
```

| Parameter | Description |
|---|---|
| `C₀` | Initial fuel level (%) |
| `k` | Consumption rate per hour (default: `0.08`) |
| `t` | Elapsed time in hours |

> Higher values of `k` simulate faster descents with greater fuel consumption.

---

## 🏗️ Layered Architecture

| Layer | Component | Function |
|---|---|---|
| 1 — Data | Python Dictionaries | Module representation |
| 2 — Decision | Boolean Functions | Evaluates AND/OR landing conditions |
| 3 — Search | Linear Search O(n) | Finds lowest fuel / highest priority |
| 4 — Sorting | Insertion Sort | Reorders queue by priority |
| 5 — Modeling | Exponential Decay | Predicts consumption `C(t) = C₀·e^(−kt)` |
| 6 — Structures | List / Queue / Stack | Controls FIFO flow and LIFO alerts |
| 7 — Output | Console | Mission report and diagnostics |

---

## 📊 Data Structures Used

| Structure | Implementation | Main Operation | Complexity | Use in MGPEB |
|---|---|---|---|---|
| List | `list` | `append()` / index `[i]` | O(1) amort. | Landed and waiting modules |
| Queue (FIFO) | `collections.deque` | `popleft()` | O(1) | Ordered landing queue |
| Stack (LIFO) | `list` | `append()` / `pop()` | O(1) | Denial alert stack |

> **Why `deque` instead of `list` for the queue?**  
> Removing from the front of a conventional list is O(n). `collections.deque` provides `popleft()` in O(1) — essential in real-time systems where scheduling latency must be minimal and predictable.

---

## 🖥️ Simulation Phases

```
PHASE 1 — Reordering queue by priority (Insertion Sort)
PHASE 2 — Processing landing authorizations (boolean logic)
PHASE 3 — Status report (landed vs. on hold)
PHASE 4 — Pending alerts (LIFO display)
PHASE 5 — Analytical searches + fuel consumption forecast
```

---

## 🚀 How to Run

**Requirements:** Python 3.x (no external dependencies)

```bash
# Clone the repository
git clone https://github.com/your-username/aurora-siger-mission.git
cd aurora-siger-mission

# Run the simulator
python MGPEBPortugues.py
```

> Since fuel, weight, and atmospheric conditions are randomly generated, each run produces a different result.

---

## 📦 Libraries Used

```python
import math        # Exponential decay calculation
import random      # Random mission variable generation
from collections import deque  # High-performance FIFO queue
```

Only Python standard library modules — **no additional installation required**.

---

## 🌱 ESG & Governance

| Dimension | Principle | Implementation in MGPEB |
|---|---|---|
| Environmental | Energy efficiency | `C(t)=C₀·e^(−kt)` + lowest fuel search |
| Social | Human safety first | Habitation (prio.1) + Medical (prio.2) as critical |
| Governance | Auditability | Explicit diagnostics + LIFO alert stack |
| Governance | Fault tolerance | Independent sensors with simulated random failure |
| Governance | Objective criteria | AND/OR logic with no subjective human intervention |

---

## 👤 Author

**Renato Levy do Valle**  
FIAP — 2026

---

## 📄 License

This project was developed for academic purposes at FIAP.

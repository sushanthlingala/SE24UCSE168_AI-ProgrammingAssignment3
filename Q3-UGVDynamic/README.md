# Q3 – UGV Pathfinding with Dynamic Obstacles
## Problem Statement
In the above problem, we relax the condition that all obstacles are **Static**. In a real world, obstacles can be dynamic and not known a priori. How do you make the UGV navigate and find the optimal path in a dynamic obstacles environment.

---
## Approach
This problem extends Q2 by removing the assumption that all obstacles are known before the UGV starts moving. The battlefield now has two kinds of obstacles:

- **Static obstacles** generated at the start (same as Q2)
- **Dynamic obstacles** that appear randomly during the UGV's traversal, unknown a priori

The algorithm used is **Replanning A* Search**. The UGV starts with an initial A* plan and moves step by step. Every 5 steps, a wave of 8 new dynamic obstacles is randomly spawned on the grid. If any of these new obstacles fall on the UGV's current planned path, the plan is immediately discarded and A* is run again from the UGV's current position to find a new route around the newly appeared obstacles.

This cycle of move, detect, and replan continues until the UGV either reaches the goal or gets completely surrounded with no viable path remaining.

---
## Files
| File | Description |
|------|-------------|
| `ugv_dynamic.py` | Full implementation of Replanning A* for dynamic obstacle navigation, with simulation, visualization and MOE reporting |
| `requirements.txt` | Python dependencies required to run the program |

---
## Setup
Install dependencies:
```bash
pip install -r requirements.txt
```
Run the program:
```bash
python ugv_dynamic.py
```

---
## Running the Program
```
*** UGV Pathfinder (Replanning A* Search) ***

1. Select Obstacle Density to Generate Grid
2. Set Start and Goal
3. Run Dynamic Simulation
4. Show Measures of Effectiveness
5. Exit
```
**Recommended flow:** Option 1 → Option 2 → Option 3 → Option 4

---
## Obstacle Density Levels
| Level | Initial Static Density |
|-------|------------------------|
| Low | 15% of cells are obstacles |
| Medium | 30% of cells are obstacles |
| High | 50% of cells are obstacles |

Dynamic obstacles are spawned in waves of 8 every 5 steps regardless of the density level chosen.

---
## Measures of Effectiveness
| Metric | Description |
|--------|-------------|
| Obstacle Density Level | Initial static obstacle density used for the run |
| Grid Size | Fixed at 70 x 70 km |
| Start / Goal | User-specified positions |
| Straight-line Distance | Euclidean (theoretical minimum) distance |
| Initial Planned Distance | Distance of the path A* planned before traversal began |
| Actual Distance Travelled | Real distance covered by the UGV including all detours |
| Extra Distance (replanning) | Additional distance caused by dynamic obstacle detours |
| Path Optimality | Ratio of straight-line to actual distance (higher = better) |
| Total Replans Triggered | How many times the UGV had to abandon its plan and replan |
| Dynamic Obstacles Spawned | Total new obstacles that appeared during the run |
| Steps Taken | Total cells visited by the UGV |
| Direction Changes | Number of turns taken along the actual path |
| Time Taken | Total simulation time in milliseconds |

---
## Project Structure
```
Q3-UGVDynamic/
├── ugv_dynamic.py
├── requirements.txt
└── README.md
```

---
## Author
Sushanth Lingala  
Roll No: **SE24UCSE168**  
Course: **CS-2201 – Artificial Intelligence**

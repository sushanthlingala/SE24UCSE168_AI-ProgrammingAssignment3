# Q2 – UGV Pathfinding on a Battlefield Grid
## Problem Statement
An **Unmanned Ground Vehicle (UGV)** is a robot that finds the optimal path from a user-specified start node to a user-specified goal node on a map of a small area in a battlefield (70x70 km). There are obstacles known a-priori. The density of obstacles can be generated randomly with three different levels of density. Design an algorithm that makes the UGV navigate through this grid space, avoiding all known obstacles, to reach the goal by the shortest distance. Trace this path along with the Measures of Effectiveness.

---
## Approach
A **70x70 grid** is used to represent the battlefield, where each cell corresponds to 1 km². Obstacles are randomly distributed across the grid at one of three configurable density levels.

The pathfinding is handled by the **A\* Search Algorithm**, which is an informed search strategy that combines the actual cost from the start node with a heuristic estimate (straight-line/Euclidean distance) to the goal. This ensures the shortest possible path is found efficiently without exploring the entire grid.

- The UGV can move in **8 directions** (including diagonals), with diagonal moves costing √2 ≈ 1.414 km and straight moves costing 1.0 km
- Start and goal cells are always guaranteed to be obstacle-free
- If no path exists due to the obstacle layout, the user is prompted to regenerate the grid or pick different positions

---
## Files
| File | Description |
|------|-------------|
| `ugv.py` | Full implementation of A* pathfinding on the battlefield grid with visualization and MOE reporting |
| `requirements.txt` | Python dependencies required to run the program |

---
## Setup
Install dependencies:
```bash
pip install -r requirements.txt
```
Run the program:
```bash
python ugv.py
```

---
## Running the Program
```
*** UGV Pathfinder (A* Search) ***

1. Select Obstacle Density to Generate Grid
2. Set Start and Goal
3. Find Optimal Path
4. Show Measures of Effectiveness
5. Exit
```
**Recommended flow:** Option 1 → Option 2 → Option 3 → Option 4

---
## Obstacle Density Levels
| Level | Density |
|-------|---------|
| Low | 15% of cells are obstacles |
| Medium | 30% of cells are obstacles |
| High | 50% of cells are obstacles |

---
## Measures of Effectiveness
| Metric | Description |
|--------|-------------|
| Density Level | Obstacle density used for the run |
| Grid Size | Fixed at 70 x 70 km |
| Start / Goal | User-specified positions |
| Straight-line Distance | Euclidean (theoretical minimum) distance |
| Path Length | Actual distance travelled by the UGV |
| Path Optimality | Ratio of straight-line to path length (higher = better) |
| Nodes Expanded | Number of nodes processed by A* |
| Path Nodes | Total cells in the final path |
| Direction Changes | Number of turns taken along the path |
| Time Taken | Computation time in milliseconds |

---
## Project Structure
```
Q2-UGVPathfinder/
├── ugv.py
├── requirements.txt
└── README.md
```

---
## Author
Sushanth Lingala  
Roll No: **SE24UCSE168**  
Course: **CS-2201 – Artificial Intelligence**

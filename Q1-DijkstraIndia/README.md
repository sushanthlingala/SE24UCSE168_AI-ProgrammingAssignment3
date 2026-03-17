# Q1 – Dijkstra's Algorithm (Uniform-Cost Search)
## Problem Statement
When actions have different costs in a state based search space, an obvious choice is to use best-first search where the evaluation function is the cost of the path from the root to the current node. This is called **Dijkstra's Algorithm** by the theoretical computer science community, and **Uniform-Cost Search** by the AI community. Implement Dijkstra's algorithm for all the cities in India and their road distances.

---
## Approach
Real road distances between major Indian cities are fetched using the **Google Maps Distance Matrix API** and stored in a local cache (`graph_cache.json`) to avoid redundant API calls on every run.

- On first run, the graph is built using **15 preset major Indian cities** and saved to cache.
- On subsequent runs, the cache is loaded instantly without the requirement of an API key.
- Additional cities can be added at runtime via the menu, which triggers a targeted API call only for the new cities.

The graph is then used to run **Dijkstra's Algorithm**, which expands nodes in order of cumulative path cost using a **min-heap priority queue**, guaranteeing the shortest road distance between any two cities.

---
## Files
| File | Description |
|------|-------------|
| `dijkstra.py` | Full implementation of Dijkstra's Algorithm with API integration, caching, and interactive menu |
| `graph_cache.json` | Pre-built cache of road distances between 15 preset Indian cities |
| `.env.example` | Template for the environment file — copy to `.env` and add your API key to use custom cities |
| `.gitignore` | Ensures `.env` is never committed to the repository |

---
## Running the Program
Install dependencies:
```bash
pip install requests python-dotenv
```
Run the program:
```bash
python dijkstra.py
```
```
Loaded graph from cache (15 cities)

1. Add Cities
2. Refresh Graph (force API call)
3. Find Shortest Path
4. Show Current Cities
5. Exit

Enter choice:
```
*(Optional)* To add cities beyond the preset list, create a `.env` file in the same folder:
```
GOOGLE_API_KEY=your_key_here
```

---
## Project Structure
```
Q1-DijkstraIndia/
├── dijkstra.py
├── graph_cache.json
├── .env.example
└── .gitignore
```

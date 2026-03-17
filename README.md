# AI Programming Assignment 2 – CS2201
This repository contains the code for the following question detailed in our Programming Assignment 2 for the CS-2201 course:
    1. When actions have different costs in a state based search space, an obvious choice is to use best-first search where the evaluation function is the cost of the path from the root to the current node. This is called Dijkstra's algorithm by the theoretical computer science community, and Uniform-Cost Search by the AI community. Implement Dijkstra's algorithm for all the cities in India and their road distances.

---
## Repository Structure
The repository contains the following files:
- **dijkstra_india_live.py**  
  Contains the implementation of Dijkstra's algorithm (Uniform-Cost Search) over a graph of real road distances between 15 major Indian cities. Road distances are fetched live using the Google Maps Distance Matrix API and cached locally to avoid redundant API calls.

- **graph_cache.json**  
  A pre-built cache of road distances between the 15 preset cities. Loaded automatically on startup so the program works out of the box without requiring an API key.

- **.env.example**  
  A template for the environment file. Copy this to `.env` and fill in your own Google Maps API key if you wish to add cities beyond the preset list.

---
## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/sushanthlingala/SE24UCSE168_AI-ProgrammingAssignments2.git
   ```
2. Install dependencies:
   ```bash
   pip install requests python-dotenv
   ```
3. Run the program:
   ```bash
   python dijkstra_india_live.py
   ```
   The program will load the preset graph from `graph_cache.json` automatically. No API key is needed to use the preset cities.

4. *(Optional)* To add cities beyond the preset list, copy `.env.example` to `.env` and fill in your Google Maps API key:
   ```
   GOOGLE_API_KEY=your_key_here
   ```

---
## Author
Sushanth Lingala  
Roll No: **SE24UCSE168**  
Course: **CS-2201 – Artificial Intelligence**

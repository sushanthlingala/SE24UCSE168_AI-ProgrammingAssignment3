# AI Programming Assignment 3 – CS2201
This repository currently contains the codes and documentations for the following questions detailed in our Programming Assignment 3 for the CS-2201 course:

    1. When actions have different costs in a state based search space, an obvious choice is to use best-first search where the evaluation function is the cost of the path from the root to the current node. This is called Dijkstra's algorithm by the theoretical computer science community, and uniform-cost search Uniform-cost search by the AI community. Implement the Dijkstra's algorithm to all the cities in India and their Road distances. This info may be taken from open sources.
    2. An Unmanned Ground Vehicle (UGV) is a robot that finds the optimal path from a given user-specified start node to a user-specified Goal node on a map of a small area in a battlefield (Eg 70x70 Kms). There are obstacles known a-priori. The density of the obstacles can be generated randomly with three different levels of density. Design an algorithm that makes the UGV to navigate through this grid space avoiding all the known obstacles to reach the goal by the shortest distance. Trace this path along with the Measures of Effectiveness.
    3. In the above problem, we relax the condition that all obstacles are Static. In a real world, obstacles can be dynamic and not known a priori. How do you make the UGV navigate and find the optinal path in a dynamic obstacles environment.
    
The codes and related documentation (if required) have been posted within the respective folders (named as per the question).
To clone this repository, please use:
```
git clone https://github.com/sushanthlingala/SE24UCSE168_AI-ProgrammingAssignment3.git
```
---
## Repository Structure
The repository is organized into the following folders:
- **Q1-DijkstraIndia**  
  Contains the implementation of Dijkstra's Algorithm (Uniform-Cost Search) over a graph of real road distances between major Indian cities, fetched using the Google Maps Distance Matrix API.

- **Q2-UGVPathfinder**  
  Contains the implementation of an A* Search based pathfinding system for a UGV navigating a randomly generated battlefield grid with three configurable obstacle density levels.

- **Q3-UGVDynamic**  
  Contains the implementation of a Replanning A* Search based pathfinding system for a UGV navigating a battlefield grid where obstacles appear dynamically mid-traversal, unknown to the UGV a priori.

---
## Author
Sushanth Lingala  
Roll No: **SE24UCSE168**  
Course: **CS-2201 – Artificial Intelligence**

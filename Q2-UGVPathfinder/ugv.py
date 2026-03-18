import heapq
import random
import time
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

GRID_SIZE = 70

DENSITY = {
    1: ("low",    0.15),
    2: ("medium", 0.30),
    3: ("high",   0.50)
}


def make_grid(rate):
    grid = [[0]*GRID_SIZE for _ in range(GRID_SIZE)]
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if random.random() < rate:
                grid[r][c] = 1
    return grid


def clear_cell(grid, pos):
    grid[pos[0]][pos[1]] = 0


def heuristic(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)


def get_neighbors(pos, grid):
    r,c = pos
    directions = [
        (-1,0),(1,0),(0,-1),(0,1),
        (-1,-1),(-1,1),(1,-1),(1,1)
    ]
    neighbors = []
    for dr,dc in directions:
        nr,nc = r+dr, c+dc
        if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
            if grid[nr][nc] == 0:
                cost = 1.414 if (dr != 0 and dc != 0) else 1.0
                neighbors.append(((nr,nc), cost))
    return neighbors


def astar(grid, start, goal):
    open_heap = []
    heapq.heappush(open_heap, (0, start))

    came_from = {start: None}
    g_score = {start: 0}
    expanded = 0

    t0 = time.time()

    while open_heap:
        _, current = heapq.heappop(open_heap)
        expanded += 1

        if current == goal:
            elapsed = time.time()-t0
            path = []
            node = goal
            while node:
                path.append(node)
                node = came_from[node]
            path.reverse()
            return path, expanded, elapsed

        for neighbor,move_cost in get_neighbors(current, grid):
            tentative = g_score[current]+move_cost
            if neighbor not in g_score or tentative < g_score[neighbor]:
                g_score[neighbor] = tentative
                f = tentative+heuristic(neighbor, goal)
                heapq.heappush(open_heap, (f, neighbor))
                came_from[neighbor] = current

    elapsed = time.time()-t0
    return None, expanded, elapsed


def path_length(path):
    total = 0.0
    for i in range(1, len(path)):
        r1,c1 = path[i-1]
        r2,c2 = path[i]
        total += math.sqrt((r2-r1)**2+(c2-c1)**2)
    return round(total, 3)


def count_turns(path):
    if len(path) < 3:
        return 0
    turns = 0
    for i in range(1, len(path)-1):
        d1 = (path[i][0]-path[i-1][0], path[i][1]-path[i-1][1])
        d2 = (path[i+1][0]-path[i][0], path[i+1][1]-path[i][1])
        if d1 != d2:
            turns += 1
    return turns


def straightline(start, goal):
    return round(heuristic(start, goal), 3)


def print_moe(last_run):
    if last_run is None:
        print("Please make an initial run to find a path using option 3 (ensure that you have already selected obstacle density and set start and goal)\n")
        return

    path,expanded,elapsed,start,goal,density_label = last_run
    sl = straightline(start, goal)
    pl = path_length(path)
    optimality = round(sl/pl*100, 2) if pl > 0 else 0
    turns = count_turns(path)

    print("\n********** Measures of Effectiveness **********")
    print(f"  Density Level         : {density_label.capitalize()}")
    print(f"  Grid Size             : {GRID_SIZE} x {GRID_SIZE} km")
    print(f"  Start                 : {start}")
    print(f"  Goal                  : {goal}")
    print(f"  Straight-line Dist    : {sl} km")
    print(f"  Path Length           : {pl} km")
    print(f"  Path Optimality       : {optimality}%")
    print(f"  Nodes Expanded        : {expanded}")
    print(f"  Path Nodes            : {len(path)}")
    print(f"  Direction Changes     : {turns}")
    print(f"  Time Taken            : {round(elapsed*1000, 3)} ms")
    print("***********************************************\n")


def visualize(grid, path, start, goal, density_label):
    canvas = np.zeros((GRID_SIZE, GRID_SIZE, 3))

    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c] == 1:
                canvas[r,c] = [0.2, 0.2, 0.2]
            else:
                canvas[r,c] = [0.95, 0.95, 0.95]

    for r,c in path:
        canvas[r,c] = [0.2, 0.6, 1.0]

    sr,sc = start
    gr,gc = goal
    canvas[sr,sc] = [0.1, 0.8, 0.1]
    canvas[gr,gc] = [0.9, 0.1, 0.1]

    fig,ax = plt.subplots(figsize=(9,9))
    ax.imshow(canvas, origin="upper")

    ax.plot(sc, sr, "g^", markersize=10, label="Start")
    ax.plot(gc, gr, "r*", markersize=12, label="Goal")

    path_c = [c for r,c in path]
    path_r = [r for r,c in path]
    ax.plot(path_c, path_r, color="deepskyblue", linewidth=1.2, alpha=0.8)

    free = mpatches.Patch(color=[0.95,0.95,0.95], label="Empty cell (no obstacle)")
    obs  = mpatches.Patch(color=[0.2,0.2,0.2],   label="Cell with obstacle")
    pth  = mpatches.Patch(color="deepskyblue",    label="Path")
    ax.legend(handles=[free, obs, pth], loc="upper right", fontsize=8)

    pl = path_length(path)
    ax.set_title(f"UGV Path — {density_label.capitalize()} Density | Length: {pl} km | Nodes: {len(path)}", fontsize=11)
    ax.set_xlabel("X (km)")
    ax.set_ylabel("Y (km)")
    plt.tight_layout()

    fname = f"ugv_path_{density_label}.png"
    plt.savefig(fname, dpi=120)
    plt.show()
    print(f"Map saved as {fname}\n")


def get_valid_pos(label, grid):
    while True:
        try:
            raw = input(f"Enter {label} (row col, space separated, 0-{GRID_SIZE-1}): ").strip().split()
            r,c = int(raw[0]), int(raw[1])
            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                return (r,c)
            print(f"Entered value is not within bounds. Please enter values between 0 and {GRID_SIZE-1}")
        except:
            print("Invalid input, please try again")


grid = None
density_label = None
start = None
goal  = None
last_run = None

print("\n*** UGV Pathfinder (A* Search) ***\n")

while True:
    print("1. Select Obstacle Density to Generate Grid")
    print("2. Set Start and Goal")
    print("3. Find Optimal Path")
    print("4. Show Measures of Effectiveness")
    print("5. Exit\n")

    try:
        choice = int(input("Enter choice: "))
    except ValueError:
        print("Please enter a number between 1 and 5\n")
        continue

    if choice==1:
        print("\n  1. Low    (15%)")
        print("  2. Medium (30%)")
        print("  3. High   (50%)")
        try:
            dlvl = int(input("Enter obstacle density choice: "))
            if dlvl not in DENSITY:
                print("Invalid choice. Please select 1, 2 or 3\n")
                continue
        except ValueError:
            print("Invalid input\n")
            continue

        density_label,rate = DENSITY[dlvl]
        grid = make_grid(rate)
        start = None
        goal  = None
        last_run = None
        print(f"Grid generated with {density_label} obstacle density ({int(rate*100)}%)\n")

    elif choice==2:
        if grid is None:
            print("Please generate a grid first using option 1\n")
            continue
        start = get_valid_pos("start", grid)
        goal  = get_valid_pos("goal",  grid)
        clear_cell(grid, start)
        clear_cell(grid, goal)
        print(f"Start set to: {start}, Goal set to: {goal}\n")

    elif choice==3:
        if grid is None:
            print("Generate a grid first (option 1)\n")
            continue
        if start is None or goal is None:
            print("Set start and goal first (option 2)\n")
            continue
        if start==goal:
            print("Start and goal are the same\n")
            continue

        print("Running A* Search Algorithm")
        path,expanded,elapsed = astar(grid, start, goal)

        if path is None:
            print("No path found! The entered goal is unreachable with current obstacle layout, please enter a different start and goal using option 2")
            print("OR")
            print("Regenerate the grid again using option 1 to get a different map\n")
            last_run = None
        else:
            last_run = (path, expanded, elapsed, start, goal, density_label)
            visualize(grid, path, start, goal, density_label)
            print("Path successfully found! Please use option 4 to view the Measures of Effectiveness for the latest run\n")

    elif choice==4:
        print_moe(last_run)

    elif choice==5:
        break

    else:
        print("Invalid choice. Enter a number between 1 and 5\n")

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

OBSTACLE_INTERVAL = 5
OBSTACLES_PER_WAVE = 8


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
    dirs = [
        (-1,0),(1,0),(0,-1),(0,1),
        (-1,-1),(-1,1),(1,-1),(1,1)
    ]
    result = []
    for dr,dc in dirs:
        nr,nc = r+dr,c+dc
        if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
            if grid[nr][nc] == 0:
                w = 1.414 if (dr!=0 and dc!=0) else 1.0
                result.append(((nr,nc), w))
    return result


def astar(grid, start, goal):
    heap = []
    heapq.heappush(heap, (0,start))

    prev = {start: None}
    gscore = {start: 0}
    expanded = 0

    while heap:
        _,cur = heapq.heappop(heap)
        expanded += 1

        if cur==goal:
            path = []
            node = goal
            while node:
                path.append(node)
                node = prev[node]
            path.reverse()
            return path, expanded

        for nb,w in get_neighbors(cur, grid):
            new_g = gscore[cur]+w
            if nb not in gscore or new_g < gscore[nb]:
                gscore[nb] = new_g
                f = new_g+heuristic(nb, goal)
                heapq.heappush(heap, (f, nb))
                prev[nb] = cur

    return None, expanded


def drop_obstacles(grid, count, safe):
    fresh = []
    tries = 0
    while len(fresh) < count and tries < count*20:
        r = random.randint(0, GRID_SIZE-1)
        c = random.randint(0, GRID_SIZE-1)
        tries += 1
        if grid[r][c]==0 and (r,c) not in safe:
            grid[r][c] = 2
            fresh.append((r,c))
    return fresh


def is_blocked(path, grid):
    for cell in path:
        if grid[cell[0]][cell[1]] != 0:
            return True
    return False


def travel_dist(trail):
    total = 0.0
    for i in range(1, len(trail)):
        r1,c1 = trail[i-1]
        r2,c2 = trail[i]
        total += math.sqrt((r2-r1)**2+(c2-c1)**2)
    return round(total, 3)


def count_turns(trail):
    if len(trail) < 3:
        return 0
    turns = 0
    for i in range(1, len(trail)-1):
        d1 = (trail[i][0]-trail[i-1][0], trail[i][1]-trail[i-1][1])
        d2 = (trail[i+1][0]-trail[i][0], trail[i+1][1]-trail[i][1])
        if d1!=d2:
            turns += 1
    return turns


def run_sim(grid, start, goal, dlabel):
    t0 = time.time()

    first_path, _ = astar(grid, start, goal)
    if first_path is None:
        return None

    cur_path = first_path[:]
    trail = [start]
    dyn_obs = []
    replans = 0
    exp_total = 0
    step = 0
    safe = {start, goal}
    ugv = start

    while ugv != goal:
        step += 1

        if step % OBSTACLE_INTERVAL == 0:
            fresh = drop_obstacles(grid, OBSTACLES_PER_WAVE, safe)
            dyn_obs.extend(fresh)

            if is_blocked(cur_path, grid):
                new_path, expanded = astar(grid, ugv, goal)
                exp_total += expanded
                replans += 1
                if new_path is None:
                    elapsed = time.time()-t0
                    return {
                        "success": False,
                        "trail": trail,
                        "replans": replans,
                        "elapsed": elapsed,
                        "dyn_obs": dyn_obs,
                        "start": start,
                        "goal": goal,
                        "dlabel": dlabel
                    }
                cur_path = new_path

        if len(cur_path) > 1:
            nxt = cur_path[1]
            if grid[nxt[0]][nxt[1]] != 0:
                new_path, expanded = astar(grid, ugv, goal)
                exp_total += expanded
                replans += 1
                if new_path is None:
                    elapsed = time.time()-t0
                    return {
                        "success": False,
                        "trail": trail,
                        "replans": replans,
                        "elapsed": elapsed,
                        "dyn_obs": dyn_obs,
                        "start": start,
                        "goal": goal,
                        "dlabel": dlabel
                    }
                cur_path = new_path
                nxt = cur_path[1]

            ugv = nxt
            trail.append(ugv)
            cur_path.pop(0)
        else:
            break

    elapsed = time.time()-t0

    return {
        "success": ugv==goal,
        "trail": trail,
        "replans": replans,
        "exp_total": exp_total,
        "elapsed": elapsed,
        "dyn_obs": dyn_obs,
        "start": start,
        "goal": goal,
        "dlabel": dlabel,
        "first_path": first_path
    }


def print_moe(run):
    if run is None:
        print("Please run the simulation first using option 3\n")
        return

    if not run["success"]:
        print("\nSimulation ended early as the UGV got completely blocked by dynamic obstacles, and no further path is possible")
        print("Please run a fresh trial using option 1 and/or option 2 (generate new grid or change start and goal)\n")

    trail = run["trail"]
    start = run["start"]
    goal  = run["goal"]

    straight  = round(heuristic(start, goal), 3)
    actual    = travel_dist(trail)
    init_dist = travel_dist(run.get("first_path", trail))
    overhead  = round(actual-init_dist, 3)
    opt       = round(straight/actual*100, 2) if actual > 0 else 0
    turns     = count_turns(trail)

    print("\n********** Measures of Effectiveness **********")
    print(f"  Obstacle Density Level              : {run['dlabel'].capitalize()}")
    print(f"  Grid Size                  : {GRID_SIZE} x {GRID_SIZE} km")
    print(f"  Start                      : {start}")
    print(f"  Goal                       : {goal}")
    print(f"  Straight-line Distance     : {straight} km")
    print(f"  Initial Planned Distance   : {init_dist} km")
    print(f"  Actual Distance Travelled  : {actual} km")
    print(f"  Extra Distance (replanning): {overhead} km")
    print(f"  Path Optimality            : {opt}%")
    print(f"  Total Replans Triggered    : {run['replans']}")
    print(f"  Dynamic Obstacles Spawned  : {len(run['dyn_obs'])}")
    print(f"  Steps Taken                : {len(trail)}")
    print(f"  Direction Changes          : {turns}")
    print(f"  Time Taken                 : {round(run['elapsed']*1000, 3)} ms")
    print("**********************************************************\n")


def visualize(grid, run):
    canvas = np.zeros((GRID_SIZE, GRID_SIZE, 3))

    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            v = grid[r][c]
            if v==1:
                canvas[r,c] = [0.2, 0.2, 0.2]
            elif v==2:
                canvas[r,c] = [0.85, 0.2, 0.2]
            else:
                canvas[r,c] = [0.95, 0.95, 0.95]

    for r,c in run["trail"]:
        canvas[r,c] = [0.2, 0.6, 1.0]

    sr,sc = run["start"]
    gr,gc = run["goal"]
    canvas[sr,sc] = [0.1, 0.8, 0.1]
    canvas[gr,gc] = [0.9, 0.1, 0.1]

    fig,ax = plt.subplots(figsize=(9,9))
    ax.imshow(canvas, origin="upper")

    ax.plot(sc, sr, "g^", markersize=10, label="Start")
    ax.plot(gc, gr, "r*", markersize=12, label="Goal")

    tc = [c for r,c in run["trail"]]
    tr = [r for r,c in run["trail"]]
    ax.plot(tc, tr, color="deepskyblue", linewidth=1.2, alpha=0.8)

    free = mpatches.Patch(color=[0.95,0.95,0.95], label="Empty cell (no obstacle)")
    sobs = mpatches.Patch(color=[0.2,0.2,0.2],   label="Cell with static obstacle (generated before traversal)")
    dobs = mpatches.Patch(color=[0.85,0.2,0.2],  label="Cell with dynamic obstacle (generated mid-traversal)")
    pth  = mpatches.Patch(color="deepskyblue",    label="Path taken")
    ax.legend(handles=[free,sobs,dobs,pth], loc="upper right", fontsize=8)

    lbl  = run["dlabel"]
    dist = travel_dist(run["trail"])
    ax.set_title(
        f"UGV Dynamic Path ({lbl.capitalize()} Density)   "
        f"Distance: {dist} km   Replans: {run['replans']}",
        fontsize=11
    )
    ax.set_xlabel("X (km)")
    ax.set_ylabel("Y (km)")
    plt.tight_layout()

    fname = f"ugv_dynamic_{lbl}.png"
    plt.savefig(fname, dpi=120)
    plt.show()
    print(f"Map saved as {fname}\n")


def get_pos(label, grid):
    while True:
        try:
            raw = input(f"Enter {label} (row col, space separated, 0-{GRID_SIZE-1}): ").strip().split()
            r,c = int(raw[0]), int(raw[1])
            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                return (r,c)
            print(f"Entered value is not within bounds. Please enter values within bounds(between 0 and {GRID_SIZE-1})")
        except:
            print("Invalid input, please try again")


grid   = None
dlabel = None
start  = None
goal   = None
run    = None

print("\n*** UGV Pathfinder (Replanning A* Search) ***\n")

while True:
    print("1. Select Obstacle Density to Generate Grid")
    print("2. Set Start and Goal")
    print("3. Run Dynamic Simulation")
    print("4. Show Measures of Effectiveness")
    print("5. Exit\n")

    try:
        choice = int(input("Enter choice: "))
    except ValueError:
        print("Please enter a number between 1 and 5\n")
        continue

    if choice==1:
        print("\n1. Low    (15%)")
        print("2. Medium (30%)")
        print("3. High   (50%)")
        try:
            dlvl = int(input("Enter obstacle density choice: "))
            if dlvl not in DENSITY:
                print("Invalid choice. Please select 1, 2 or 3\n")
                continue
        except ValueError:
            print("Invalid input\n")
            continue

        dlabel,rate = DENSITY[dlvl]
        grid  = make_grid(rate)
        start = None
        goal  = None
        run   = None
        print(f"Grid generated with {dlabel} obstacle density ({int(rate*100)}%)\n")

    elif choice==2:
        if grid is None:
            print("Please generate a grid first using option 1\n")
            continue
        start = get_pos("start", grid)
        goal  = get_pos("goal",  grid)
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

        print("Running dynamic simulation...")
        run = run_sim(grid, start, goal, dlabel)

        if run is None:
            print("No initial path found, goal is unreachable from start with current obstacle layout")
            print("Try regenerating the grid (option 1) or picking different start and goal (option 2)\n")
        else:
            status = "successfully reached the goal" if run["success"] else "got blocked by dynamic obstacles"
            print(f"Simulation complete. UGV {status}")
            print(f"Replans triggered: {run['replans']}   Dynamic obstacles spawned: {len(run['dyn_obs'])}")
            visualize(grid, run)
            print("Use option 4 to view Measures of Effectiveness\n")

    elif choice==4:
        print_moe(run)

    elif choice==5:
        break

    else:
        print("Invalid choice. Enter a number between 1 and 5\n")

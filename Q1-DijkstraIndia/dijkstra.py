import heapq
import requests
import os, json
from dotenv import load_dotenv

load_dotenv()

cache_file = "graph_cache.json"

default_cities = [
    "Delhi", "Mumbai", "Chennai", "Kolkata", "Bengaluru",
    "Hyderabad", "Ahmedabad", "Pune", "Jaipur", "Lucknow",
    "Bhopal", "Nagpur", "Patna", "Bhubaneswar", "Chandigarh"
]

api_key = os.environ.get("GOOGLE_API_KEY")


def fetch_distances(cities):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    limit = 100
    total = len(cities)
    chunk = max(1, limit // total)

    road_map = {city: [] for city in cities}
    batches = [cities[i:i+chunk] for i in range(0, total, chunk)]

    for idx, batch in enumerate(batches, start=1):
        print(f"Please wait...")
        params = {
            "origins": "|".join(batch),
            "destinations" : "|".join(cities),
            "key": api_key
        }

        try:
            resp = requests.get(url, params=params).json()
        except requests.RequestException as e:
            print(f"Network error on batch {idx}: {e}")
            return None

        if resp.get("status") != "OK":
            print(f"API error on batch {idx}: {resp.get('status')} — {resp.get('error_message', 'no details')}")
            return None

        for i, origin in enumerate(batch):
            for j, destination in enumerate(cities):
                if origin != destination:
                    try:
                        entry = resp["rows"][i]["elements"][j]
                        if entry["status"] != "OK":
                            raise KeyError("entry status not OK")
                        km = entry["distance"]["value"] // 1000
                    except KeyError:
                        print(f"  Warning: could not get distance from {origin} to {destination}, setting to infinity!")
                        km = float('inf')

                    road_map[origin].append((destination, km))

    return road_map


def save_cache(road_map, cities):
    payload = {"city_list": cities, "graph": road_map}
    with open(cache_file, "w") as f:
        json.dump(payload, f, indent=2)


def load_cache():
    if not os.path.exists(cache_file):
        return None, None
    try:
        with open(cache_file,"r") as f:
            payload = json.load(f)
        return payload["graph"], payload["city_list"]
    except (json.JSONDecodeError, KeyError):
        print("Cache file was corrupted, will rebuild.")
        return None,None


def add_to_graph(current_map, current_cities, incoming):
    merged = current_cities + incoming
    print(f"Fetching distances for {len(incoming)} new city/cities against all {len(merged)} cities...")
    updated_map = fetch_distances(merged)

    if updated_map is None:
        return None, None
    return updated_map, merged


def dijkstra(road_map, start):
    heap = []
    heapq.heappush(heap, (0,start))

    dist = {city: float('inf') for city in road_map}
    came_from = {city: None for city in road_map}
    seen = set()
    dist[start] = 0

    while heap:
        cost, current = heapq.heappop(heap)

        if current in seen:
            continue
        seen.add(current)

        for neighbor,weight in road_map[current]:
            new_cost = cost+weight

            if new_cost < dist[neighbor]:
                dist[neighbor] = new_cost
                came_from[neighbor] = current
                heapq.heappush(heap, (new_cost,neighbor))

    return dist, came_from


def get_path(came_from, target):
    path = []
    depth_limit = len(came_from)+1
    hops = 0

    while target:
        path.append(target)
        target = came_from[target]
        hops += 1
        if hops>depth_limit:
            print("Warning: Cycle detected!")
            break

    return path[::-1]


def clean(name):
    return name.strip().title()


road_map,city_list = load_cache()

if road_map is None:
    print(f"No cache found. Building graph for {len(default_cities)} preset cities")
    road_map = fetch_distances(default_cities)

    if road_map is None:
        print("Could not build graph on startup. Please enter the cities manually and refresh the graph, or try building preset graph again using option 2.")
        city_list = default_cities[:]
    else:
        city_list = default_cities[:]
        save_cache(road_map, city_list)
        print("Graph ready.\n")
else:
    print(f"Loaded graph from cache ({len(city_list)} cities)")

while True:
    print("\n1. Add Cities")
    print("2. Refresh Graph (force API call)")
    print("3. Find Shortest Path")
    print("4. Show Current Cities")
    print("5. Exit")

    try:
        choice = int(input("Enter choice: "))
    except ValueError:
        print("Please enter a number between 1 and 5.")
        continue

    if choice==1:
        if not api_key:
            print("Adding cities requires a Google Maps API key.")
            print("Add it to a .env file as: GOOGLE_API_KEY=your_key_here")
            print("Read more regarding this in the README.md file")
            continue

        raw = input("Enter cities to add (comma separated): ").split(",")
        incoming = [clean(c) for c in raw]
        new_ones = [c for c in incoming if c not in city_list]

        if not new_ones:
            print("All entered cities are already in the graph.")
            continue

        print(f"Adding: {', '.join(new_ones)}")
        updated_map,updated_cities = add_to_graph(road_map, city_list, new_ones)

        if updated_map is None:
            print("Could not expand graph, keeping existing one.")
        else:
            road_map = updated_map
            city_list = updated_cities
            save_cache(road_map, city_list)
            print(f"Graph updated and cached. There are now {len(city_list)} cities.")

    elif choice==2:
        if not api_key:
            print("Refreshing the graph requires a Google Maps API key.")
            print("Add it to a .env file as: GOOGLE_API_KEY=your_key_here")
            print("Read more regarding this in the README.md file")
            continue

        print(f"Forcing full rebuild for all {len(city_list)} cities...")
        rebuilt = fetch_distances(city_list)

        if rebuilt is None:
            print("Rebuild failed, keeping existing graph")
        else:
            road_map = rebuilt
            save_cache(road_map, city_list)
            print("Graph rebuilt and graph_cache.json updated")

    elif choice == 3:
        if road_map is None:
            print("Graph is not available, try option 2 to rebuild")
            continue

        print("\nAvailable cities:")
        for city in road_map:
            print(city)

        src = clean(input("\nEnter source city: "))
        dst = clean(input("Enter destination city: "))

        if src not in road_map or dst not in road_map:
            print("Invalid city. Please ensure that the name matches one of the cities listed above, or add a valid city using Option 1 (requires API call)")
            continue

        if src==dst:
            print("Source and destination are the same city, hence distance is 0 km")
            continue

        dist,came_from = dijkstra(road_map, src)

        print("\nShortest Distance:", dist[dst], "km")
        print("Path:", " -> ".join(get_path(came_from, dst)))

    elif choice == 4:
        if not city_list:
            print("No cities in graph yet")
        else:
            print(f"\nCurrent cities ({len(city_list)}):")
            for city in city_list:
                print(f"  {city}")

    elif choice == 5:
        break

    else:
        print("Invalid choice. Please enter a number between 1 and 5")

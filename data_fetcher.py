import json
import time
import requests

REGION_NAME = "Chicago Metropolitan Area, Illinois, USA"

# 1. Cities
CITIES = [
    "Chicago, Illinois, USA",
    "Evanston, Illinois, USA",
    "Skokie, Illinois, USA",
    "Naperville, Illinois, USA",
    "Aurora, Illinois, USA",
    "Joliet, Illinois, USA",
    "Elgin, Illinois, USA",
    "Waukegan, Illinois, USA",
    "Cicero, Illinois, USA",
    "Arlington Heights, Illinois, USA",
    "Schaumburg, Illinois, USA",
    "Palatine, Illinois, USA",
    "Orland Park, Illinois, USA",
    "Tinley Park, Illinois, USA",
    "Oak Lawn, Illinois, USA",
    "Berwyn, Illinois, USA",
    "Des Plaines, Illinois, USA",
    "Wheaton, Illinois, USA",
    "Downers Grove, Illinois, USA",
    "Bolingbrook, Illinois, USA",
    "Oak Park, Illinois, USA",
    "Elmhurst, Illinois, USA",
]

# 2. Road connections between cities
CONNECTIONS = [
    ("Chicago, Illinois, USA", "Cicero, Illinois, USA"),
    ("Chicago, Illinois, USA", "Oak Park, Illinois, USA"),
    ("Chicago, Illinois, USA", "Evanston, Illinois, USA"),
    ("Chicago, Illinois, USA", "Oak Lawn, Illinois, USA"),
    ("Chicago, Illinois, USA", "Berwyn, Illinois, USA"),
    ("Cicero, Illinois, USA", "Berwyn, Illinois, USA"),
    ("Oak Park, Illinois, USA", "Elmhurst, Illinois, USA"),
    ("Elmhurst, Illinois, USA", "Downers Grove, Illinois, USA"),
    ("Downers Grove, Illinois, USA", "Naperville, Illinois, USA"),
    ("Naperville, Illinois, USA", "Aurora, Illinois, USA"),
    ("Naperville, Illinois, USA", "Bolingbrook, Illinois, USA"),
    ("Bolingbrook, Illinois, USA", "Joliet, Illinois, USA"),
    ("Joliet, Illinois, USA", "Orland Park, Illinois, USA"),
    ("Orland Park, Illinois, USA", "Tinley Park, Illinois, USA"),
    ("Tinley Park, Illinois, USA", "Oak Lawn, Illinois, USA"),
    ("Evanston, Illinois, USA", "Skokie, Illinois, USA"),
    ("Skokie, Illinois, USA", "Des Plaines, Illinois, USA"),
    ("Des Plaines, Illinois, USA", "Arlington Heights, Illinois, USA"),
    ("Arlington Heights, Illinois, USA", "Palatine, Illinois, USA"),
    ("Palatine, Illinois, USA", "Schaumburg, Illinois, USA"),
    ("Schaumburg, Illinois, USA", "Elgin, Illinois, USA"),
    ("Elgin, Illinois, USA", "Aurora, Illinois, USA"),
    ("Des Plaines, Illinois, USA", "Schaumburg, Illinois, USA"),
    ("Arlington Heights, Illinois, USA", "Schaumburg, Illinois, USA"),
    ("Waukegan, Illinois, USA", "Evanston, Illinois, USA"),
    ("Waukegan, Illinois, USA", "Des Plaines, Illinois, USA"),
    ("Elmhurst, Illinois, USA", "Schaumburg, Illinois, USA"),
    ("Wheaton, Illinois, USA", "Elmhurst, Illinois, USA"),
    ("Wheaton, Illinois, USA", "Naperville, Illinois, USA"),
    ("Wheaton, Illinois, USA", "Downers Grove, Illinois, USA"),
]

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OSRM_URL = "http://router.project-osrm.org/route/v1/driving"
HEADERS = {"User-Agent": "CS411-AI-Search-Visualizer/1.0"}


def short_name(full_name):
    """'Chicago, Illinois, USA' -> 'Chicago'"""
    return full_name.split(",")[0].strip()


def geocode(place_name):
    """Return (lat, lon) for a place using the Nominatim API."""
    params = {"q": place_name, "format": "json", "limit": 1}
    resp = requests.get(NOMINATIM_URL, params=params, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    results = resp.json()
    if not results:
        raise ValueError(f"Nominatim could not geocode: {place_name}")
    return float(results[0]["lat"]), float(results[0]["lon"])


def route_distance_km(lat1, lon1, lat2, lon2):
    """Return driving distance in kilometers between two coordinates using OSRM."""
    coords = f"{lon1},{lat1};{lon2},{lat2}"  # OSRM expects lon,lat order
    url = f"{OSRM_URL}/{coords}"
    params = {"overview": "false"}
    resp = requests.get(url, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != "Ok":
        raise ValueError(f"OSRM routing failed: {data}")
    meters = data["routes"][0]["distance"]
    return round(meters / 1000.0, 2)


def build_graph():
    nodes = {}
    print(f"Geocoding {len(CITIES)} cities via Nominatim...")
    for city in CITIES:
        name = short_name(city)
        lat, lon = geocode(city)
        nodes[name] = {"lat": lat, "lon": lon}
        print(f"  {name}: ({lat}, {lon})")
        time.sleep(1)

    edges = []
    print(f"\nFetching {len(CONNECTIONS)} road distances via OSRM...")
    for a_full, b_full in CONNECTIONS:
        a, b = short_name(a_full), short_name(b_full)
        lat1, lon1 = nodes[a]["lat"], nodes[a]["lon"]
        lat2, lon2 = nodes[b]["lat"], nodes[b]["lon"]
        distance = route_distance_km(lat1, lon1, lat2, lon2)
        edges.append({"from": a, "to": b, "distance": distance})
        print(f"  {a} <-> {b}: {distance} km")
        time.sleep(0.5)

    return {"region": REGION_NAME, "nodes": nodes, "edges": edges}


def main():
    graph = build_graph()
    with open("map_data.json", "w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2) 
    print(f"\nSaved graph with {len(graph['nodes'])} nodes and "
          f"{len(graph['edges'])} edges to map_data.json")


if __name__ == "__main__":
    main()

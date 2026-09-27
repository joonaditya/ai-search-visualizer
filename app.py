import json
import os

from flask import Flask, jsonify, render_template, request

from uninformed import bfs, dfs, ucs, ids
from informed import greedy_best_first, a_star

app = Flask(__name__)

MAP_DATA_PATH = os.path.join(os.path.dirname(__file__), "map_data.json")

ALGORITHM_CONCEPTS = {
    "bfs": {
        "name": "Breadth-First Search (BFS)",
        "main_idea": "Explores the graph level by level, expanding all nodes at the "
                      "current depth before moving to the next depth.",
        "node_selection": "Chooses the node that has been in the frontier the longest "
                           "(FIFO queue).",
        "information_used": "Depth only (number of edges from the start). It does not "
                             "consider path cost or heuristics.",
    },
    "dfs": {
        "name": "Depth-First Search (DFS)",
        "main_idea": "Explores as far as possible along each branch before backtracking.",
        "node_selection": "Chooses the most recently discovered node that still has "
                           "unexplored neighbors (LIFO stack).",
        "information_used": "Depth only. It does not consider path cost or heuristics, "
                             "so it is not guaranteed to find the shortest path.",
    },
    "ucs": {
        "name": "Uniform-Cost Search (UCS)",
        "main_idea": "Expands the node with the lowest cumulative path cost from the "
                      "start, guaranteeing the cheapest path is found first.",
        "node_selection": "Chooses the frontier node with the smallest g(n) (cost so far), "
                           "using a priority queue.",
        "information_used": "Path cost g(n) only, no heuristic information.",
    },
    "ids": {
        "name": "Iterative Deepening Search (IDS)",
        "main_idea": "Performs repeated depth-limited DFS with an increasing depth limit "
                      "(0, 1, 2, ...) until the goal is found, combining DFS's low memory "
                      "use with BFS's completeness.",
        "node_selection": "Same as DFS, but nodes deeper than the current depth limit "
                           "are not expanded.",
        "information_used": "Depth only, evaluated against the current iteration's limit.",
    },
    "greedy": {
        "name": "Greedy Best-First Search",
        "main_idea": "Expands the node that appears closest to the goal, using only a "
                      "heuristic estimate and ignoring the cost already spent.",
        "node_selection": "Chooses the frontier node with the smallest heuristic value h(n), "
                           "the straight-line distance to the goal.",
        "information_used": "Heuristic information h(n) only. Fast, but not guaranteed to "
                             "be optimal.",
    },
    "astar": {
        "name": "A* Search",
        "main_idea": "Combines the cost already spent with an estimate of the cost "
                      "remaining, expanding the node that minimizes the total estimated "
                      "cost of a solution through it.",
        "node_selection": "Chooses the frontier node with the smallest f(n) = g(n) + h(n).",
        "information_used": "Both path cost g(n) and heuristic h(n) (straight-line distance "
                             "to the goal). Optimal when h(n) is admissible.",
    },
}

# Uniform wrapper signature (graph, coords, source, goal) so the /api/search
# route can call any algorithm the same way, even the ones that ignore coords.
ALGORITHMS = {
    "bfs": lambda graph, coords, s, g: bfs(graph, s, g),
    "dfs": lambda graph, coords, s, g: dfs(graph, s, g),
    "ucs": lambda graph, coords, s, g: ucs(graph, s, g),
    "ids": lambda graph, coords, s, g: ids(graph, s, g),
    "greedy": lambda graph, coords, s, g: greedy_best_first(graph, coords, s, g),
    "astar": lambda graph, coords, s, g: a_star(graph, coords, s, g),
}


def load_map_data():
    with open(MAP_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def build_adjacency_list(map_data):
    """Convert the edge list into an undirected weighted adjacency list."""
    graph = {city: [] for city in map_data["nodes"]}
    for edge in map_data["edges"]:
        a, b, dist = edge["from"], edge["to"], edge["distance"]
        graph[a].append((b, dist))  # roads are two-way, so add both directions
        graph[b].append((a, dist))
    return graph


def build_coords(map_data):
    #flatten each city's lat/lon into a simple lookup used by the heuristic functions
    return {city: (info["lat"], info["lon"]) for city, info in map_data["nodes"].items()}


#loaded once at startup so every request reuses the same in-memory graph
MAP_DATA = load_map_data()
GRAPH = build_adjacency_list(MAP_DATA)
COORDS = build_coords(MAP_DATA)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/map", methods=["GET"])
def get_map():
    """Return the full graph (nodes + edges) for rendering on the map."""
    return jsonify(MAP_DATA)


@app.route("/api/algorithms", methods=["GET"])
def get_algorithms():
    """Return the list of available algorithms and their concept notes."""
    return jsonify(ALGORITHM_CONCEPTS)


@app.route("/api/search", methods=["POST"])
def search():
    """Run the requested search algorithm between a source and destination."""
    payload = request.get_json(force=True) or {}
    source = payload.get("source")
    destination = payload.get("destination")
    algorithm = payload.get("algorithm")

    if not source or not destination or not algorithm:
        return jsonify({"error": "source, destination, and algorithm are required"}), 400
    if source not in GRAPH or destination not in GRAPH:
        return jsonify({"error": "Unknown source or destination city"}), 400
    if algorithm not in ALGORITHMS:
        return jsonify({"error": f"Unknown algorithm: {algorithm}"}), 400

    result = ALGORITHMS[algorithm](GRAPH, COORDS, source, destination)  # dispatch by name
    result["algorithm"] = algorithm
    result["concept"] = ALGORITHM_CONCEPTS[algorithm]
    result["source"] = source
    result["destination"] = destination
    return jsonify(result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  #render injects PORT at runtime
    app.run(host="0.0.0.0", port=port, debug=True)

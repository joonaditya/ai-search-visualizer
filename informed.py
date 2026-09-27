import heapq
import math


def haversine(coord1, coord2):
    """Great-circle distance in kilometers between two (lat, lon) points."""
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    r = 6371.0  # Earth radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))  # standard haversine formula


def _heuristic(coords, node, goal):
    # Straight-line distance to the goal, used as h(n) in Greedy/A*
    return haversine(coords[node], coords[goal])


def _reconstruct_path(parent, start, goal):
    # Walk backwards from goal to start using the parent pointers then flip it
    path = [goal]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    return path


def _path_cost(graph, path):
    """Compute the total edge-weight cost of a path."""
    if not path or len(path) < 2:
        return 0.0
    cost = 0.0
    for a, b in zip(path, path[1:]):  # sum the weight of each consecutive edge
        for neighbor, weight in graph.get(a, []):
            if neighbor == b:
                cost += weight
                break
    return cost


def greedy_best_first(graph, coords, start, goal):
    """Greedy Best-First Search: always expands the node that looks closest
    to the goal according to the heuristic h(n), ignoring path cost so far."""
    counter = 0  # tie-breaker for heap comparisons
    frontier = [(_heuristic(coords, start, goal), counter, start)]
    visited = set()
    parent = {}
    order_expanded = []

    while frontier:
        _, _, current = heapq.heappop(frontier)  # pop the city that looks closest to goal
        if current in visited:
            continue
        visited.add(current)
        order_expanded.append(current)

        if current == goal:
            path = _reconstruct_path(parent, start, goal)
            cost = _path_cost(graph, path)
            return {"path": path, "cost": cost, "nodes_expanded": len(order_expanded),
                    "order_expanded": order_expanded}

        for neighbor, _weight in graph.get(current, []):
            if neighbor not in visited:
                if neighbor not in parent:
                    parent[neighbor] = current
                counter += 1
                heapq.heappush(frontier, (_heuristic(coords, neighbor, goal), counter, neighbor))

    return {"path": [], "cost": float("inf"), "nodes_expanded": len(order_expanded),
            "order_expanded": order_expanded}


def a_star(graph, coords, start, goal):
    """A* Search: expands the node with lowest f(n) = g(n) + h(n), where
    g(n) is the cost so far and h(n) is the straight-line-distance heuristic."""
    counter = 0
    g_cost = {start: 0.0}  # cheapest known cost from start to each city
    frontier = [(_heuristic(coords, start, goal), counter, start)]
    parent = {}
    visited = set()
    order_expanded = []

    while frontier:
        _, _, current = heapq.heappop(frontier)  # pop the city with lowest f = g + h
        if current in visited:
            continue
        visited.add(current)
        order_expanded.append(current)

        if current == goal:
            path = _reconstruct_path(parent, start, goal)
            return {"path": path, "cost": g_cost[goal], "nodes_expanded": len(order_expanded),
                    "order_expanded": order_expanded}

        for neighbor, weight in graph.get(current, []):
            tentative_g = g_cost[current] + weight
            if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                g_cost[neighbor] = tentative_g  # found a cheaper route to this city
                parent[neighbor] = current
                f_cost = tentative_g + _heuristic(coords, neighbor, goal)
                counter += 1
                heapq.heappush(frontier, (f_cost, counter, neighbor))

    return {"path": [], "cost": float("inf"), "nodes_expanded": len(order_expanded),
            "order_expanded": order_expanded}

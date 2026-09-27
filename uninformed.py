from collections import deque


def _reconstruct_path(parent, start, goal):
    # Walk backwards from goal to start using the parent pointers, then flip it.
    path = [goal]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    return path


def bfs(graph, start, goal):
    """Breadth-First Search: expands nodes level by level (FIFO queue)."""
    if start == goal:
        return {"path": [start], "cost": 0.0, "nodes_expanded": 1, "order_expanded": [start]}

    visited = {start}  # mark visited on enqueue so we never queue the same city twice
    parent = {}
    queue = deque([start])
    order_expanded = []

    while queue:
        current = queue.popleft()  # FIFO: oldest-discovered city goes first
        order_expanded.append(current)

        if current == goal:
            path = _reconstruct_path(parent, start, goal)
            cost = _path_cost(graph, path)
            return {"path": path, "cost": cost, "nodes_expanded": len(order_expanded),
                    "order_expanded": order_expanded}

        for neighbor, _weight in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    return {"path": [], "cost": float("inf"), "nodes_expanded": len(order_expanded),
            "order_expanded": order_expanded}


def dfs(graph, start, goal):
    """Depth-First Search: expands the deepest unexplored node first (LIFO stack)."""
    visited = set()
    parent = {}
    stack = [start]
    order_expanded = []

    while stack:
        current = stack.pop()  # LIFO: most recently pushed city goes first
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
                parent.setdefault(neighbor, current)  # keep the first parent found
                stack.append(neighbor)

    return {"path": [], "cost": float("inf"), "nodes_expanded": len(order_expanded),
            "order_expanded": order_expanded}


def ucs(graph, start, goal):
    """Uniform-Cost Search: always expands the node with the lowest path cost so far."""
    import heapq

    frontier = [(0.0, start)]  # min-heap ordered by cumulative cost
    best_cost = {start: 0.0}
    parent = {}
    visited = set()
    order_expanded = []

    while frontier:
        cost, current = heapq.heappop(frontier)  # pop the cheapest-so-far city
        if current in visited:
            continue
        visited.add(current)
        order_expanded.append(current)

        if current == goal:
            path = _reconstruct_path(parent, start, goal)
            return {"path": path, "cost": cost, "nodes_expanded": len(order_expanded),
                    "order_expanded": order_expanded}

        for neighbor, weight in graph.get(current, []):
            new_cost = cost + weight
            if neighbor not in best_cost or new_cost < best_cost[neighbor]:
                best_cost[neighbor] = new_cost  # found a cheaper route to this city
                parent[neighbor] = current
                heapq.heappush(frontier, (new_cost, neighbor))

    return {"path": [], "cost": float("inf"), "nodes_expanded": len(order_expanded),
            "order_expanded": order_expanded}


def ids(graph, start, goal, max_depth=50):
    """Iterative Deepening Search: repeated depth-limited DFS with increasing depth limit."""
    total_expanded = 0
    order_expanded_all = []

    for depth_limit in range(max_depth + 1):  # re-run DFS with a deeper cutoff each time
        visited = {}
        result = _depth_limited_dfs(graph, start, goal, depth_limit, visited, order_expanded_all)
        total_expanded = len(order_expanded_all)
        if result is not None:
            path, parent = result
            cost = _path_cost(graph, path)
            return {"path": path, "cost": cost, "nodes_expanded": total_expanded,
                    "order_expanded": order_expanded_all}

    return {"path": [], "cost": float("inf"), "nodes_expanded": total_expanded,
            "order_expanded": order_expanded_all}


def _depth_limited_dfs(graph, start, goal, limit, visited, order_expanded_all):
    """Helper for IDS: depth-limited DFS that returns (path, parent) or None."""
    stack = [(start, 0, [start])]  # each stack entry carries the full path so far

    while stack:
        current, depth, path_so_far = stack.pop()
        order_expanded_all.append(current)

        if current == goal:
            return path_so_far, None

        if depth < limit:  # only expand further if we haven't hit this iteration's depth cap
            for neighbor, _weight in graph.get(current, []):
                if neighbor not in path_so_far:  # avoid cycles within this path
                    stack.append((neighbor, depth + 1, path_so_far + [neighbor]))

    return None


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

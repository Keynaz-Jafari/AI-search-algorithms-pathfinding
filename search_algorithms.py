from collections import deque
from collections.abc import Callable
from heapq import heappop, heappush
from time import perf_counter
from typing import Dict, List, Optional, Set, Tuple

from grid import Grid, Position
from search_result import SearchResult


NeighborFunction = Callable[[Position], List[Position]]


def _build_result(
    algorithm: str,
    path: Optional[List[Position]],
    visited_nodes: int,
    started_at: float,
) -> SearchResult:
    execution_time_ms = (perf_counter() - started_at) * 1000
    return SearchResult(
        algorithm=algorithm,
        path_found=path is not None,
        path_length=(len(path) - 1) if path else 0,
        visited_nodes=visited_nodes,
        execution_time_ms=execution_time_ms,
        path=path,
    )


def build_empty_result(algorithm: str) -> SearchResult:
    return SearchResult(
        algorithm=algorithm,
        path_found=False,
        path_length=0,
        visited_nodes=0,
        execution_time_ms=0.0,
        path=None,
    )


def validate_search_inputs(grid: Grid, get_neighbors: NeighborFunction) -> None:
    if not grid.is_walkable(grid.start):
        raise ValueError("Start position must be walkable.")
    if not grid.is_walkable(grid.goal):
        raise ValueError("Goal position must be walkable.")
    if not callable(get_neighbors):
        raise TypeError("get_neighbors must be callable.")


def reconstruct_path(
    parents: Dict[Position, Optional[Position]],
    goal: Position,
) -> List[Position]:
    path = [goal]
    current = goal

    while parents[current] is not None:
        current = parents[current]
        path.append(current)

    path.reverse()
    return path


def manhattan_distance(position: Position, goal: Position) -> int:
    row, col = position
    goal_row, goal_col = goal
    return abs(row - goal_row) + abs(col - goal_col)


def breadth_first_search(grid: Grid) -> SearchResult:
    algorithm = "BFS"
    started_at = perf_counter()
    validate_search_inputs(grid, grid.get_neighbors)

    frontier = deque([grid.start])
    parents: Dict[Position, Optional[Position]] = {grid.start: None}
    visited: Set[Position] = set()
    visited_nodes = 0

    while frontier:
        current = frontier.popleft()
        if current in visited:
            continue

        visited.add(current)
        visited_nodes += 1

        if current == grid.goal:
            return _build_result(
                algorithm,
                reconstruct_path(parents, grid.goal),
                visited_nodes,
                started_at,
            )

        for neighbor in grid.get_neighbors(current):
            if neighbor not in parents:
                parents[neighbor] = current
                frontier.append(neighbor)

    return _build_result(algorithm, None, visited_nodes, started_at)


def depth_first_search(grid: Grid) -> SearchResult:
    algorithm = "DFS"
    started_at = perf_counter()
    validate_search_inputs(grid, grid.get_neighbors)

    stack = [grid.start]
    parents: Dict[Position, Optional[Position]] = {grid.start: None}
    visited: Set[Position] = set()
    visited_nodes = 0

    while stack:
        current = stack.pop()
        if current in visited:
            continue

        visited.add(current)
        visited_nodes += 1

        if current == grid.goal:
            return _build_result(
                algorithm,
                reconstruct_path(parents, grid.goal),
                visited_nodes,
                started_at,
            )

        neighbors = grid.get_neighbors(current)
        for neighbor in reversed(neighbors):
            if neighbor not in visited and neighbor not in parents:
                parents[neighbor] = current
                stack.append(neighbor)

    return _build_result(algorithm, None, visited_nodes, started_at)


def _depth_limited_search(
    grid: Grid,
    limit: int,
) -> Tuple[Optional[List[Position]], int]:
    visited_nodes = 0
    path = [grid.start]
    path_set = {grid.start}

    def search(
        current: Position,
        remaining_depth: int,
    ) -> Optional[List[Position]]:
        nonlocal visited_nodes
        visited_nodes += 1

        if current == grid.goal:
            return list(path)
        if remaining_depth == 0:
            return None

        for neighbor in grid.get_neighbors(current):
            if neighbor in path_set:
                continue
            path.append(neighbor)
            path_set.add(neighbor)
            result = search(neighbor, remaining_depth - 1)
            if result is not None:
                return result
            path_set.remove(neighbor)
            path.pop()

        return None

    return search(grid.start, limit), visited_nodes


def iterative_deepening_search(grid: Grid) -> SearchResult:
    algorithm = "IDS"
    started_at = perf_counter()
    validate_search_inputs(grid, grid.get_neighbors)

    max_depth = grid.rows * grid.cols
    total_visited_nodes = 0

    for depth_limit in range(max_depth + 1):
        path, visited_nodes = _depth_limited_search(grid, depth_limit)
        total_visited_nodes += visited_nodes

        if path is not None:
            return _build_result(
                algorithm,
                path,
                total_visited_nodes,
                started_at,
            )

    return _build_result(algorithm, None, total_visited_nodes, started_at)


def greedy_best_first_search(grid: Grid) -> SearchResult:
    algorithm = "Greedy Best First Search"
    started_at = perf_counter()
    validate_search_inputs(grid, grid.get_neighbors)

    frontier: List[Tuple[int, int, Position]] = []
    heappush(frontier, (manhattan_distance(grid.start, grid.goal), 0, grid.start))
    parents: Dict[Position, Optional[Position]] = {grid.start: None}
    visited: Set[Position] = set()
    visited_nodes = 0
    order = 0

    while frontier:
        _, _, current = heappop(frontier)
        if current in visited:
            continue

        visited.add(current)
        visited_nodes += 1

        if current == grid.goal:
            return _build_result(
                algorithm,
                reconstruct_path(parents, grid.goal),
                visited_nodes,
                started_at,
            )

        for neighbor in grid.get_neighbors(current):
            if neighbor in visited or neighbor in parents:
                continue
            order += 1
            parents[neighbor] = current
            priority = manhattan_distance(neighbor, grid.goal)
            heappush(frontier, (priority, order, neighbor))

    return _build_result(algorithm, None, visited_nodes, started_at)


def a_star_search(grid: Grid) -> SearchResult:
    algorithm = "A* Search"
    started_at = perf_counter()
    validate_search_inputs(grid, grid.get_neighbors)

    frontier: List[Tuple[int, int, int, Position]] = []
    heappush(frontier, (manhattan_distance(grid.start, grid.goal), 0, 0, grid.start))
    parents: Dict[Position, Optional[Position]] = {grid.start: None}
    best_costs: Dict[Position, int] = {grid.start: 0}
    visited: Set[Position] = set()
    visited_nodes = 0
    order = 0

    while frontier:
        _, current_cost, _, current = heappop(frontier)
        if current in visited:
            continue

        visited.add(current)
        visited_nodes += 1

        if current == grid.goal:
            return _build_result(
                algorithm,
                reconstruct_path(parents, grid.goal),
                visited_nodes,
                started_at,
            )

        for neighbor in grid.get_neighbors(current):
            new_cost = current_cost + 1
            if new_cost >= best_costs.get(neighbor, float("inf")):
                continue

            best_costs[neighbor] = new_cost
            parents[neighbor] = current
            order += 1
            priority = new_cost + manhattan_distance(neighbor, grid.goal)
            heappush(frontier, (priority, new_cost, order, neighbor))

    return _build_result(algorithm, None, visited_nodes, started_at)


def run_all_searches(grid: Grid) -> List[SearchResult]:
    return [
        breadth_first_search(grid),
        depth_first_search(grid),
        iterative_deepening_search(grid),
        greedy_best_first_search(grid),
        a_star_search(grid),
    ]

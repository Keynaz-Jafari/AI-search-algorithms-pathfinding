from grid import Grid, Position, load_grid
from search_algorithms import run_all_searches
from typing import List


def assert_valid_path(grid: Grid, path: List[Position]) -> None:
    assert path[0] == grid.start
    assert path[-1] == grid.goal

    for current, next_position in zip(path, path[1:]):
        row, col = current
        next_row, next_col = next_position
        assert abs(row - next_row) + abs(col - next_col) == 1
        assert grid.is_walkable(next_position)


def main() -> None:
    grid = load_grid("map.txt")
    results = run_all_searches(grid)

    for result in results:
        assert result.path_found, f"{result.algorithm} did not find a path."
        assert result.path is not None
        assert result.path_length == len(result.path) - 1
        assert_valid_path(grid, result.path)

    bfs_result = next(result for result in results if result.algorithm == "BFS")
    astar_result = next(result for result in results if result.algorithm == "A* Search")
    assert bfs_result.path_length == astar_result.path_length

    print("Sanity checks passed.")


if __name__ == "__main__":
    main()

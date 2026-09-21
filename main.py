from grid import load_grid
from search_algorithms import run_all_searches


def format_comparison_table(results) -> str:
    headers = [
        "Algorithm",
        "Path Found",
        "Path Length",
        "Visited Nodes",
        "Execution Time",
    ]
    rows = [
        [
            result.algorithm,
            "Yes" if result.path_found else "No",
            str(result.path_length),
            str(result.visited_nodes),
            f"{result.execution_time_ms:.3f} ms",
        ]
        for result in results
    ]

    widths = [
        max(len(headers[index]), *(len(row[index]) for row in rows))
        for index in range(len(headers))
    ]
    header_line = " | ".join(
        headers[index].ljust(widths[index]) for index in range(len(headers))
    )
    separator = "-+-".join("-" * width for width in widths)
    body = "\n".join(
        " | ".join(row[index].ljust(widths[index]) for index in range(len(headers)))
        for row in rows
    )
    return f"{header_line}\n{separator}\n{body}"


def main() -> None:
    grid = load_grid("map.txt")
    obstacle_count = sum(row.count("X") for row in grid.cells)
    open_count = grid.rows * grid.cols - obstacle_count

    print("Grid loaded successfully.")
    print(f"Rows : {grid.rows}")
    print(f"Cols : {grid.cols}")
    print(f"Start : {grid.start}")
    print(f"Goal : {grid.goal}")
    print(f"Obstacles : {obstacle_count}")
    print(f"Open Cells : {open_count}")
    print(f"Start Neighbors : {grid.get_neighbors(grid.start)}")
    print()

    results = run_all_searches(grid)
    for result in results:
        print(result.display())
        print()

    print("Comparison Table")
    print(format_comparison_table(results))


if __name__ == "__main__":
    main()

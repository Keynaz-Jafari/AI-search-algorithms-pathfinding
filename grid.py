from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Union


Position = Tuple[int, int]


@dataclass(frozen=True)
class Grid:
    cells: Tuple[str, ...]
    start: Position
    goal: Position

    @property
    def rows(self) -> int:
        return len(self.cells)

    @property
    def cols(self) -> int:
        return len(self.cells[0]) if self.cells else 0

    def in_bounds(self, position: Position) -> bool:
        row, col = position
        return 0 <= row < self.rows and 0 <= col < self.cols

    def is_obstacle(self, position: Position) -> bool:
        row, col = position
        return self.cells[row][col] == "X"

    def is_walkable(self, position: Position) -> bool:
        return self.in_bounds(position) and not self.is_obstacle(position)

    def get_neighbors(self, position: Position) -> List[Position]:
        row, col = position
        candidates = [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1),
        ]
        return [candidate for candidate in candidates if self.is_walkable(candidate)]


def load_grid(map_file: Union[str, Path] = "map.txt") -> Grid:
    path = Path(map_file)
    lines = [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    if not lines:
        raise ValueError("Map file is empty.")

    width = len(lines[0])
    if any(len(line) != width for line in lines):
        raise ValueError("All map rows must have the same length.")

    allowed_symbols = {"S", "G", ".", "X"}
    start_positions: List[Position] = []
    goal_positions: List[Position] = []

    for row, line in enumerate(lines):
        for col, symbol in enumerate(line):
            if symbol not in allowed_symbols:
                raise ValueError(f"Invalid map symbol: {symbol!r}")
            if symbol == "S":
                start_positions.append((row, col))
            elif symbol == "G":
                goal_positions.append((row, col))

    if len(start_positions) != 1:
        raise ValueError("Map must contain exactly one start position marked with S.")
    if len(goal_positions) != 1:
        raise ValueError("Map must contain exactly one goal position marked with G.")

    return Grid(
        cells=tuple(lines),
        start=start_positions[0],
        goal=goal_positions[0],
    )

from dataclasses import dataclass
from typing import List, Optional

from grid import Position


@dataclass(frozen=True)
class SearchResult:
    algorithm: str
    path_found: bool
    path_length: int
    visited_nodes: int
    execution_time_ms: float
    path: Optional[List[Position]]

    def display(self) -> str:
        found_text = "Yes" if self.path_found else "No"
        path_text = self.path if self.path is not None else []
        return (
            f"Algorithm : {self.algorithm}\n"
            f"Path Found : {found_text}\n"
            f"Path Length : {self.path_length}\n"
            f"Visited Nodes : {self.visited_nodes}\n"
            f"Execution Time : {self.execution_time_ms:.3f} ms\n"
            f"Path : {path_text}"
        )

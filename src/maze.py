from src.cell import Cell
from typing import Any


class Maze:

    def __init__(self, config: dict[str, Any]) -> None:

        self.width: int = config["WIDTH"]
        self.height: int = config["HEIGHT"]
        self.entry: tuple[int] = config["ENTRY"]
        self.exit: tuple[int] = config["EXIT"]
        self.output: str = config["OUTPUT_FILE"]
        self.perfect: bool = config["PERFECT"]
        self.initialize_maze()

    def create_maze(self) -> None:
        pass

    def initialize_maze(self) -> None:

        maze = []

        for _ in range(self.height):
            row = []
            for _ in range(self.width):
                row.append(Cell())
            maze.append(row)

        self.maze = maze

    def __str__(self) -> str:

        result = ""

        for row in self.maze:
            result += ("".join(str(cell) for cell in row)) + "\n"
        return result

    def __repr__(self) -> str:
        return '\n'.join(str(row) for row in self.maze)

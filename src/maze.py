from src.cell import Cell
from src.cell import Direction
import random
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

    def create_maze(self, col: int, row: int) -> None:

        self.maze[row][col].visited = True
        directions = [
            Direction.north,
            Direction.east,
            Direction.south,
            Direction.west
            ]
        random.shuffle(directions)

        for direction in directions:
            match direction:
                case Direction.north:
                    if row > 0 and not self.maze[row - 1][col].visited:
                        self.maze[row][col].open_wall(Direction.north)
                        self.maze[row - 1][col].open_wall(Direction.south)
                        self.create_maze(row=(row - 1), col=col)

                case Direction.south:
                    if row < self.height - 1 and not self.maze[row + 1][col].visited:
                        self.maze[row][col].open_wall(Direction.south)
                        self.maze[row + 1][col].open_wall(Direction.north)
                        self.create_maze(row=(row + 1), col=col)

                case Direction.east:
                    if col < self.width - 1 and not self.maze[row][col + 1].visited:
                        self.maze[row][col].open_wall(Direction.east)
                        self.maze[row][col + 1].open_wall(Direction.west)
                        self.create_maze(row=row, col=(col + 1))

                case Direction.west:
                    if col > 0 and not self.maze[row][col - 1].visited:
                        self.maze[row][col].open_wall(Direction.west)
                        self.maze[row][col - 1].open_wall(Direction.east)
                        self.create_maze(row=row, col=(col - 1))

    def initialize_maze(self) -> None:

        maze: list[list[Cell]] = []

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

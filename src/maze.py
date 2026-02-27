from src.cell import Cell
from src.cell import Direction
import random
import time
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
        self.print_maze()

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

        for i in range(self.height):
            row: list[Cell] = []

            for j in range(self.width):
                row.append(Cell())

                if i == self.entry[1] and j == self.entry[0]:
                    row[j].is_entry = True
                elif i == self.exit[1] and j == self.exit[0]:
                    row[j].is_exit = True

            maze.append(row)

        self.maze = maze

    def print_maze(self):
        print("\033[2J\033[H")
        WALL_COLOR = '\033[48;2;1;155;156m  \033[0m'
        START_COLOR = '\033[48;2;3;12;142m  \033[0m'
        END_COLOR = '\033[48;2;200;3;101m  \033[0m'
        PATH_COLOR = '\033[40m  \033[0m'

        print(WALL_COLOR * (self.width * 2 + 1))

        for row in self.maze:
            line_str = WALL_COLOR

            for cell in row:
                if cell.is_entry:
                    line_str += START_COLOR
                elif cell.is_exit:
                    line_str += END_COLOR
                else:
                    line_str += PATH_COLOR

                if cell.is_wall_closed(Direction.east):
                    line_str += WALL_COLOR
                else:
                    line_str += PATH_COLOR

            print(line_str)

            bottom_str = WALL_COLOR

            for cell in row:
                if cell.is_wall_closed(Direction.south):
                    bottom_str += WALL_COLOR
                else:
                    bottom_str += PATH_COLOR

                bottom_str += WALL_COLOR

            print(bottom_str)
        time.sleep(0.1)

    def __str__(self) -> str:

        result = ""

        for row in self.maze:
            result += ("".join(str(cell) for cell in row)) + "\n"
        return result

    def __repr__(self) -> str:
        return '\n'.join(str(row) for row in self.maze)

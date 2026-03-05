"""Module for manage the Maze and relative methods."""

from mazegen.requirement_parser import MazeConfig
from mazegen.cell import Cell, Direction
from mazegen.themes import THEMES
from collections import deque
from typing import Optional
import subprocess
import platform
import random
import time


def clear_screen() -> None:
    """Clear the shell window."""
    if platform.system() == "Windows":
        print("\033[2J\033[H")
    else:
        subprocess.run("clear", shell=True)


class Maze:
    """Class representing a Maze."""

    def __init__(self, model: MazeConfig) -> None:
        """Initialize the object Maze.

        Args:
            model: Pydantic Base Model containing maze configuration.
        """
        config = model.model_dump()
        self.width: int = config["WIDTH"]
        self.height: int = config["HEIGHT"]
        self.entry: tuple[int, int] = config["ENTRY"]
        self.exit: tuple[int, int] = config["EXIT"]
        self.start: tuple[int, int] = (config["START"]
                                       if config["START"]
                                       else config["ENTRY"])
        self.output: str = config["OUTPUT_FILE"]
        self.perfect: bool = config["PERFECT"]
        self.algo: Optional[str] = config.get("ALGORITHM", None)
        self.theme: dict[str, str] = THEMES['default']
        self.seed: Optional[str] = config.get('SEED', None)
        self.random = False if config.get('SEED', None) else True
        self.path = ""
        self.error_message = ""
        self.animation = True
        self.solution = True
        self.two_forty = True
        self.maze = self.init_maze()

    @staticmethod
    def get_random_seed() -> str:
        """Generate a random seed.

        Returns:
            seed: the seed generated.
        """
        alpha: str = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"
        digit: str = "0123456789"
        symbol: str = "?!@#$%^&*()_-+={}[]:;|/<>,.\\"
        pool: str = alpha + digit + symbol
        seed: str = "".join([random.choice(pool)
                             for _ in range(random.randint(21, 42))])
        return seed

    def init_maze(self) -> list[list[Cell]]:
        """Initialize the proper maze as a list[list[Cell]].

        Returns:
            maze: the maze generated.
        """
        maze: list[list[Cell]] = []
        if self.random:
            self.seed = self.get_random_seed()
        random.seed(self.seed)

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

        if self.two_forty:
            if self.width < 9 or self.height < 7:
                self.error_message = "Maze too small to contain '42'"
            else:
                self.error_message = ""
                self.forty_two()

                if self.maze[self.entry[1]][self.entry[0]].visited == 42:
                    raise ValueError("[ERR] ENTRY inside the 42!\n")

                if self.maze[self.exit[1]][self.exit[0]].visited == 42:
                    raise ValueError("[ERR] EXIT inside the 42!\n")

                if self.maze[self.start[1]][self.start[0]].visited == 42:
                    raise ValueError("[ERR] STARTING POINT inside the 42!\n")
        return maze

    def never_been_there(self) -> None:
        """Set all visitable cells to <visited = 0>."""
        for row in self.maze:
            for cell in row:
                cell.is_solved = False
                cell.steps = 0
                if cell.visited != 42:
                    cell.visited = 0
        self.path = ""

    def forty_two(self) -> None:
        """Put number 42 inside the maze."""
        center_x = int((self.width - 1) / 2)
        center_y = int((self.height - 1) / 2)

        for i in range(center_x - 3, center_x + 4):
            if i != center_x - 2 and i != center_x - 1 and i != center_x:
                self.maze[center_y - 2][i].visited = 42

        self.maze[center_y - 1][center_x - 3].visited = 42
        self.maze[center_y - 1][center_x + 3].visited = 42

        for i in range(center_x - 3, center_x + 4):
            if i != center_x:
                self.maze[center_y][i].visited = 42

        self.maze[center_y + 1][center_x - 1].visited = 42
        self.maze[center_y + 1][center_x + 1].visited = 42

        for i in range(center_x - 3, center_x + 4):
            if i != center_x - 3 and i != center_x - 2 and i != center_x:
                self.maze[center_y + 2][i].visited = 42

    def create_maze(self) -> None:
        """Generate a maze using configuration algorithm."""
        match self.algo:

            case "backtrack":
                self.backtrack(self.start[1], self.start[0])

            case "prim":
                self.prim(self.start[1], self.start[0],
                          [(self.start[1], self.start[0])])

            case "kruskal":
                self.kruskal()

            case "nirugger":
                self.nirugger()

            case "eller":
                self.eller()

    def backtrack(self, col: int, row: int) -> None:
        """Backtrack algorithm for maze generation.

        Args:
            col: y-axis of the first cell.
            row: x-axis of the first cell.
        """
        self.maze[row][col].visited = 1
        directions = [
            Direction.north,
            Direction.east,
            Direction.south,
            Direction.west
            ]
        random.shuffle(directions)
        if (self.animation):
            self.print_maze()

        i = 0
        for direction in directions:
            match direction:

                case Direction.north:
                    if (row > 0
                            and not self.maze[row - 1][col].visited):

                        self.maze[row][col].open_wall(Direction.north)
                        self.maze[row - 1][col].open_wall(Direction.south)
                        self.backtrack(row=(row - 1), col=col)

                case Direction.south:
                    if (row < self.height - 1
                            and not self.maze[row + 1][col].visited):

                        self.maze[row][col].open_wall(Direction.south)
                        self.maze[row + 1][col].open_wall(Direction.north)
                        i += 1
                        self.backtrack(row=(row + 1), col=col)

                case Direction.east:
                    if (col < self.width - 1
                            and not self.maze[row][col + 1].visited):

                        self.maze[row][col].open_wall(Direction.east)
                        self.maze[row][col + 1].open_wall(Direction.west)
                        self.backtrack(row=row, col=(col + 1))

                case Direction.west:
                    if (col > 0
                            and not self.maze[row][col - 1].visited):

                        self.maze[row][col].open_wall(Direction.west)
                        self.maze[row][col - 1].open_wall(Direction.east)
                        self.backtrack(row=row, col=(col - 1))

    def prim(self,
             col: int,
             row: int,
             frontier: list[tuple[int, int]]) -> None:
        """Prim algorithm for maze generation.

        Args:
            col: y-axis of the first cell.
            row: x-axis of the first cell.
            frontier: list containing the coordinates of the first cell.
        """
        self.maze[row][col].visited = True
        directions = [
            Direction.north,
            Direction.east,
            Direction.south,
            Direction.west
            ]
        random.shuffle(directions)
        if (self.animation):
            self.print_maze()

        for direction in directions:
            match direction:

                case Direction.north:
                    if (row > 0
                            and not self.maze[row - 1][col].visited):

                        self.maze[row][col].open_wall(Direction.north)
                        self.maze[row - 1][col].open_wall(Direction.south)
                        frontier.append((col, row-1))

                        self.maze[row - 1][col].visited = True

                        item = random.choice(frontier)
                        self.prim(row=item[1],
                                  col=item[0],
                                  frontier=frontier)

                case Direction.south:
                    if (row < self.height - 1
                            and not self.maze[row + 1][col].visited):

                        self.maze[row][col].open_wall(Direction.south)
                        self.maze[row + 1][col].open_wall(Direction.north)
                        frontier.append((col, row+1))
                        self.maze[row + 1][col].visited = True

                        item = random.choice(frontier)

                        self.prim(row=item[1],
                                  col=item[0],
                                  frontier=frontier)

                case Direction.east:
                    if (col < self.width - 1
                            and not self.maze[row][col + 1].visited):

                        self.maze[row][col].open_wall(Direction.east)
                        self.maze[row][col + 1].open_wall(Direction.west)
                        self.maze[row][col + 1].visited = True

                        frontier.append((col+1, row))
                        item = random.choice(frontier)

                        self.prim(row=item[1],
                                  col=item[0],
                                  frontier=frontier)

                case Direction.west:
                    if (col > 0
                            and not self.maze[row][col - 1].visited):

                        self.maze[row][col].open_wall(Direction.west)
                        self.maze[row][col - 1].open_wall(Direction.east)
                        frontier.append((col-1, row))
                        self.maze[row][col-1].visited = True

                        item = random.choice(frontier)
                        self.prim(row=item[1],
                                  col=item[0],
                                  frontier=frontier)

        if (col, row) in frontier:
            frontier.remove((col, row))
        if frontier:
            item = random.choice(frontier)
            self.prim(col=item[0],
                      row=item[1],
                      frontier=frontier)

    def kruskal(self) -> None:
        """Kruskal algorithm for maze generation."""
        directions = [
            Direction.north,
            Direction.east,
            Direction.south,
            Direction.west
            ]

        krusk_list: list[set[tuple[int, int]]] = []
        for row in range(len(self.maze)):
            for col in range(len(self.maze[row])):
                if not self.maze[row][col].visited:
                    krusk_list.append({(row, col)})

        while len(krusk_list) > 1:

            flag = False
            if (self.animation):
                self.print_maze()
            this_set = random.choice(krusk_list)
            row, col = random.choice(tuple(this_set))
            random.shuffle(directions)

            for direction in directions:
                match direction:

                    case Direction.north:
                        if (row > 0
                                and (row - 1, col) not in this_set
                                and not self.maze[row - 1][col].visited):
                            flag = True
                            self.maze[row][col].open_wall(Direction.north)
                            self.maze[row - 1][col].open_wall(Direction.south)
                            for i in krusk_list:
                                if (row - 1, col) in i:
                                    this_set.update(i)
                                    krusk_list.remove(i)
                                    break
                        if flag:
                            break

                    case Direction.south:
                        if (row < self.height - 1
                                and (row + 1, col) not in this_set
                                and not self.maze[row + 1][col].visited):
                            flag = True
                            self.maze[row][col].open_wall(Direction.south)
                            self.maze[row + 1][col].open_wall(Direction.north)
                            for i in krusk_list:
                                if (row + 1, col) in i:
                                    this_set.update(i)
                                    krusk_list.remove(i)
                                    break
                        if flag:
                            break

                    case Direction.east:
                        if (col < self.width - 1
                                and (row, col + 1) not in this_set
                                and not self.maze[row][col + 1].visited):
                            flag = True
                            self.maze[row][col].open_wall(Direction.east)
                            self.maze[row][col + 1].open_wall(Direction.west)
                            for i in krusk_list:
                                if (row, col + 1) in i:
                                    this_set.update(i)
                                    krusk_list.remove(i)
                                    break
                        if flag:
                            break

                    case Direction.west:
                        if (col > 0
                                and (row, col - 1) not in this_set
                                and not self.maze[row][col - 1].visited):
                            flag = True
                            self.maze[row][col].open_wall(Direction.west)
                            self.maze[row][col - 1].open_wall(Direction.east)
                            for i in krusk_list:
                                if (row, col - 1) in i:
                                    this_set.update(i)
                                    krusk_list.remove(i)
                                    break
                        if flag:
                            break

    def eller(self) -> None:
        """Eller algorithm for maze generation."""
        self.start = (0, 0)
        el_list: list[set[tuple[int, int]]] = []
        for col in range(len(self.maze[0])):
            el_list.append({(0, col)})

        for row in range(len(self.maze)):

            # per ogni set prendere un elemento random e collegarloaquellosotto
            # trattare la bottom line come edge case
            # fare controlli su celle adiacenti se visited
            for col in range(len(self.maze[row][col])):
                if not self.maze[row][col].visited:
                    if ((not col or not random.randint(0, 1)) and not
                            any((row, col) in coords for coords in el_list)):
                        continue
                    else:
                        pass

            for col in range(len(self.maze[row])):
                if not self.maze[row][col].visited:
                    if ((not col or not random.randint(0, 1)) and not
                            any((row, col) in coords for coords in el_list)):
                        el_list.append({(row, col)})
                    else:
                        el_list[len(el_list) - 1].update({(row, col)})
                        self.maze[row][col - 1].open_wall(Direction.east)
                        self.maze[row][col].open_wall(Direction.west)
                if self.animation:
                    self.print_maze()

            for col in range(len(self.maze[row])):
                if not self.maze[row][col].visited:
                    if row < self.height - 1 and random.randint(0, 1):
                        for coords in el_list:
                            if (row, col) in coords:
                                coords.update({(row + 1, col)})
                                self.maze[row + 1][col].open_wall(
                                    Direction.north
                                    )
                                self.maze[row][col].open_wall(Direction.south)
                if self.animation:
                    self.print_maze()

    def nirugger(self) -> None:
        """nirugger algorithm for maze generation."""
        self.make_it_empty()
        directions = [
            Direction.north,
            Direction.east,
            Direction.south,
            Direction.west
            ]

        for row in range(0, self.height):
            for col in range(0, self.width):

                if self.maze[row][col].total_closed() >= 2:
                    continue

                elif row == 0:
                    dir = random.choice(directions)
                    while dir == Direction.north:
                        dir = random.choice(directions)

                    if (dir == Direction.south and
                            self.maze[row + 1][col].total_closed() <= 1):
                        self.maze[row][col].close_wall(dir)
                        self.maze[row + 1][col].close_wall(Direction.north)

                    if (dir == Direction.east and col < self.width - 1 and
                            self.maze[row][col + 1].total_closed() <= 1):
                        self.maze[row][col].close_wall(dir)
                        self.maze[row][col + 1].close_wall(Direction.west)

                    if (dir == Direction.west and col > 0 and
                            self.maze[row][col - 1].total_closed() <= 1):
                        self.maze[row][col].close_wall(dir)
                        self.maze[row][col - 1].close_wall(Direction.east)

                elif row == self.height - 1:
                    dir = random.choice(directions)
                    while dir == Direction.south:
                        dir = random.choice(directions)

                    if (dir == Direction.north and
                            self.maze[row - 1][col].total_closed() <= 1):
                        self.maze[row - 1][col].close_wall(Direction.south)
                        self.maze[row][col].close_wall(dir)

                    if (dir == Direction.east and col < self.width - 1 and
                            self.maze[row][col + 1].total_closed() <= 1):
                        self.maze[row][col + 1].close_wall(Direction.west)
                        self.maze[row][col].close_wall(dir)

                    if (dir == Direction.west and col > 0 and
                            self.maze[row][col - 1].total_closed() <= 1):
                        self.maze[row][col - 1].close_wall(Direction.east)
                        self.maze[row][col].close_wall(dir)

                elif col == self.width - 1:
                    dir = random.choice(directions)
                    while dir == Direction.east:
                        dir = random.choice(directions)

                    if (dir == Direction.north and row > 0 and
                            self.maze[row - 1][col].total_closed() <= 1):
                        self.maze[row - 1][col].close_wall(Direction.south)
                        self.maze[row][col].close_wall(dir)

                    if (dir == Direction.south and
                            row < self.height - 1 and
                            self.maze[row + 1][col].total_closed() <= 1):
                        self.maze[row + 1][col].close_wall(Direction.north)
                        self.maze[row][col].close_wall(dir)

                    if (dir == Direction.west and
                            self.maze[row][col - 1].total_closed() <= 1):
                        self.maze[row][col - 1].close_wall(Direction.east)
                        self.maze[row][col].close_wall(dir)

                elif col == 0:
                    dir = random.choice(directions)
                    while dir == Direction.west:
                        dir = random.choice(directions)

                    if (dir == Direction.north and row > 0 and
                            self.maze[row - 1][col].total_closed() <= 1):
                        self.maze[row - 1][col].close_wall(Direction.south)
                        self.maze[row][col].close_wall(dir)

                    if (dir == Direction.south and
                            row < self.height - 1 and
                            self.maze[row + 1][col].total_closed() <= 1):
                        self.maze[row + 1][col].close_wall(Direction.north)
                        self.maze[row][col].close_wall(dir)

                    if (dir == Direction.east and
                            self.maze[row][col + 1].total_closed() <= 1):
                        self.maze[row][col + 1].close_wall(Direction.west)
                        self.maze[row][col].close_wall(dir)

                if self.maze[row][col].walls == 0:
                    if self.valid_helper(row, col):
                        dir_1 = random.choice(directions)
                        dir_2 = random.choice(directions)
                        while dir_1 == dir_2:
                            dir_2 = random.choice(directions)
                        self.maze[row][col].close_wall(dir_1)
                        self.maze[row][col].close_wall(dir_2)
                        match dir_1:
                            case Direction.north:
                                self.maze[row - 1][col].close_wall(
                                    Direction.south
                                    )
                            case Direction.south:
                                self.maze[row + 1][col].close_wall(
                                    Direction.north
                                    )
                            case Direction.east:
                                self.maze[row][col + 1].close_wall(
                                    Direction.west
                                    )
                            case Direction.west:
                                self.maze[row][col - 1].close_wall(
                                    Direction.east
                                    )
                        match dir_2:
                            case Direction.north:
                                self.maze[row - 1][col].close_wall(
                                    Direction.south
                                    )
                            case Direction.south:
                                self.maze[row + 1][col].close_wall(
                                    Direction.north
                                    )
                            case Direction.east:
                                self.maze[row][col + 1].close_wall(
                                    Direction.west
                                    )
                            case Direction.west:
                                self.maze[row][col - 1].close_wall(
                                    Direction.east
                                    )

            if self.animation:
                self.print_maze()

    def make_it_empty(self) -> None:
        """Open all walls of the maze except boundaries and '42' walls."""
        directions = [
            Direction.north,
            Direction.east,
            Direction.south,
            Direction.west
            ]

        for row in self.maze:
            for cell in row:
                for direction in directions:
                    cell.open_wall(direction)

        for r in range(len(self.maze)):
            for c in range(len(self.maze[r])):

                if r == 0:
                    self.maze[r][c].close_wall(Direction.north)

                if r == self.height - 1:
                    self.maze[r][c].close_wall(Direction.south)

                if c == 0:
                    self.maze[r][c].close_wall(Direction.west)

                if c == self.width - 1:
                    self.maze[r][c].close_wall(Direction.east)

                if self.maze[r][c].visited == 42:
                    for dir in directions:
                        self.maze[r][c].close_wall(dir)
                        match dir:
                            case Direction.north:
                                self.maze[r - 1][c].close_wall(Direction.south)
                            case Direction.south:
                                self.maze[r + 1][c].close_wall(Direction.north)
                            case Direction.east:
                                self.maze[r][c + 1].close_wall(Direction.west)
                            case Direction.west:
                                self.maze[r][c - 1].close_wall(Direction.east)

        if self.animation:
            self.print_maze()

    def make_it_wrong(self) -> None:
        """Open a certain number of walls of a perfect maze."""
        directions = [
            Direction.north,
            Direction.east,
            Direction.south,
            Direction.west
            ]

        open_walls = 0
        for row in self.maze:
            for cell in row:
                for direction in directions:
                    open_walls += cell.is_open(direction)

        i = 0
        while i < round(open_walls / 42):

            r = random.randint(0, self.height - 1)
            c = random.randint(0, self.width - 1)
            dir = random.choice(directions)

            match dir:
                case Direction.north:
                    if (r > 0 and
                            self.maze[r][c].visited != 42 and
                            self.maze[r - 1][c].visited != 42 and
                            self.maze[r][c].is_closed(dir)):

                        self.maze[r][c].open_wall(dir)
                        self.maze[r - 1][c].open_wall(Direction.south)
                        i += 1

                case Direction.south:
                    if (r < self.height - 1 and
                            self.maze[r][c].visited != 42 and
                            self.maze[r + 1][c].visited != 42 and
                            self.maze[r][c].is_closed(dir)):

                        self.maze[r][c].open_wall(dir)
                        self.maze[r + 1][c].open_wall(Direction.north)
                        i += 1

                case Direction.east:
                    if (c < self.width - 1 and
                            self.maze[r][c].visited != 42 and
                            self.maze[r][c + 1].visited != 42 and
                            self.maze[r][c].is_closed(dir)):

                        self.maze[r][c].open_wall(dir)
                        self.maze[r][c + 1].open_wall(Direction.west)
                        i += 1

                case Direction.west:
                    if (c > 0 and
                            self.maze[r][c].visited != 42 and
                            self.maze[r][c - 1].visited != 42 and
                            self.maze[r][c].is_closed(dir)):

                        self.maze[r][c].open_wall(dir)
                        self.maze[r][c - 1].open_wall(Direction.east)
                        i += 1
            if self.animation:
                self.print_maze()
        self.make_it_valid()

    def valid_helper(self, row: int, col: int) -> bool:
        """Check if all four walls of a cell are open.

        Args:
            row: x-axis of the cell.
            col: y-axis of the cell.
        Returns:
            True if all walls are open,
            False otherwise.
        """
        cell_n = self.maze[row - 1][col]
        cell_s = self.maze[row + 1][col]
        cell_e = self.maze[row][col + 1]
        cell_w = self.maze[row][col - 1]

        walls_n = (cell_n.is_open(Direction.east) and
                   cell_n.is_open(Direction.west))
        walls_s = (cell_s.is_open(Direction.east) and
                   cell_s.is_open(Direction.west))
        walls_e = (cell_e.is_open(Direction.north) and
                   cell_e.is_open(Direction.south))
        walls_w = (cell_w.is_open(Direction.north) and
                   cell_w.is_open(Direction.south))

        return all([walls_n, walls_s, walls_e, walls_w])

    def make_it_valid(self) -> None:
        """Close walls if needed for validation."""
        directions = [
            Direction.north,
            Direction.east,
            Direction.south,
            Direction.west
            ]

        for row in range(1, self.height - 1):
            for col in range(1, self.width - 1):
                if self.maze[row][col].walls == 0:
                    if self.valid_helper(row, col):
                        dir_1 = random.choice(directions)
                        dir_2 = random.choice(directions)
                        while dir_1 == dir_2:
                            dir_2 = random.choice(directions)
                        self.maze[row][col].close_wall(dir_1)
                        self.maze[row][col].close_wall(dir_2)
                        match dir_1:
                            case Direction.north:
                                self.maze[row - 1][col].close_wall(
                                    Direction.south
                                    )
                            case Direction.south:
                                self.maze[row + 1][col].close_wall(
                                    Direction.north
                                    )
                            case Direction.east:
                                self.maze[row][col + 1].close_wall(
                                    Direction.west
                                    )
                            case Direction.west:
                                self.maze[row][col - 1].close_wall(
                                    Direction.east
                                    )
                        match dir_2:
                            case Direction.north:
                                self.maze[row - 1][col].close_wall(
                                    Direction.south
                                    )
                            case Direction.south:
                                self.maze[row + 1][col].close_wall(
                                    Direction.north
                                    )
                            case Direction.east:
                                self.maze[row][col + 1].close_wall(
                                    Direction.west
                                    )
                            case Direction.west:
                                self.maze[row][col - 1].close_wall(
                                    Direction.east
                                    )

                if self.animation:
                    self.print_maze()

    def backtrack_solver(self, col: int, row: int, path: str) -> None:
        """Backtrack algorithm for maze resolution.

        Args:
            col: y-axis of the first cell.
            row: x-axis of the first cell.
            path: a string with cardinal instructions (N,E,S,W) representing
                  the solution path.
        """
        self.maze[row][col].visited = 1
        if self.maze[row][col].is_exit:
            self.path = path
            return

        directions = [
            Direction.north,
            Direction.east,
            Direction.south,
            Direction.west
            ]

        random.shuffle(directions)
        for direction in directions:
            if self.path:
                break
            match direction:

                case Direction.north:
                    if (row > 0 and not
                            self.maze[row - 1][col].visited and not
                            self.maze[row][col].is_closed(Direction.north)):

                        self.backtrack_solver(row=(row - 1),
                                              col=col,
                                              path=path + 'N')

                case Direction.south:
                    if (row < self.height - 1 and not
                            self.maze[row + 1][col].visited and not
                            self.maze[row][col].is_closed(Direction.south)):

                        self.backtrack_solver(row=(row + 1),
                                              col=col,
                                              path=path + 'S')

                case Direction.east:
                    if (col < self.width - 1 and not
                            self.maze[row][col + 1].visited and not
                            self.maze[row][col].is_closed(Direction.east)):

                        self.backtrack_solver(row=row,
                                              col=(col + 1),
                                              path=path + 'E')

                case Direction.west:
                    if (col > 0 and not
                            self.maze[row][col - 1].visited and not
                            self.maze[row][col].is_closed(Direction.west)):

                        self.backtrack_solver(row=row,
                                              col=(col - 1),
                                              path=path + 'W')

        self.maze[row][col].visited = 0

    def breadth_first_search_solver(self) -> None:
        """Breadth-First Search algorithm for maze resolution."""
        c: int = 0
        r: int = 0
        if len(self.entry) == 2:
            c, r = self.entry
        queue: deque[tuple[int, int]] = deque([(r, c)])
        self.maze[r][c].visited = 1
        self.maze[r][c].steps = 0

        while queue:

            r, c = queue.popleft()
            if (c, r) == self.exit:
                break

            if (r > 0 and
                    self.maze[r][c].is_open(Direction.north) and not
                    self.maze[r - 1][c].visited):
                queue.append((r - 1, c))
                self.maze[r - 1][c].visited = 1
                self.maze[r - 1][c].steps = self.maze[r][c].steps + 1

            if (r < self.height - 1 and
                    self.maze[r][c].is_open(Direction.south) and not
                    self.maze[r + 1][c].visited):
                queue.append((r + 1, c))
                self.maze[r + 1][c].visited = 1
                self.maze[r + 1][c].steps = self.maze[r][c].steps + 1

            if (c < self.width - 1 and
                    self.maze[r][c].is_open(Direction.east) and not
                    self.maze[r][c + 1].visited):
                queue.append((r, c + 1))
                self.maze[r][c + 1].visited = 1
                self.maze[r][c + 1].steps = self.maze[r][c].steps + 1

            if (c > 0 and
                    self.maze[r][c].is_open(Direction.west) and not
                    self.maze[r][c - 1].visited):
                queue.append((r, c - 1))
                self.maze[r][c - 1].visited = 1
                self.maze[r][c - 1].steps = self.maze[r][c].steps + 1

        htap: str = ""
        while (c, r) != self.entry:

            if (r > 0 and
                    self.maze[r][c].is_open(Direction.north) and
                    self.maze[r - 1][c].steps == self.maze[r][c].steps - 1):
                htap += 'S'
                r = r - 1

            elif (r < self.height - 1 and
                  self.maze[r][c].is_open(Direction.south) and
                  self.maze[r + 1][c].steps == self.maze[r][c].steps - 1):
                htap += 'N'
                r = r + 1

            elif (c < self.width - 1 and
                  self.maze[r][c].is_open(Direction.east) and
                  self.maze[r][c + 1].steps == self.maze[r][c].steps - 1):
                htap += 'W'
                c = c + 1

            elif (c > 0 and
                  self.maze[r][c].is_open(Direction.west) and
                  self.maze[r][c - 1].steps == self.maze[r][c].steps - 1):
                htap += 'E'
                c = c - 1

        self.path = htap[::-1]

    def assign_solution(self) -> None:
        """Assign to cells the is_solved attribute."""
        row: int = 0
        col: int = 0
        if len(self.entry) == 2:
            col, row = self.entry[0], self.entry[1]
        self.maze[row][col].is_solved = True
        path = self.path

        for char in path:
            if self.animation:
                self.print_maze()
            match char:

                case 'N':
                    row = row - 1

                case 'S':
                    row = row + 1

                case 'E':
                    col = col + 1

                case 'W':
                    col = col - 1

            self.maze[row][col].is_solved = True

    def hide_corner(self, r: int, c: int) -> int:
        """Check if all the walls in between diagonal walls are open.

        Args:
            r: x-index of the cell.
            c: y-index of the cell.
        Returns:
            1 (truthy) if all walls are open.
            0 (falsy) otherwise.
        """
        if r >= len(self.maze) - 1 or c >= len(self.maze[0]) - 1:
            return 0
        se: int = (self.maze[r][c].is_open(Direction.south) and
                   self.maze[r][c].is_open(Direction.east))
        nw: int = (self.maze[r + 1][c + 1].is_open(Direction.north) and
                   self.maze[r + 1][c + 1].is_open(Direction.west))
        return se and nw

    def print_maze(self) -> None:
        """Print strings on terminal representig the state of the maze."""
        if not self or not self.maze:
            return

        # maze_str = ""
        clear_screen()
        print(self.theme['wall'] * (len(self.maze[0]) * 2 + 1))
        # maze_str += self.theme['wall'] * (len(self.maze[0]) * 2 + 1) + "\n"

        for row in range(len(self.maze)):
            line_str = self.theme['wall']

            for col in range(len(self.maze[row])):

                if self.maze[row][col].is_entry:
                    line_str += self.theme['entry']

                elif self.maze[row][col].is_exit:
                    line_str += self.theme['exit']

                elif self.maze[row][col].is_solved:
                    if self.solution:
                        line_str += self.theme['solved']
                    else:
                        line_str += self.theme['path']

                elif self.maze[row][col].visited == 42:
                    line_str += self.theme['ft']

                else:
                    line_str += self.theme['path']

                if (col < self.width - 1 and
                    (self.maze[row][col].visited == 42 and
                     self.maze[row][col + 1].visited == 42)):
                    line_str += self.theme['ft_wall']

                elif self.maze[row][col].is_closed(Direction.east):
                    line_str += self.theme['wall']

                elif ((self.maze[row][col].is_entry or
                      self.maze[row][col].is_solved) and
                      self.maze[row][col + 1].is_solved):
                    if self.solution:
                        line_str += self.theme['solved']
                    else:
                        line_str += self.theme['path']

                else:
                    line_str += self.theme['path']

            print(line_str)
            # maze_str += line_str + "\n"

            bottom_str = self.theme['wall']

            for col in range(len(self.maze[row])):
                if (row < self.height - 1 and
                    (self.maze[row][col].visited == 42 and
                     self.maze[row + 1][col].visited == 42)):
                    bottom_str += self.theme['ft_wall']

                elif self.maze[row][col].is_closed(Direction.south):
                    bottom_str += self.theme['wall']

                elif ((self.maze[row][col].is_entry or
                      self.maze[row][col].is_solved) and
                      self.maze[row + 1][col].is_solved):
                    if self.solution:
                        bottom_str += self.theme['solved']
                    else:
                        bottom_str += self.theme['path']

                else:
                    bottom_str += self.theme['path']

                if (self.hide_corner(row, col)):
                    bottom_str += self.theme['path']
                else:
                    bottom_str += self.theme['wall']
            print(bottom_str)
            # maze_str += bottom_str + "\n"
        # print(maze_str)
        time.sleep(0.042)

    def __str__(self) -> str:
        """Readable representation of the maze.

        Returns:
            result: a string containing a visual representation of the maze.
        """
        result = ""

        for row in self.maze:
            result += ("".join(str(cell) for cell in row)) + "\n"

        return result

    def __repr__(self) -> str:
        """Readable representation of the maze, usable to print a list.

        Returns:
            result: a string containing a visual representation of the maze.
        """
        return '\n'.join(str(row) for row in self.maze)

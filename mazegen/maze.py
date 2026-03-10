"""Module for manage the Maze and relative methods."""

from mazegen.requirement_parser import MazeConfig
from mazegen.cell import Cell, Direction
from mazegen.themes import THEMES
from collections import deque
from typing import Optional
import platform
import random
import time


def clear_screen() -> None:
    """Clear the shell window."""
    if platform.system() == "Windows":
        print("\033[2J\033[H")
        print("\033[3J\033[H")
    else:
        print("\033[2J\033[H")
        print("\033[3J\033[H")


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
        self.sleep_time = 0.042
        self.maze = self.init_maze()

    @staticmethod
    def get_random_seed() -> str:
        """Generate a random seed.

        Returns:
            seed: the seed generated.
        """
        alpha: str = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"
        digit: str = "0123456789"
        symbol: str = "?!@#$%^&*()_-+{}[]:;|/<>,.\\"
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
                self.error_message = str("[SORRY]: "
                                         "maze too small to contain '42'")
            else:
                self.error_message = ""
                self.forty_two()

                if self.maze[self.entry[1]][self.entry[0]].visited == 42:
                    raise ValueError("[ERROR]: "
                                     "ENTRY inside the 42!\n")

                if self.maze[self.exit[1]][self.exit[0]].visited == 42:
                    raise ValueError("[ERROR]: "
                                     "EXIT inside the 42!\n")

                if self.maze[self.start[1]][self.start[0]].visited == 42:
                    raise ValueError("[ERROR]: "
                                     "STARTING POINT inside the 42!\n")

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

            case "eller":
                self.eller()

            case "kruskal":
                self.kruskal()

            case "aldous_broder":
                self.aldous_broder(self.start[1], self.start[0])

            case "wilson":
                self.wilson()

            case "recursive_division":
                self.make_it_empty()
                if self.two_forty and not self.error_message:
                    self.ft_recursive_division()
                else:
                    if self.width > self.height:
                        axis = 1
                    elif self.width < self.height:
                        axis = 0
                    else:
                        axis = random.randint(0, 1)
                    self.recursive_division(x=0,
                                            y=0,
                                            width=self.width,
                                            height=self.height,
                                            axis=axis)

            case "hunt_and_kill":
                self.hunt_and_kill()

            case "sidewinder":
                self.sidewinder()

            case "binary_tree":
                self.binary_tree()

            case "nirugger":
                if not self.perfect:
                    self.perfect = True
                    self.nirugger()
                    self.perfect = False
                else:
                    self.nirugger()

    def backtrack(self, col: int, row: int) -> None:
        """Backtrack algorithm for maze generation.

        Args:
            col: y-axis of the first cell.
            row: x-axis of the first cell.
        """
        directions = [
            Direction.north,
            Direction.east,
            Direction.south,
            Direction.west
            ]

        if (self.animation):
            self.print_maze()

        i = 0
        random.shuffle(directions)
        self.maze[row][col].visited = 1
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
        directions = [
            Direction.north,
            Direction.east,
            Direction.south,
            Direction.west
            ]

        if (self.animation):
            self.print_maze()

        random.shuffle(directions)
        self.maze[row][col].visited = 1
        for direction in directions:
            match direction:

                case Direction.north:
                    if (row > 0
                            and not self.maze[row - 1][col].visited):

                        self.maze[row][col].open_wall(Direction.north)
                        self.maze[row - 1][col].open_wall(Direction.south)
                        frontier.append((col, row - 1))

                        self.maze[row - 1][col].visited = 1

                        item = random.choice(frontier)
                        self.prim(row=item[1],
                                  col=item[0],
                                  frontier=frontier)

                case Direction.south:
                    if (row < self.height - 1
                            and not self.maze[row + 1][col].visited):

                        self.maze[row][col].open_wall(Direction.south)
                        self.maze[row + 1][col].open_wall(Direction.north)
                        frontier.append((col, row + 1))
                        self.maze[row + 1][col].visited = 1

                        item = random.choice(frontier)

                        self.prim(row=item[1],
                                  col=item[0],
                                  frontier=frontier)

                case Direction.east:
                    if (col < self.width - 1
                            and not self.maze[row][col + 1].visited):

                        self.maze[row][col].open_wall(Direction.east)
                        self.maze[row][col + 1].open_wall(Direction.west)
                        self.maze[row][col + 1].visited = 1

                        frontier.append((col + 1, row))
                        item = random.choice(frontier)

                        self.prim(row=item[1],
                                  col=item[0],
                                  frontier=frontier)

                case Direction.west:
                    if (col > 0
                            and not self.maze[row][col - 1].visited):

                        self.maze[row][col].open_wall(Direction.west)
                        self.maze[row][col - 1].open_wall(Direction.east)
                        frontier.append((col - 1, row))
                        self.maze[row][col - 1].visited = 1

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

    def eller_stage_one(self,
                        row: int,
                        unique_sets: int) -> int:

        for col in range(self.width):
            if col == self.width - 1:
                continue

            coin = random.randint(0, 1)
            if (self.maze[row + 1][col + 1].visited == 42 and
                    self.maze[row - 1][col + 1].visited == 42 and
                    self.maze[row + 1][col - 1].visited == 42 and
                    self.maze[row - 1][col - 1].visited != 42):

                self.maze[row][col].open_wall(Direction.east)
                self.maze[row][col + 1].open_wall(Direction.west)
                new_id = self.maze[row][col].id
                old_id = self.maze[row][col + 1].id
                self.maze[row][col + 1].open_wall(Direction.east)
                self.maze[row][col + 2].open_wall(Direction.west)
                new_id = self.maze[row][col + 1].id
                old_id = self.maze[row][col + 2].id

                for c in range(self.width):
                    if self.maze[row][c].id == old_id:
                        self.maze[row][c].id = new_id
                unique_sets -= 1

            elif (coin
                    and self.maze[row][col].id != self.maze[row][col + 1].id
                    and self.maze[row][col].visited != 42
                    and self.maze[row][col + 1].visited != 42):

                self.maze[row][col].open_wall(Direction.east)
                self.maze[row][col + 1].open_wall(Direction.west)
                old_id = self.maze[row][col + 1].id
                new_id = self.maze[row][col].id

                for c in range(self.width):
                    if self.maze[row][c].id == old_id:
                        self.maze[row][c].id = new_id
                unique_sets -= 1

            if self.animation:
                self.print_maze()

        return unique_sets

    def eller_stage_two(self,
                        row: int,
                        unique_sets: int,
                        el_set: set[tuple[int, int]]) -> int:

        preset_id = set(self.maze[row][col].id
                        for col in range(self.width))

        for id in preset_id:
            coords = []

            for col in range(self.width):
                if (self.maze[row][col].id == id
                        and self.maze[row][col].visited != 42):
                    coords.append((row, col))

            if len(coords) == 1:
                r, c = coords[0][0], coords[0][1]

                if self.maze[r + 1][c].visited != 42:
                    self.maze[r][c].open_wall(Direction.south)
                    self.maze[r + 1][c].open_wall(Direction.north)
                    self.maze[r + 1][c].id = self.maze[r][c].id
                    el_set.add((r + 1, c))

                else:
                    i = c
                    while self.maze[r + 1][i].visited == 42:

                        if (self.maze[r][i].id != self.maze[r][i + 1].id
                                and self.maze[r][i].visited != 42
                                and self.maze[r][i + 1].visited != 42):

                            self.maze[r][i].open_wall(Direction.east)
                            self.maze[r][i + 1].open_wall(Direction.west)
                            new_id = self.maze[r][i + 1].id
                            old_id = self.maze[r][i].id

                            for j in range(self.width):
                                if self.maze[r][j].id == old_id:
                                    self.maze[r][j].id = new_id
                            unique_sets -= 1
                        i += 1

                    if (self.maze[r][i].id != self.maze[r + 1][i].id
                            and self.maze[r][i].visited != 42):

                        self.maze[r][i].open_wall(Direction.south)
                        self.maze[r + 1][i].open_wall(Direction.north)
                        self.maze[r + 1][i].id = self.maze[r][i].id
                        el_set.add((r + 1, i))

            else:
                if not coords:
                    continue

                choices = random.randint(0, len(coords))
                if not choices:
                    choices = 1

                for _ in range(choices):
                    choosen = random.choice(coords)
                    r, c = choosen[0], choosen[1]
                    if (self.maze[r][c].id != self.maze[r + 1][c].id
                            and self.maze[r + 1][c].visited != 42):

                        self.maze[r][c].open_wall(Direction.south)
                        self.maze[r + 1][c].open_wall(Direction.north)
                        self.maze[r + 1][c].id = self.maze[r][c].id
                        el_set.add((r + 1, c))

                    else:
                        i = c
                        while self.maze[r + 1][i].visited == 42:
                            if (self.maze[r][i].id
                                    != self.maze[r][i + 1].id
                                    and self.maze[r][i].visited != 42
                                    and self.maze[r][i + 1].visited != 42):

                                self.maze[r][i].open_wall(Direction.east)
                                self.maze[r][i + 1].open_wall(Direction.west)
                                old_id = self.maze[r][i + 1].id
                                new_id = self.maze[r][i].id

                                for j in range(self.width):
                                    if self.maze[r][j].id == old_id:
                                        self.maze[r][j].id = new_id
                                unique_sets -= 1

                                if (r, i + 1) in coords:
                                    coords.remove((r, i + 1))
                            i += 1

                        if (self.maze[r][i].id != self.maze[r + 1][i].id
                                and self.maze[r][i].visited != 42):

                            self.maze[r][i].open_wall(Direction.south)
                            self.maze[r + 1][i].open_wall(Direction.north)
                            self.maze[r + 1][i].id = self.maze[r][i].id
                            el_set.add((r + 1, i))
                    coords.remove(choosen)

            if self.animation:
                self.print_maze()

        return unique_sets

    def eller_stage_three(self,
                          row: int,
                          unique_sets: int,
                          el_set: set[tuple[int, int]]) -> int:

        preset_id = set(self.maze[row][col].id
                        for col in range(self.width))

        next_id = max(preset_id) + 1
        for col in range(self.width):
            if ((row + 1, col) not in el_set
                    and self.maze[row + 1][col].visited != 42):
                el_set.add((row + 1, col))
                self.maze[row + 1][col].id = next_id
                unique_sets += 1
                next_id += 1

        return unique_sets

    def eller(self) -> None:

        el_set: set[tuple[int, int]] = set()
        unique_sets = 0

        for cell in self.maze[0]:
            el_set.add((0, unique_sets))
            unique_sets += 1
            cell.id = unique_sets

        for row in range(self.height - 1):

            unique_sets = self.eller_stage_one(row, unique_sets)
            unique_sets = self.eller_stage_two(row, unique_sets, el_set)
            unique_sets = self.eller_stage_three(row, unique_sets, el_set)

        row = self.height - 1
        for col in range(self.width):
            if col == self.width - 1:
                continue

            if self.maze[row][col].id != self.maze[row][col + 1].id:
                self.maze[row][col].open_wall(Direction.east)
                self.maze[row][col + 1].open_wall(Direction.west)
                old_id = self.maze[row][col + 1].id
                new_id = self.maze[row][col].id

                for c in range(self.width):
                    if self.maze[row][c].id == old_id:
                        self.maze[row][c].id = new_id
                unique_sets -= 1

            if self.animation:
                self.print_maze()

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

            random.shuffle(directions)
            this_set = random.choice(krusk_list)
            row, col = random.choice(tuple(this_set))

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

    def aldous_broder(self, col: int, row: int) -> None:
        """Aldous-Broder algorithm for maze generation."""
        directions = [
            Direction.north,
            Direction.east,
            Direction.south,
            Direction.west
            ]

        counter = 0
        total_cells = 0

        for r in self.maze:
            for cell in r:
                if cell.visited != 42:
                    total_cells += 1

        while counter < total_cells:
            if self.maze[row][col].visited == 0:
                self.maze[row][col].visited = 1
                counter += 1
            self.maze[row][col].target = True

            if self.animation:
                self.print_maze()

            choice = random.choice(directions)
            match choice:
                case Direction.north:
                    if (row == 0
                            or self.maze[row - 1][col].visited == 42):
                        continue

                    if not self.maze[row - 1][col].visited:
                        self.maze[row][col].open_wall(Direction.north)
                        self.maze[row - 1][col].open_wall(Direction.south)

                    self.maze[row][col].target = False
                    row = row - 1

                case Direction.south:
                    if (row == self.height - 1
                            or self.maze[row + 1][col].visited == 42):
                        continue

                    if not self.maze[row + 1][col].visited:
                        self.maze[row][col].open_wall(Direction.south)
                        self.maze[row + 1][col].open_wall(Direction.north)

                    self.maze[row][col].target = False
                    row = row + 1

                case Direction.east:
                    if (col == self.width - 1
                            or self.maze[row][col + 1].visited == 42):
                        continue

                    if not self.maze[row][col + 1].visited:
                        self.maze[row][col].open_wall(Direction.east)
                        self.maze[row][col + 1].open_wall(Direction.west)

                    self.maze[row][col].target = False
                    col = col + 1

                case Direction.west:
                    if (col == 0
                            or self.maze[row][col - 1].visited == 42):
                        continue

                    if not self.maze[row][col - 1].visited:
                        self.maze[row][col].open_wall(Direction.west)
                        self.maze[row][col - 1].open_wall(Direction.east)

                    self.maze[row][col].target = False
                    col = col - 1

    def wilson_opener(self, r: int, c: int, dir: Direction, steps: int) -> int:
        """Match direction and open walls.

        Args:
            r: row of the maze.
            c: column of the maze.
            dir: direction chosen.
        Returns:
            int: 1 (truthy) if the wall are opened.
                 0 (falsy) otherwise.
        """

        match dir:

            case Direction.north:
                if r > 0 and self.maze[r - 1][c].visited != 42:
                    if not self.maze[r - 1][c].steps:
                        self.maze[r][c].open_wall(Direction.north)
                        self.maze[r - 1][c].open_wall(Direction.south)
                    self.maze[r][c].steps = steps
                    return 1

            case Direction.south:
                if r < self.height - 1 and self.maze[r + 1][c].visited != 42:
                    if not self.maze[r + 1][c].steps:
                        self.maze[r][c].open_wall(Direction.south)
                        self.maze[r + 1][c].open_wall(Direction.north)
                    self.maze[r][c].steps = steps
                    return 1

            case Direction.east:
                if c < self.width - 1 and self.maze[r][c + 1].visited != 42:
                    if not self.maze[r][c + 1].steps:
                        self.maze[r][c].open_wall(Direction.east)
                        self.maze[r][c + 1].open_wall(Direction.west)
                    self.maze[r][c].steps = steps
                    return 1

            case Direction.west:
                if c > 0 and self.maze[r][c - 1].visited != 42:
                    if not self.maze[r][c - 1].steps:
                        self.maze[r][c].open_wall(Direction.west)
                        self.maze[r][c - 1].open_wall(Direction.east)
                    self.maze[r][c].steps = steps
                    return 1
        return 0

    def wilson_killer(self, r: int, c: int) -> None:

        while True:

            if (r > 0 and
                    self.maze[r][c].is_open(Direction.north) and
                    self.maze[r - 1][c].steps == self.maze[r][c].steps + 1):
                self.maze[r][c].close_wall(Direction.north)
                self.maze[r - 1][c].close_wall(Direction.south)
                self.maze[r][c].steps = 0
                r = r - 1
                continue

            elif (r < self.height - 1 and
                  self.maze[r][c].is_open(Direction.south) and
                  self.maze[r + 1][c].steps == self.maze[r][c].steps + 1):
                self.maze[r][c].close_wall(Direction.south)
                self.maze[r + 1][c].close_wall(Direction.north)
                self.maze[r][c].steps = 0
                r = r + 1
                continue

            elif (c < self.width - 1 and
                  self.maze[r][c].is_open(Direction.east) and
                  self.maze[r][c + 1].steps == self.maze[r][c].steps + 1):
                self.maze[r][c].close_wall(Direction.east)
                self.maze[r][c + 1].close_wall(Direction.west)
                self.maze[r][c].steps = 0
                c = c + 1
                continue

            elif (c > 0 and
                  self.maze[r][c].is_open(Direction.west) and
                  self.maze[r][c - 1].steps == self.maze[r][c].steps + 1):
                self.maze[r][c].close_wall(Direction.west)
                self.maze[r][c - 1].close_wall(Direction.east)
                self.maze[r][c].steps = 0
                c = c - 1
                continue
            break
        if self.animation:
            self.print_maze()
        self.maze[r][c].steps = 0

    def wilson_validator(self,
                         start: tuple[int, int],
                         end: list[tuple[int, int]],
                         pool: list[tuple[int, int]]) -> None:

        r, c = start[0], start[1]
        while True:
            if (r > 0 and
                    self.maze[r][c].is_open(Direction.north) and
                    self.maze[r - 1][c].steps == self.maze[r][c].steps + 1):
                self.maze[r][c].steps = 0
                self.maze[r][c].visited = 1
                end.append((r, c))
                pool.remove((r, c))
                r = r - 1
                continue

            elif (r < self.height - 1 and
                  self.maze[r][c].is_open(Direction.south) and
                  self.maze[r + 1][c].steps == self.maze[r][c].steps + 1):
                self.maze[r][c].steps = 0
                self.maze[r][c].visited = 1
                end.append((r, c))
                pool.remove((r, c))
                r = r + 1
                continue

            elif (c < self.width - 1 and
                  self.maze[r][c].is_open(Direction.east) and
                  self.maze[r][c + 1].steps == self.maze[r][c].steps + 1):
                self.maze[r][c].steps = 0
                self.maze[r][c].visited = 1
                end.append((r, c))
                pool.remove((r, c))
                c = c + 1
                continue

            elif (c > 0 and
                  self.maze[r][c].is_open(Direction.west) and
                  self.maze[r][c - 1].steps == self.maze[r][c].steps + 1):
                self.maze[r][c].steps = 0
                self.maze[r][c].visited = 1
                end.append((r, c))
                pool.remove((r, c))
                c = c - 1
                continue
            break
        self.maze[r][c].steps = 0
        self.maze[r][c].visited = 1
        end.append((r, c))
        pool.remove((r, c))

    def wilson(self) -> None:
        """Wilson algorithm for maze generation."""
        directions = [
            Direction.north,
            Direction.east,
            Direction.south,
            Direction.west
            ]

        pool: list[tuple[int, int]] = []
        for row in range(self.height):
            for col in range(self.width):
                if not self.maze[row][col].visited:
                    pool.append((row, col))

        end: list[tuple[int, int]] = []
        end.append(random.choice(pool))
        self.maze[end[0][0]][end[0][1]].is_player = True
        pool.remove(end[0])

        while len(pool):
            start = random.choice(pool)
            r, c = start[0], start[1]
            steps = 1
            while not (r, c) in end:
                if self.maze[r][c].steps:
                    steps = self.maze[r][c].steps
                    self.wilson_killer(r, c)
                    self.maze[r][c].steps = steps
                random.shuffle(directions)
                for direction in directions:
                    match direction:

                        case Direction.north:
                            if self.wilson_opener(r, c, direction, steps):
                                steps += 1
                                r = r - 1
                                break

                        case Direction.south:
                            if self.wilson_opener(r, c, direction, steps):
                                steps += 1
                                r = r + 1
                                break

                        case Direction.east:
                            if self.wilson_opener(r, c, direction, steps):
                                steps += 1
                                c = c + 1
                                break

                        case Direction.west:
                            if self.wilson_opener(r, c, direction, steps):
                                steps += 1
                                c = c - 1
                                break
                if self.animation:
                    self.print_maze()
            self.wilson_validator(start, end, pool)
            self.maze[end[0][0]][end[0][1]].is_player = False

    def ft_recursive_division(self) -> None:
        """Recurisive division argorithm with '42' at the center."""
        center_x = int((self.width - 1) / 2)
        center_y = int((self.height - 1) / 2)
        offset_x = self.width % 2
        offset_y = self.height % 2
        axis = random.randint(0, 1)
        col = center_x - 4
        open = random.randint(0, center_y - 3)
        for row in range(center_y - 2):
            if row == open:
                continue
            self.maze[row][col].close_wall(Direction.east)
            self.maze[row][col + 1].close_wall(Direction.west)
        self.recursive_division(x=0,
                                y=0,
                                width=center_x - 3,
                                height=center_y + 3,
                                axis=axis)

        axis = not axis
        row = center_y - 3
        open = random.randint(center_x + 4, self.width - 1)
        for col in range(center_x + 4, self.width):
            if col == open:
                continue
            self.maze[row][col].close_wall(Direction.south)
            self.maze[row + 1][col].close_wall(Direction.north)
        self.recursive_division(x=center_x - 3,
                                y=0,
                                width=center_x + 5 - offset_x,
                                height=center_y - 2,
                                axis=axis)

        axis = not axis
        col = center_x + 4
        open = random.randint(center_y + 2, self.height - 1)
        for row in range(center_y + 2, self.height):
            if row == open:
                continue
            self.maze[row][col].close_wall(Direction.west)
            self.maze[row][col - 1].close_wall(Direction.east)
        self.recursive_division(x=center_x + 4,
                                y=center_y - 2,
                                width=center_x - 2 - offset_x,
                                height=center_y + 4 - offset_y,
                                axis=axis)

        axis = not axis
        row = center_y + 3
        open = random.randint(0, center_x - 2)
        for col in range(0, center_x - 1):
            if col == open:
                continue
            self.maze[row][col].close_wall(Direction.north)
            self.maze[row - 1][col].close_wall(Direction.south)
        self.recursive_division(x=0,
                                y=center_y + 3,
                                width=center_x + 4,
                                height=center_y - 1 - offset_y,
                                axis=axis)

        axis = not axis
        row = center_y - 3
        open = random.randint(center_x - 2, center_x)
        for col in range(center_x - 2, center_x + 1):
            if col == open:
                continue
            self.maze[row][col].close_wall(Direction.south)
            self.maze[row + 1][col].close_wall(Direction.north)
        self.recursive_division(x=center_x - 2,
                                y=center_y - 2,
                                width=3,
                                height=2,
                                axis=axis)

        open = random.randint(center_x - 3, center_x - 2)
        row = center_y + 2
        for col in range(center_x - 3, center_x - 1):
            if col == open:
                continue
            self.maze[row][col].close_wall(Direction.south)
            self.maze[row + 1][col].close_wall(Direction.north)

        open = random.randint(center_y + 1, center_y + 2)
        col = center_x - 4
        for row in range(center_y + 1, center_y + 3):
            if row == open:
                continue
            self.maze[row][col].close_wall(Direction.east)
            self.maze[row][col + 1].close_wall(Direction.west)

        axis = not axis
        self.recursive_division(x=center_x - 3,
                                y=center_y + 1,
                                width=2,
                                height=2,
                                axis=axis)

    def recursive_division(self,
                           x: int,
                           y: int,
                           width: int,
                           height: int,
                           axis: int) -> None:
        """Recursive division algorithm for maze generation.

        Args:
            x: x coord of the sub-maze.
            y: y coord of the sub-maze.
            width: width of the sub-maze.
            height: height of the sub-maze.
            axis: 0 or 1, deciding wich axes is divided.
        """
        axis = not axis
        if width < 2 or height < 2:
            return
        if axis:
            if height == 2:
                row = y + 1
            else:
                row = random.randrange(y + 1, y + height)
                while self.maze[row][x].visited == 42:
                    row = random.randrange(y + 1, y + height)

            open = random.randint(x, x + width - 1)
            while self.maze[row][open].visited == 42:
                open = random.randint(x, x + width - 1)

            for col in range(x, x + width):
                if col == open:
                    continue
                self.maze[row][col].close_wall(Direction.north)
                self.maze[row - 1][col].close_wall(Direction.south)

                if self.animation:
                    self.print_maze()

            self.recursive_division(x, y, width, row - y, axis)
            self.recursive_division(x, row, width, height - row + y, axis)

        if not axis:
            if width == 2:
                col = x + 1
            else:
                col = random.randrange(x + 1, x + width)

                # controllare il while perche la guardia non controllava
                # self.maze[y][col].visited ma self.maze[y][col]

                while self.maze[y][col].visited == 42:
                    col = random.randrange(x + 1, x + width)

            open = random.randint(y, y + height - 1)
            while self.maze[open][col].visited == 42:
                open = random.randint(y, y + height - 1)

            for row in range(y, y + height):
                if row == open:
                    continue

                self.maze[row][col].close_wall(Direction.west)
                self.maze[row][col - 1].close_wall(Direction.east)

                if self.animation:
                    self.print_maze()
            self.recursive_division(x, y, col - x, height, axis)
            self.recursive_division(col, y, width - col + x, height, axis)

    def hak_helper(self, row: int, col: int) -> int:
        """Check if all neighbooring cells are visited.

        Args:
            row: the row of the cell.
            col: the column of the cell.
        Returns:
            int: 1 (truthy) if all cells are visited.
                 0 (false) otherwise.
        """
        north = (row == 0 or self.maze[row - 1][col].visited)
        south = (row == self.height - 1 or self.maze[row + 1][col].visited)
        east = (col == self.width - 1 or self.maze[row][col + 1].visited)
        west = (col == 0 or self.maze[row][col - 1].visited)

        return north and south and east and west

    def hak_opener(self, r: int, c: int, dir: Direction) -> int:
        """Match direction and open walls.

        Args:
            r: row of the maze.
            c: column of the maze.
            dir: direction chosen.
        Returns:
            int: 1 (truthy) if the wall are opened.
                 0 (falsy) otherwise.
        """
        match dir:

            case Direction.north:
                if (r > 0
                        and not self.maze[r - 1][c].visited):

                    self.maze[r][c].open_wall(Direction.north)
                    self.maze[r - 1][c].open_wall(Direction.south)
                    self.maze[r - 1][c].visited = 1
                    return 1

            case Direction.south:
                if (r < self.height - 1
                        and not self.maze[r + 1][c].visited):

                    self.maze[r][c].open_wall(Direction.south)
                    self.maze[r + 1][c].open_wall(Direction.north)
                    self.maze[r + 1][c].visited = 1
                    return 1

            case Direction.east:
                if (c < self.width - 1
                        and not self.maze[r][c + 1].visited):

                    self.maze[r][c].open_wall(Direction.east)
                    self.maze[r][c + 1].open_wall(Direction.west)
                    self.maze[r][c + 1].visited = 1
                    return 1

            case Direction.west:
                if (c > 0
                        and not self.maze[r][c - 1].visited):

                    self.maze[r][c].open_wall(Direction.west)
                    self.maze[r][c - 1].open_wall(Direction.east)
                    self.maze[r][c - 1].visited = 1
                    return 1
        return 0

    def hunt_and_kill(self) -> None:
        """Hunt and Kill algorithm for maze generation."""
        directions = [
            Direction.north,
            Direction.east,
            Direction.south,
            Direction.west
            ]

        for row in range(self.height):
            for col in range(self.width):
                r, c = row, col
                if self.maze[row][col].visited:
                    continue

                if col > 0 and self.maze[row][col - 1].visited == 1:
                    self.maze[r][c].open_wall(Direction.west)
                    self.maze[r][c - 1].open_wall(Direction.east)

                elif row > 0 and self.maze[row - 1][col].visited == 1:
                    self.maze[r][c].open_wall(Direction.north)
                    self.maze[r - 1][c].open_wall(Direction.south)

                elif (row > 0 and self.maze[row - 1][col].visited == 42 and
                      col > 0 and self.maze[row][col - 1].visited == 42):
                    self.maze[r][c].open_wall(Direction.east)
                    self.maze[r][c + 1].open_wall(Direction.west)
                    self.maze[r][c + 1].open_wall(Direction.east)
                    self.maze[r][c + 1].visited = 1
                    self.maze[r][c + 2].open_wall(Direction.west)

                self.maze[r][c].visited = 1
                while True:

                    if (self.hak_helper(r, c)):
                        break

                    random.shuffle(directions)

                    for direction in directions:
                        match direction:

                            case Direction.north:
                                if self.hak_opener(r, c, direction):
                                    r = r - 1
                                    break

                            case Direction.south:
                                if self.hak_opener(r, c, direction):
                                    r = r + 1
                                    break

                            case Direction.east:
                                if self.hak_opener(r, c, direction):
                                    c = c + 1
                                    break

                            case Direction.west:
                                if self.hak_opener(r, c, direction):
                                    c = c - 1
                                    break

                    if self.animation:
                        self.print_maze()

    def side_neighbors(self,
                       current_set: set[tuple[int, int]],
                       side: str) -> int:

        if side == "top":
            for item in current_set:
                r, c = item[0], item[1]
                if self.maze[r - 1][c].visited != 42:
                    return 1
            return 0

    def side_edger(self,
                   universe: set[tuple[int, int]],
                   current_set: set[tuple[int, int]]) -> None:

        edge_case = False
        choosen = random.choice(list(current_set))
        r, c = choosen[0], choosen[1]

        while self.maze[r - 1][c].visited == 42:
            if not self.side_neighbors(current_set, "top"):
                edge_case = True

                min_item = min(list(current_set),
                               key=lambda x: x[1])
                max_item = max(list(current_set),
                               key=lambda x: x[1])

                min_r, min_c = min_item[0], min_item[1]
                max_r, max_c = max_item[0], max_item[1]

                if not self.maze[min_r][min_c - 1].visited == 42:
                    self.maze[min_r][min_c].open_wall(Direction.west)
                    self.maze[min_r][min_c - 1].open_wall(Direction.east)
                    current_set.add((min_r, min_c - 1))

                elif not self.maze[max_r][max_c + 1].visited == 42:
                    self.maze[max_r][max_c].open_wall(Direction.east)
                    self.maze[max_r][max_c + 1].open_wall(Direction.west)
                    current_set.add((max_r, max_c + 1))

                if self.animation:
                    self.print_maze()

            else:
                choosen = random.choice(list(current_set))
                r, c = choosen[0], choosen[1]

        if not edge_case:
            self.maze[r][c].open_wall(Direction.north)
            self.maze[r - 1][c].open_wall(Direction.south)

        for item in current_set:
            universe.add(item)
        current_set.clear()

    def sidewinder(self) -> None:

        universe: set[tuple[int, int]] = set()
        for col in range(self.width):
            if col == 0:
                continue
            else:
                self.maze[0][col].open_wall(Direction.west)
                self.maze[0][col - 1].open_wall(Direction.east)

            if self.animation:
                self.print_maze()

        for row in range(1, self.height):
            current_set: set[tuple[int, int]] = set(())
            for col in range(self.width):
                if self.maze[row][col].visited == 42:
                    continue

                coin = random.randint(0, 1)
                current_set.add((row, col))

                if (coin
                        and col < self.width - 1
                        and self.maze[row][col + 1].visited != 42
                        and self.maze[row][col].is_closed(Direction.north)):
                    self.maze[row][col].open_wall(Direction.east)
                    self.maze[row][col + 1].open_wall(Direction.west)

                    if self.animation:
                        self.print_maze()

                if (coin
                        and col < self.width - 1
                        and self.maze[row][col + 1].visited == 42):
                    coin = not coin

                if (not coin
                        or col == self.width - 1):
                    self.side_edger(universe, current_set)

                for item in current_set:
                    universe.add(item)

            if self.animation:
                self.print_maze()

    def binary_tree(self) -> None:
        """Binary Tree algorithm for maze generation."""
        i: int = 0
        j: int = 0
        for j in range(self.width):
            for i in range(self.height):
                if (i == self.height - 1 and j == self.width - 1):
                    break

                if i == self.height - 1:
                    choice = 1
                elif j == self.width - 1:
                    choice = 0

                elif (self.maze[i][j].visited == 42 or
                        (self.maze[i + 1][j].visited == 42) and
                        (self.maze[i][j + 1].visited == 42)):
                    continue

                elif (self.maze[i + 1][j + 1].visited == 42 and
                      self.maze[i - 1][j + 1].visited == 42 and
                      self.maze[i + 1][j - 1].visited == 42 and
                      self.maze[i - 1][j - 1].visited != 42):
                    choice = 2

                elif self.maze[i][j + 1].visited == 42:
                    choice = 0
                elif self.maze[i + 1][j].visited == 42:
                    choice = 1
                else:
                    choice = random.randint(0, 1)

                match choice:
                    case 1:
                        self.maze[i][j].open_wall(Direction.east)
                        self.maze[i][j + 1].open_wall(Direction.west)

                    case 0:
                        self.maze[i][j].open_wall(Direction.south)
                        self.maze[i + 1][j].open_wall(Direction.north)

                    case 2:
                        self.maze[i][j].open_wall(Direction.south)
                        self.maze[i][j].open_wall(Direction.east)
                        self.maze[i + 1][j].open_wall(Direction.north)
                        self.maze[i][j + 1].open_wall(Direction.west)

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
        """Open all walls of the maze except from boundaries and '42' walls."""
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
                open_walls += cell.total_open()

        i = 0
        while i < round(open_walls / 13.37):

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
        directions = [
            Direction.north,
            Direction.east,
            Direction.south,
            Direction.west
            ]

        self.maze[row][col].visited = 1
        if self.maze[row][col].is_exit:
            self.path = path
            return

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

            if self.animation and self.solution:
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
        if (r >= len(self.maze) - 1
                or c >= len(self.maze[0]) - 1):
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

        clear_screen()
        player = "\033[48;2;255;255;255m  \033[0m"
        print(self.theme['wall'] * (len(self.maze[0]) * 2 + 1))

        for row in range(len(self.maze)):
            line_str = self.theme['wall']

            for col in range(len(self.maze[row])):

                if (self.maze[row][col].is_player
                        and not self.maze[row][col].x_sub
                        and not self.maze[row][col].y_sub):
                    line_str += player

                elif self.maze[row][col].is_entry:
                    line_str += self.theme['entry']

                elif self.maze[row][col].is_exit:
                    line_str += self.theme['exit']

                elif self.maze[row][col].target:
                    line_str += self.theme['ft']

                elif self.maze[row][col].is_solved:
                    if self.solution:
                        line_str += self.theme['solved']
                    else:
                        line_str += self.theme['path']

                elif self.maze[row][col].visited == 42:
                    line_str += self.theme['ft']

                else:
                    line_str += self.theme['path']

                if (self.maze[row][col].is_player
                        and self.maze[row][col].x_sub
                        and not self.maze[row][col].y_sub):
                    line_str += player

                elif (col < self.width - 1 and
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

            bottom_str = self.theme['wall']
            for col in range(len(self.maze[row])):

                if (self.maze[row][col].is_player
                        and not self.maze[row][col].x_sub
                        and self.maze[row][col].y_sub):
                    bottom_str += player

                elif (row < self.height - 1 and
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

                if (self.maze[row][col].is_player
                        and self.maze[row][col].x_sub
                        and self.maze[row][col].y_sub):
                    bottom_str += player

                elif (self.hide_corner(row, col)):
                    bottom_str += self.theme['path']
                else:
                    bottom_str += self.theme['wall']

            print(bottom_str)
        time.sleep(self.sleep_time)

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

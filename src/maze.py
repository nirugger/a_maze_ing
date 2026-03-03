from src.cell import Cell
from src.cell import Direction
import random
import time
import subprocess
import platform
from typing import Any
from collections import deque
from src.themes import THEMES


def clear_screen() -> None:
    if platform.system() == "Windows":
        print("\033[2J\033[H")
    else:
        subprocess.run("clear", shell=True)


class Maze:

    def __init__(self, config: dict[str, Any]) -> None:

        self.width: int = config["WIDTH"]
        self.height: int = config["HEIGHT"]
        self.entry: tuple[int] = config["ENTRY"]
        self.exit: tuple[int] = config["EXIT"]
        self.start: tuple[int] = (config["START"]
                                  if config["START"]
                                  else config["ENTRY"])
        self.output: str = config["OUTPUT_FILE"]
        self.perfect: bool = config["PERFECT"]
        self.algo: str = config.get("ALGORITHM", None)
        self.theme: dict = THEMES['default']
        self.seed: Any = config.get('SEED', None)
        self.path = ""
        self.error_message = ""
        self.maze = None
        self.animation = True
        self.solution = True
        self.two_forty = True

    def init_maze(self) -> None:

        maze: list[list[Cell]] = []
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

    def never_been_there(self) -> None:

        for row in self.maze:
            for cell in row:
                cell.is_solved = False
                cell.steps = 0
                if cell.visited != 42:
                    cell.visited = 0
        self.path = ""

    def forty_two(self) -> None:

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

        # self.init_maze()

        algos: dict[str, callable] = {
            "backtrack": self.backtrack,
            "prim": self.prim,
            "kruskal": self.kruskal
            }

        match self.algo:

            case "backtrack":
                algos['backtrack'](self.start[1], self.start[0])

            case "prim":
                algos['prim'](self.start[1], self.start[0],
                              [(self.start[1], self.start[0])])

            case "kruskal":
                algos['kruskal']()

    def backtrack(self, col: int, row: int) -> None:

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

    def prim(self, col: int, row: int, frontier: list[tuple]) -> None:

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

        directions = [
            Direction.north,
            Direction.east,
            Direction.south,
            Direction.west
            ]

        krusk_list: list[set] = []
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

    def make_it_wrong(self) -> None:

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

        directions = [
            Direction.north,
            Direction.east,
            Direction.south,
            Direction.west
            ]

        random.shuffle(directions)
        for row in range(1, self.height - 1):
            for col in range(1, self.width - 1):
                if self.maze[row][col].walls == 0:
                    if self.valid_helper(row, col):
                        self.maze[row][col].close_wall(directions[0])
                        self.maze[row][col].close_wall(directions[1])
                        if self.animation:
                            self.print_maze()

    def backtrack_solver(self, col: int, row: int, path: str) -> None:

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

        c, r = self.entry
        queue: deque[tuple[int]] = deque([(r, c)])
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

    def hide_corner(self, r: int, c: int) -> bool:
        if r >= len(self.maze) - 1 or c >= len(self.maze[0]) - 1:
            return False
        se = (self.maze[r][c].is_open(Direction.south) and
              self.maze[r][c].is_open(Direction.east))
        nw = (self.maze[r + 1][c + 1].is_open(Direction.north) and
              self.maze[r + 1][c + 1].is_open(Direction.west))
        return se and nw

    def print_maze(self) -> None:

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
                    line_str += self.theme['start']

                elif self.maze[row][col].is_exit:
                    line_str += self.theme['end']

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

        result = ""

        for row in self.maze:
            result += ("".join(str(cell) for cell in row)) + "\n"

        return result

    def __repr__(self) -> str:

        return '\n'.join(str(row) for row in self.maze)

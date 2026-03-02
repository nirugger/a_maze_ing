from src.cell import Cell
from src.cell import Direction
import random
import time
import subprocess
import platform
from typing import Any
from src.themes import THEMES


def clear_screen():
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
        self.start: tuple[int] = (config["STARTING_POINT"]
                                  if config["STARTING_POINT"]
                                  else config["ENTRY"])
        self.output: str = config["OUTPUT_FILE"]
        self.perfect: bool = config["PERFECT"]
        self.algo: str = config.get("ALGORITHM", None)
        self.theme: dict = THEMES['default']
        self.path = ""
        self.error_message = ""
        self.maze = None

    def init_maze(self) -> None:

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
        if self.width < 9 or self.height < 7:
            self.error_message = "Maze too small to contain '42'"
        else:
            self.forty_two()
            if (self.maze[self.entry[1]][self.entry[0]].visited == 42 or
                    self.maze[self.exit[1]][self.exit[0]].visited == 42):
                raise ValueError("[ERR] Keypoints inside the 42!")

    def never_been_there(self) -> None:

        for row in self.maze:
            for cell in row:
                if cell.visited != 42:
                    cell.visited = False
        self.path = ""

    def unsolve(self):

        for row in self.maze:
            for cell in row:
                cell.is_solved = False

    def forty_two(self):

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

    def create_maze(self):

        self.init_maze()

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
        self.print_maze()

        i = 0
        for direction in directions:
            match direction:
                case Direction.north:
                    if row > 0 and not self.maze[row - 1][col].visited:
                        self.maze[row][col].open_wall(Direction.north)
                        self.maze[row - 1][col].open_wall(Direction.south)
                        self.backtrack(row=(row - 1), col=col)

                case Direction.south:
                    if row < self.height - 1 and not self.maze[row + 1][col].visited:
                        self.maze[row][col].open_wall(Direction.south)
                        self.maze[row + 1][col].open_wall(Direction.north)
                        i += 1
                        self.backtrack(row=(row + 1), col=col)

                case Direction.east:
                    if col < self.width - 1 and not self.maze[row][col + 1].visited:
                        self.maze[row][col].open_wall(Direction.east)
                        self.maze[row][col + 1].open_wall(Direction.west)
                        self.backtrack(row=row, col=(col + 1))

                case Direction.west:
                    if col > 0 and not self.maze[row][col - 1].visited:
                        self.maze[row][col].open_wall(Direction.west)
                        self.maze[row][col - 1].open_wall(Direction.east)
                        self.backtrack(row=row, col=(col - 1))

    def prim(self, col: int, row: int, frontiera: list[tuple]) -> None:

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
                        frontiera.append((col, row-1))

                        self.maze[row - 1][col].visited = True

                        item = random.choice(frontiera)
                        self.prim(row=item[1], col=item[0], frontiera=frontiera)

                case Direction.south:
                    if row < self.height - 1 and not self.maze[row + 1][col].visited:
                        self.maze[row][col].open_wall(Direction.south)
                        self.maze[row + 1][col].open_wall(Direction.north)
                        frontiera.append((col, row+1))
                        self.maze[row + 1][col].visited = True

                        item = random.choice(frontiera)

                        self.prim(row=item[1], col=item[0], frontiera=frontiera)

                case Direction.east:
                    if col < self.width - 1 and not self.maze[row][col + 1].visited:
                        self.maze[row][col].open_wall(Direction.east)
                        self.maze[row][col + 1].open_wall(Direction.west)
                        self.maze[row][col + 1].visited = True

                        frontiera.append((col+1, row))
                        item = random.choice(frontiera)

                        self.prim(row=item[1], col=item[0], frontiera=frontiera)

                case Direction.west:
                    if col > 0 and not self.maze[row][col - 1].visited:
                        self.maze[row][col].open_wall(Direction.west)
                        self.maze[row][col - 1].open_wall(Direction.east)
                        frontiera.append((col-1, row))
                        self.maze[row][col-1].visited = True

                        item = random.choice(frontiera)
                        self.prim(row=item[1], col=item[0], frontiera=frontiera)

        if (col, row) in frontiera:
            frontiera.remove((col, row))
        if frontiera:
            item = random.choice(frontiera)
            self.prim(col=item[0], row=item[1], frontiera=frontiera)

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
                        self.backtrack_solver(row=(row - 1), col=col, path=path + 'N')

                case Direction.south:
                    if (row < self.height - 1 and not
                            self.maze[row + 1][col].visited and not
                            self.maze[row][col].is_closed(Direction.south)):
                        self.backtrack_solver(row=(row + 1), col=col, path=path + 'S')

                case Direction.east:
                    if (col < self.width - 1 and not
                            self.maze[row][col + 1].visited and not
                            self.maze[row][col].is_closed(Direction.east)):
                        self.backtrack_solver(row=row, col=(col + 1), path=path + 'E')

                case Direction.west:
                    if (col > 0 and not
                            self.maze[row][col - 1].visited and not
                            self.maze[row][col].is_closed(Direction.west)):
                        self.backtrack_solver(row=row, col=(col - 1), path=path + 'W')

        self.maze[row][col].visited = 0

    def assign_solution(self) -> None:
        col, row = self.entry[0], self.entry[1]
        path = self.path
        for char in path:
            self.print_maze()
            match char:
                case 'N':
                    row, col = row - 1, col
                case 'S':
                    row, col = row + 1, col
                case 'E':
                    row, col = row, col + 1
                case 'W':
                    row, col = row, col - 1
            self.maze[row][col].is_solved = True

    def print_maze(self):

        if not self or not self.maze:
            return
        clear_screen()

        WALL_COLOR = self.theme['wall']
        FT_COLOR = self.theme['ft']
        FT_WALL_COLOR = self.theme['ft_wall']
        START_COLOR = self.theme['start']
        END_COLOR = self.theme['end']
        PATH_COLOR = self.theme['path']
        SOLVED_COLOR = self.theme['solved']

        print(WALL_COLOR * (self.width * 2 + 1))

        for row in range(len(self.maze)):
            line_str = WALL_COLOR

            for col in range(len(self.maze[row])):
                if self.maze[row][col].is_entry:
                    line_str += START_COLOR
                elif self.maze[row][col].is_exit:
                    line_str += END_COLOR
                elif self.maze[row][col].is_solved:
                    line_str += SOLVED_COLOR
                elif self.maze[row][col].visited == 42:
                    line_str += FT_COLOR
                else:
                    line_str += PATH_COLOR

                if (col < self.width - 1 and
                    (self.maze[row][col].visited == 42 and
                     self.maze[row][col + 1].visited == 42)):
                    line_str += FT_WALL_COLOR
                elif self.maze[row][col].is_closed(Direction.east):
                    line_str += WALL_COLOR
                elif ((self.maze[row][col].is_entry or
                      self.maze[row][col].is_solved) and
                      self.maze[row][col + 1].is_solved):
                    line_str += SOLVED_COLOR
                else:
                    line_str += PATH_COLOR

            print(line_str)

            bottom_str = WALL_COLOR

            for col in range(len(self.maze[row])):
                if (row < self.height - 1 and
                    (self.maze[row][col].visited == 42 and
                     self.maze[row + 1][col].visited == 42)):
                    bottom_str += FT_WALL_COLOR
                elif self.maze[row][col].is_closed(Direction.south):
                    bottom_str += WALL_COLOR
                elif ((self.maze[row][col].is_entry or
                      self.maze[row][col].is_solved) and
                      self.maze[row + 1][col].is_solved):
                    bottom_str += SOLVED_COLOR
                else:
                    bottom_str += PATH_COLOR

                bottom_str += WALL_COLOR

            print(bottom_str)
        time.sleep(0.0)

    def __str__(self) -> str:

        result = ""

        for row in self.maze:
            result += ("".join(str(cell) for cell in row)) + "\n"
        return result

    def __repr__(self) -> str:
        return '\n'.join(str(row) for row in self.maze)

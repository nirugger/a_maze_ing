from mazegen.maze import Maze
from mazegen.cell import Cell
from mazegen.cell import Direction
import sys


def getchar_win() -> int:
    import msvcrt

    if msvcrt.kbhit():      # se è stato premuto un tasto
        key = msvcrt.getch()  # legge il tasto
        if key in (b'\xe0', b'\x00'):
            key2 = msvcrt.getch()  # byte reale della freccia
            while msvcrt.kbhit():
                msvcrt.getch()
            if key2 == b'H':       # ↑
                sys.stdin.flush
                return Direction.north
            elif key2 == b'P':     # ↓
                sys.stdin.flush
                return Direction.south
            elif key2 == b'K':     # ←
                sys.stdin.flush
                return Direction.west
            elif key2 == b'M':     # →
                sys.stdin.flush
                return Direction.east
        sys.stdin.flush


def getchar_linux():
    import termios
    import tty
 
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)  # legge 1 carattere
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch


def getchar():
    if sys.platform.startswith("win"):
        return getchar_win()
    else:
        return getchar_linux()


class Game:

    def __init__(self, starting_x_pos: int, starting_y_pos: int) -> None:
        self.x = starting_x_pos
        self.y = starting_y_pos
        self.x_sub = 0
        self.y_sub = 0

    def unset_pos(self, maze: list[list[Cell]]) -> None:

        maze[self.y][self.x].is_player = 0
        maze[self.y][self.x].x_sub = 0
        maze[self.y][self.x].y_sub = 0

    def set_pos(self, maze: list[list[Cell]]) -> None:

        maze[self.y][self.x].is_player = 1
        maze[self.y][self.x].x_sub = self.x_sub
        maze[self.y][self.x].y_sub = self.y_sub

    def set_player(self, maze:list[list[Cell]], direction: Direction) -> None:
        if not maze or not maze[0]:
            return

        height = len(maze)
        width = len(maze[0])

        match direction:
            case Direction.north:
                if self.y_sub:
                    # if not self.x_sub:
                    #     self.y_sub = 0
                    # else:
                    #     if (self.y > 0 and self.x > 0
                    #             and maze[self.y - 1][self.x - 1].is_open(Direction.south)
                    #             and maze[self.y - 1][self.x - 1].is_open(Direction.east)):
                    #         self.y -= 1
                    #         self.y_sub = 1
                    pass

                else:
                    if self.y > 0 and maze[self.y][self.x].is_open(direction):
                        self.y -= 1
                        self.y_sub = 1

            case Direction.south:
                if (not self.y_sub
                        and maze[self.y][self.x].is_open(direction)):
                    if not self.x_sub:
                        self.y_sub = 1
                    else:
                        if (self.y < height - 1
                                and self.x < width - 1
                                and maze[self.y + 1][self.x + 1].is_open(Direction.north)
                                and maze[self.y + 1][self.x + 1].is_open(Direction.west)):
                            self.y += 1
                            self.y_sub = 0

                else:
                    if (self.y < height - 1
                            and maze[self.y][self.x].is_open(direction)):
                        self.y += 1
                        self.y_sub = 0

            case Direction.west:
                if self.x_sub:
                    # if not self.y_sub:
                    #     self.x_sub = 0
                    # else:
                    #     if (self.y > 0 and self.x > 0
                    #             and maze[self.y - 1][self.x - 1].is_open(Direction.south)
                    #             and maze[self.y - 1][self.x - 1].is_open(Direction.east)):
                    #         self.x -= 1
                    #         self.x_sub = 0
                    pass

                else:
                    if self.x > 0 and maze[self.y][self.x].is_open(direction):
                        self.x -= 1
                        self.x_sub = 1

            case Direction.east:
                if (not self.x_sub
                        and maze[self.y][self.x].is_open(direction)):
                    if not self.y_sub:
                        self.x_sub = 1
                    else:
                        if (self.y < height - 1
                                and self.x < width - 1
                                and maze[self.y + 1][self.x + 1].is_open(Direction.north)
                                and maze[self.y + 1][self.x + 1].is_open(Direction.west)):
                            self.x += 1
                            self.x_sub = 0


                else:
                    if (self.x < width - 1
                            and maze[self.y][self.x].is_open(direction)):
                        self.x += 1
                        self.x_sub = 0


    def move_player(self, maze: Maze) -> None:
        while True:

            if (maze.maze[self.y][self.x].is_exit
                    and not self.x_sub and not self.y_sub):
                break

            direction = getchar()
            if direction:
                self.unset_pos(maze.maze)
                self.set_player(maze.maze, direction)
                self.set_pos(maze.maze)
            maze.print_maze()


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
            if key2 == b'H':       # ↑
                return Direction.north
            elif key2 == b'P':     # ↓
                return Direction.south
            elif key2 == b'K':     # ←
                return Direction.west
            elif key2 == b'M':     # →
                return Direction.east


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
        self.x_pos = starting_x_pos
        self.y_pos = starting_y_pos
        self.x_sub_pos = 0
        self.y_sub_pos = 0

    def unset_pos(self, maze:list[list[Cell]]) -> None:

        maze[self.x_pos][self.y_pos].is_player = 0
        maze[self.x_pos][self.y_pos].x_sub_pos = 0
        maze[self.x_pos][self.y_pos].y_sub_pos = 0

    def set_pos(self, maze:list[list[Cell]]) -> None:

        maze[self.y_pos][self.x_pos].is_player = 1
        maze[self.y_pos][self.x_pos].x_sub_pos = self.x_sub_pos
        maze[self.y_pos][self.x_pos].y_sub_pos = self.y_sub_pos

    def set_player(self, maze:list[list[Cell]], direction: Direction) -> None:

        match direction:
            case Direction.north:
                if self.y_sub_pos:
                    self.y_sub_pos = 0
                else:
                    if self.y_pos > 0 and maze[self.y_pos][self.x_pos].is_open(direction):
                        self.y_pos -= 1
                        self.y_sub_pos = 1

            case Direction.south:
                if not self.y_sub_pos:
                    self.y_sub_pos = 1
                else:
                    if self.y_pos > 0 and maze[self.y_pos][self.x_pos].is_open(direction):
                        self.y_pos += 1
                        self.y_sub_pos = 0

            case Direction.west:
                if self.y_sub_pos:
                    self.y_sub_pos = 0
                else:
                    if self.y_pos > 0 and maze[self.y_pos][self.x_pos].is_open(direction):
                        self.y_pos -= 1
                        self.y_sub_pos = 1

            case Direction.east:
                if not self.y_sub_pos:
                    self.y_sub_pos = 1
                else:
                    if self.y_pos > 0 and maze[self.y_pos][self.x_pos].is_open(direction):
                        self.y_pos += 1
                        self.y_sub_pos = 0


    def move_player(self, maze: Maze) -> None:
        while True:

            if (maze.maze[self.y_pos][self.x_pos].is_exit
                    and not self.x_sub_pos and not self.y_sub_pos):
                break

            direction = getchar()
            if direction:
                self.unset_pos(maze.maze)
                self.set_player(maze.maze, direction)
                self.set_pos(maze.maze)
            maze.print_maze()


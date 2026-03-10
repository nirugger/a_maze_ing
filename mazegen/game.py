from mazegen.maze import Maze
from mazegen.cell import Cell
from mazegen.cell import Direction
import sys


def getchar_windows() -> Direction | None:

    try:
        import msvcrt

        if msvcrt.kbhit():  # type: ignore[attr-defined]
            key = msvcrt.getch()  # type: ignore[attr-defined]
            if key in (b'\xe0', b'\x00'):
                key2 = msvcrt.getch()  # type: ignore[attr-defined]
                while msvcrt.kbhit():  # type: ignore[attr-defined]
                    msvcrt.getch()  # type: ignore[attr-defined]
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
    except Exception:
        print("[ERROR]: "
              "This is not windows!!!")
    return None


def getchar_linux() -> Direction | str | None:
    import termios
    import tty

    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
        if key == '\x1b':
            key += sys.stdin.read(2)
            if key == '\x1b[A':
                return Direction.north
            elif key == '\x1b[B':
                return Direction.south
            elif key == '\x1b[C':
                return Direction.east
            elif key == '\x1b[D':
                return Direction.west

        elif key == 'w':
            return Direction.north
        elif key == 's':
            return Direction.south
        elif key == 'd':
            return Direction.east
        elif key == 'a':
            return Direction.west
        elif key == 'q' or key == 'e':
            return key
        return None
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def getchar() -> Direction | str | None:
    if sys.platform.startswith("win"):
        return getchar_windows()
    else:
        return getchar_linux()


class Game:

    def __init__(self, starting_x_pos: int, starting_y_pos: int) -> None:
        self.x = starting_x_pos
        self.y = starting_y_pos
        self.x_sub = 0
        self.y_sub = 0

    def unset_pos(self, maze: list[list[Cell]]) -> None:

        maze[self.y][self.x].is_player = False
        maze[self.y][self.x].x_sub = 0
        maze[self.y][self.x].y_sub = 0

    def set_pos(self, maze: list[list[Cell]]) -> None:

        maze[self.y][self.x].is_player = True
        maze[self.y][self.x].x_sub = self.x_sub
        maze[self.y][self.x].y_sub = self.y_sub

    def set_player(self, maze: list[list[Cell]], direction: Direction) -> None:
        if not maze or not maze[0]:
            return

        height = len(maze)
        width = len(maze[0])

        match direction:
            case Direction.north:
                if self.y_sub:
                    self.y_sub = 0

                else:
                    if not self.x_sub:
                        if self.y > 0 and maze[self.y][self.x].is_open(
                                direction
                                ):
                            self.y -= 1
                            self.y_sub = 1
                    else:
                        if (self.y > 0 and self.x < width - 1
                                and maze[self.y][self.x].is_open(
                                    Direction.north)
                                and maze[self.y - 1][self.x + 1].is_open(
                                    Direction.south)
                                and maze[self.y - 1][self.x + 1].is_open(
                                    Direction.west)):
                            self.y -= 1
                            self.y_sub = 1

            case Direction.south:
                if (not self.y_sub
                        and maze[self.y][self.x].is_open(
                            direction)):
                    if not self.x_sub:
                        self.y_sub = 1
                    else:
                        if (self.y < height - 1
                                and self.x < width - 1
                                and maze[self.y + 1][self.x + 1].is_open(
                                    Direction.north)
                                and maze[self.y + 1][self.x + 1].is_open(
                                    Direction.west)):
                            self.y_sub = 1

                else:
                    if (self.y < height - 1
                            and maze[self.y][self.x].is_open(
                                direction)):
                        self.y += 1
                        self.y_sub = 0

            case Direction.west:
                if self.x_sub:
                    self.x_sub = 0

                else:
                    if not self.y_sub:
                        if self.x > 0 and maze[self.y][self.x].is_open(
                                direction):
                            self.x -= 1
                            self.x_sub = 1
                    else:
                        if (self.y < height - 1 and self.x > 0
                                and maze[self.y][self.x - 1].is_open(
                                    Direction.south)
                                and maze[self.y][self.x - 1].is_open(
                                    Direction.east)
                                and maze[self.y + 1][self.x - 1].is_open(
                                    Direction.east)):
                            self.x -= 1
                            self.x_sub = 1

            case Direction.east:
                if (not self.x_sub
                        and maze[self.y][self.x].is_open(
                            direction)):
                    if not self.y_sub:
                        self.x_sub = 1
                    else:
                        if (self.y < height - 1
                                and self.x < width - 1
                                and maze[self.y + 1][self.x + 1].is_open(
                                    Direction.north)
                                and maze[self.y + 1][self.x + 1].is_open(
                                    Direction.west)):
                            self.x_sub = 1

                else:
                    if (self.x < width - 1
                            and maze[self.y][self.x].is_open(direction)):
                        self.x += 1
                        self.x_sub = 0

    @staticmethod
    def dis_play_menu() -> None:

        print()
        print("╔════════════════════════════════════════════════╗")
        print("║        WELCOME TO A_MAZE_ING: THE GAME!        ║")
        print("╠════════════════════════════════════════════════╣")
        print("║                  MOVE AROUND:                  ║")
        print("║   ↑  ←  ↓  →          or          w  a  s  d   ║")
        print("╠════════════════════════════════════════════════╣")
        print("║ e: toggle solution [ON/OFF]      q: quit game  ║")
        print("╚════════════════════════════════════════════════╝")
        print()

    def move_player(self, maze: Maze) -> None:
        maze.solution = False
        while True:
            maze.print_maze()
            self.dis_play_menu()

            if (maze.maze[self.y][self.x].is_exit
                    and not self.x_sub and not self.y_sub):
                break

            key = getchar()
            if key:
                if key == 'e':
                    maze.solution = not maze.solution
                elif key == 'q' or key == 'Q':
                    break
                elif isinstance(key, Direction):
                    self.unset_pos(maze.maze)
                    self.set_player(maze.maze, key)
                    self.set_pos(maze.maze)

        self.unset_pos(maze.maze)

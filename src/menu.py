from src.maze import Maze
from src.maze import clear_screen
from src.requirement_parser import Parser
from src.requirement_parser import MazeConfig
from src.themes import THEMES
from typing import Optional, Any
from random import randint as r
from random import seed
from pydantic import ValidationError
import copy


class Menu:

    maze: Optional[Maze] = None
    config: Optional[dict[str, Any]] = None

    @classmethod
    def a_maze_init(cls, file: str) -> None:
        try:
            cls.config = Parser.parse_config(file)
            cls.maze = Maze(cls.config)
        except (EOFError, Exception) as e:
            print(repr(e))
            exit(1)

    @classmethod
    def maze_generator(cls) -> None:

        cls.maze.init_maze()
        cls.maze.create_maze()
        cls.maze.print_maze()
        if not cls.maze.perfect:
            cls.maze.make_it_wrong()
        cls.maze.never_been_there()
        cls.maze.unsolve()
        cls.maze.breadth_first_search_solver()
        cls.maze.assign_solution()
        if cls.maze.error_message:
            print(cls.maze.error_message)

    @classmethod
    def display_main_menu(cls) -> None:
        print()
        print()
        print()
        print("╔═════════════════════════════════════════════════╗")
        print("║                    W31C0M3 2                    ║")
        print("║    ▗▄▖ ▗▖  ▗▖ ▗▄▖ ▗▄▄▄▄▖▗▄▄▄▖▗▄▄▄▖▗▖  ▗▖ ▗▄▄▖   ║")
        print("║   ▐▌ ▐▌▐▛▚▞▜▌▐▌ ▐▌   ▗▞▘▐▌     █  ▐▛▚▖▐▌▐▌      ║")
        print("║   ▐▛▀▜▌▐▌  ▐▌▐▛▀▜▌ ▗▞▘  ▐▛▀▀▘  █  ▐▌ ▝▜▌▐▌▝▜▌   ║")
        print("║   ▐▌ ▐▌▐▌  ▐▌▐▌ ▐▌▐▙▄▄▄▖▐▙▄▄▖▗▄█▄▖▐▌  ▐▌▝▚▄▞▘   ║")
        print("║                                                 ║")
        print("║            a  wond_err_full  project            ║")
        print("╚═════════════════════════════════════════════════╝")
        print()
        print()
        print("╔══════════════════════════╗╔═════════════════════╗")
        print("║  1: Generate Maze        ║║   coded by:         ║")
        print("║  2: Configure Maze       ║║                     ║")
        print("║  3: Colors!              ║║      tvanni &       ║")
        print("║  4: animation            ║║      nirugger       ║")
        print("║  5: solution             ║║                     ║")
        print("║  q: Exit                 ║║  (aka Tom & Gerru)  ║")
        print("╚══════════════════════════╝╚═════════════════════╝")
        print()
        print()
        print()

    @classmethod
    def main_menu(cls) -> None:

        msg = "\n"
        while True:
            clear_screen()
            cls.display_main_menu()
            print(msg)
            choice = input("Choose your path: ").strip().lower()
            match choice:
                case "1":
                    try:
                        cls.maze_generator()
                        cls.maze_menu()
                        msg = "\n"
                    except ValueError as e:
                        msg = e.args[0]
                case "2":
                    try:
                        cls.config_menu()
                        msg = "\n"
                    except ValidationError as e:
                        for err in e.errors():
                            msg += err['msg'] + "\n"
                case "3":
                    cls.color_menu()
                    clear_screen()
                    msg = "\n"
                case "4":
                    cls.maze.animation = not cls.maze.animation
                    msg = f"Maze animation changed to {cls.maze.animation}\n"
                case "5":
                    cls.maze.solution = not cls.maze.solution
                    state = "VISIBLE" if cls.maze.solution else "INVISIBLE"
                    msg = f"Maze solution changed to '{state}'\n"
                    msg = "\n"
                case "q":
                    cls.closure()
                case _:
                    msg = "error: invalid input\n"

    @classmethod
    def display_maze_menu(cls) -> None:

        print()
        print("╔═════════════════════════════════════════════════╗")
        print("║                    7H47  W45                    ║")
        print("║    ▗▄▖ ▗▖  ▗▖ ▗▄▖ ▗▄▄▄▄▖▗▄▄▄▖▗▄▄▄▖▗▖  ▗▖ ▗▄▄▖   ║")
        print("║   ▐▌ ▐▌▐▛▚▞▜▌▐▌ ▐▌   ▗▞▘▐▌     █  ▐▛▚▖▐▌▐▌      ║")
        print("║   ▐▛▀▜▌▐▌  ▐▌▐▛▀▜▌ ▗▞▘  ▐▛▀▀▘  █  ▐▌ ▝▜▌▐▌▝▜▌   ║")
        print("║   ▐▌ ▐▌▐▌  ▐▌▐▌ ▐▌▐▙▄▄▄▖▐▙▄▄▖▗▄█▄▖▐▌  ▐▌▝▚▄▞▘   ║")
        print("║                                                 ║")
        print("║             H0W 480U7 4N07H3R 7RY ?             ║")
        print("╚═════════════════════════════════════════════════╝")
        print()
        print()
        print("╔══════════════════════════╗╔═════════════════════╗")
        print("║  1: Re-Generate Maze     ║║   coded by:         ║")
        print("║  2: Configure Maze       ║║                     ║")
        print("║  3: Colors!              ║║      tvanni &       ║")
        print("║  4: Animation            ║║      nirugger       ║")
        print("║  5: Solution             ║║                     ║")
        print("║  q: Exit                 ║║  (aka Tom & Gerru)  ║")
        print("╚══════════════════════════╝╚═════════════════════╝")

    @classmethod
    def maze_menu(cls) -> None:

        msg = "\n"
        while True:
            cls.maze.print_maze()
            print(cls.maze.error_message)
            cls.display_maze_menu()
            print(msg)
            choice = input("Re-choose your path: ").strip().lower()
            match choice:
                case "1":
                    try:
                        cls.maze_generator()
                        msg = "\n"
                    except ValueError as e:
                        msg = e.args[0]
                case "2":
                    try:
                        cls.config_menu()
                        msg = "\n"
                    except ValidationError as e:
                        for err in e.errors():
                            msg += err['msg'] + "\n"
                case "3":
                    cls.color_menu()
                    clear_screen()
                    msg = "\n"
                case "4":
                    cls.maze.animation = not cls.maze.animation
                    msg = f"Maze animation changed to {cls.maze.animation}\n"
                case "5":
                    cls.maze.solution = not cls.maze.solution
                    state = "VISIBLE" if cls.maze.solution else "INVISIBLE"
                    msg = f"Maze solution changed to '{state}'\n"
                case "q":
                    cls.closure()
                case _:
                    msg = "error: invalid input\n"
                    clear_screen()
                    cls.maze.print_maze()

    @staticmethod
    def closure():
        print("\n" * 3)
        print("“A labyrinth is not a place to be lost, "
              "but a path to be found.”"
              "\n  — Anonymous")
        print("\n")
        print("“A labyrinth is not a maze, though.”"
              "\n  — nirugger")
        print("\n" * 6)
        exit(1)

    def display_config_menu():

        print()
        print()
        print("╔══════════════════════════════════════════╗")
        print("║  1: WIDTH                                ║")
        print("║  2: HEIGHT                               ║")
        print("║  3: ENTRY                                ║")
        print("║  4: EXIT                                 ║")
        print("║  5: STARTING POINT                       ║")
        print("║  6: PERFECT                              ║")
        print("║  7: ALGORITHM                            ║")
        print("║  8: SEED                                 ║")
        print("║  9: Reset to Default                     ║")
        print("║  q: Back to Main Menu                    ║")
        print("╚══════════════════════════════════════════╝")
        print()

    @classmethod
    def config_menu(cls):

        mod_config = {
            "WIDTH": cls.maze.width,
            "HEIGHT": cls.maze.height,
            "ENTRY": cls.maze.entry,
            "EXIT": cls.maze.exit,
            "START": cls.maze.start,
            "PERFECT": cls.maze.perfect,
            "ALGORITHM": cls.maze.algo,
            "OUTPUT_FILE": cls.maze.output
            }

        msg = "\n"
        while True:
            clear_screen()
            cls.display_config_menu()
            print(msg)
            choice = input("choose an option: ")
            match choice:

                case "1":
                    width = int(input("Choose the width of the maze "
                                "(>=2, <=41): "))
                    if 1 < width < 42:
                        mod_config['WIDTH'] = width
                        msg = f"WIDTH value set to {width}\n"
                    else:
                        msg = "WIDTH value unacceptable (2 <= WIDTH <= 41)\n"

                case "2":
                    height = int(input("Choose the height of the maze "
                                 "(>=2, <=21): "))
                    if 1 < height < 22:
                        mod_config['HEIGHT'] = height
                        msg = f"HEIGHT value set to {height}\n"
                    else:
                        msg = "HEIGHT value unacceptable (2 <= HEIGHT <= 21)\n"

                case "3":
                    x = int(input("Choose the x (>=0): "))
                    y = int(input("Choose the y (>=0): "))
                    if x >= 0 and y >= 0:
                        mod_config['ENTRY'] = f"{x},{y}"
                        msg = f"ENTRY set to ({x}, {y})\n"
                    else:
                        msg = "ENTRY value unacceptable (x,y >= 0)\n"

                case "4":
                    x = int(input("Choose the x (>=0): "))
                    y = int(input("Choose the y (>=0): "))
                    if x >= 0 and y >= 0:
                        mod_config['EXIT'] = f"{x},{y}"
                        msg = f"EXIT set to ({x}, {y})\n"
                    else:
                        msg = "EXIT value unacceptable (x,y >= 0)\n"

                case "5":
                    x = int(input("Choose the x (>=0): "))
                    y = int(input("Choose the y (>=0): "))
                    if x >= 0 and y >= 0:
                        mod_config['START'] = f"{x},{y}"
                        msg = f"STARTING POINT set to ({x}, {y})\n"
                    else:
                        msg = "STARTING POINT value unacceptable (x,y >= 0)\n"

                case "6":
                    choice = input("Must thy maze be PERFECT? [y/n]: ")
                    match choice:
                        case "y":
                            mod_config['PERFECT'] = "true"
                            msg = "PERFECT set to 'TRUE'\n"
                        case "n":
                            mod_config['PERFECT'] = "false"
                            msg = "PERFECT set to 'FALSE'\n"
                        case _:
                            msg = "error: invalid input\n"

                case "7":
                    cls.algorithm_menu()
                    msg = "\n"

                case "8":
                    seed = input("Choose the seed (leave empty for None): ")
                    if not seed:
                        seed = None
                    cls.maze.seed = seed
                    msg = f"SEED set to {seed}\n"

                case "9":
                    mod_config = copy.deepcopy(cls.config)
                    msg = "CONFIG set to 'DEFAULT'\n"

                case "q":
                    mod_config = MazeConfig(**mod_config).model_dump()
                    cls.maze.width = mod_config['WIDTH']
                    cls.maze.height = mod_config['HEIGHT']
                    cls.maze.entry = mod_config['ENTRY']
                    cls.maze.exit = mod_config['EXIT']
                    cls.maze.start = mod_config['START']
                    cls.maze.perfect = mod_config['PERFECT']
                    msg = "\n"
                    return

                case _:
                    msg = "error: invalid input\n"

    def display_algorithm_menu():
        print()
        print("╔══════════════════════════════════════════╗")
        print("║  1: BACKTRACK                            ║")
        print("║  2: PRIM                                 ║")
        print("║  3: KRUSKAL                              ║")
        print("║  q: back to configuration menu           ║")
        print("╚══════════════════════════════════════════╝")
        print()

    @classmethod
    def algorithm_menu(cls):

        msg = "\n"
        while True:
            clear_screen()
            cls.display_config_menu()
            cls.display_algorithm_menu()
            print(msg)
            choice = input("choose an option: ")
            match choice:
                case "1":
                    MazeConfig.ALGORITHM = 'backtrack'
                    cls.maze.algo = 'backtrack'
                    msg = "You choose 'BACKTRACK'. Truly original.\n"
                case "2":
                    MazeConfig.ALGORITHM = 'prim'
                    cls.maze.algo = 'prim'
                    msg = ("You choose 'PRIM'. "
                           "Overall, just another backtrack.\n")
                case "3":
                    MazeConfig.ALGORITHM = 'kruskal'
                    cls.maze.algo = 'kruskal'
                    msg = "You choose 'KRUSKAL'. Slow but steady.\n"
                case "q":
                    return
                case _:
                    msg = "error: invalid input\n"

    def display_color_menu():

        print()
        print()
        print("╔══════════════════════════════════════════╗")
        print("║  1: DEFAULT                              ║")
        print("║  2: OCEAN                                ║")
        print("║  3: FOREST                               ║")
        print("║  4: DESERT                               ║")
        print("║  5: VOLCANIC                             ║")
        print("║  6: CYBERPUNK                            ║")
        print("║  0: R4ND0M                               ║")
        print("║  q: Back to Menu                         ║")
        print("╚══════════════════════════════════════════╝")
        print()

    @classmethod
    def color_menu(cls):

        seed()
        msg = ''
        while True:

            random = {
                "wall":
                    f"\033[48;2;{r(0, 254)};{r(0, 254)};{r(0, 254)}m  \033[0m",
                "path":
                    f"\033[48;2;{r(0, 254)};{r(0, 254)};{r(0, 254)}m  \033[0m",
                "ft":
                    f"\033[48;2;{r(0, 254)};{r(0, 254)};{r(0, 254)}m  \033[0m",
                "ft_wall":
                    f"\033[48;2;{r(0, 254)};{r(0, 254)};{r(0, 254)}m  \033[0m",
                "start":
                    f"\033[48;2;{r(0, 254)};{r(0, 254)};{r(0, 254)}m  \033[0m",
                "end":
                    f"\033[48;2;{r(0, 254)};{r(0, 254)};{r(0, 254)}m  \033[0m",
                "solved":
                    f"\033[48;2;{r(0, 254)};{r(0, 254)};{r(0, 254)}m  \033[0m"
            }

            clear_screen()
            cls.maze.print_maze()
            cls.display_color_menu()
            print(msg)
            choice = input("choose your style: ")
            match choice:
                case "1":
                    cls.maze.theme = THEMES['default']
                    msg = "THEME set to 'DEFAULT'\n"
                case "2":
                    cls.maze.theme = THEMES['ocean']
                    msg = "THEME set to 'OCEAN'\n"
                case "3":
                    cls.maze.theme = THEMES['forest']
                    msg = "THEME set to 'FOREST'\n"
                case "4":
                    cls.maze.theme = THEMES['desert']
                    msg = "THEME set to 'DESERT'\n"
                case "5":
                    cls.maze.theme = THEMES['volcanic']
                    msg = "THEME set to 'VOLCANIC'\n"
                case "6":
                    cls.maze.theme = THEMES['cyberpunk']
                    msg = "THEME set to 'CYBERPUNK'\n"
                case "0":
                    cls.maze.theme = random
                    msg = "THEME set to 'R4ND0M' (warning!)\n"
                case "q":
                    seed(cls.maze.seed)
                    return
                case _:
                    msg = "error: invalid input\n"

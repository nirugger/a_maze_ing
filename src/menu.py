from src.maze import Maze
from src.maze import clear_screen
from src.requirement_parser import Parser
from src.requirement_parser import MazeConfig
from src.themes import THEMES
from typing import Optional
from random import randint as r


class Menu:

    maze: Optional[Maze] = None

    @classmethod
    def amazinit(cls, file: str) -> None:
        try:
            config = Parser.parse_config(file)
            cls.maze = Maze(config)
        except Exception as e:
            print(repr(e))
            exit(1)

    @classmethod
    def maze_generator(cls) -> None:
        try:
            # cls.maze.theme = cls.current_theme

            cls.maze.create_maze()
            cls.maze.print_maze()
            cls.maze.never_been_there()
            cls.maze.unsolve()
            cls.maze.backtrack_solver(cls.maze.entry[0],
                                      cls.maze.entry[1],
                                      path="")
            cls.maze.assign_solution()
            if cls.maze.error_message:
                print(cls.maze.error_message)

        except Exception as e:
            print(str(e))

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
        print("║  1) Generate Maze        ║║   coded by:         ║")
        print("║  2) Configure Maze       ║║      tvanni &       ║")
        print("║  3) Colors!              ║║      nirugger       ║")
        print("║  q) Exit                 ║║  (aka Tom & Gerru)  ║")
        print("╚══════════════════════════╝╚═════════════════════╝")
        print()
        print()
        print()

    @classmethod
    def main_menu(cls) -> None:

        msg = ''
        while True:
            clear_screen()
            cls.display_main_menu()
            print(msg)
            choice = input("Choose your path: ").strip().lower()
            match choice:
                case "1":
                    cls.maze_generator()
                    cls.maze_menu()
                    msg = ''
                case "2":
                    cls.config_menu()
                    msg = ''
                case "3":
                    cls.color_menu()
                    clear_screen()
                    msg = ''
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
        print("║  1) Re-Generate Maze     ║║   coded by:         ║")
        print("║  2) Configure Maze       ║║      tvanni &       ║")
        print("║  3) Colors!              ║║      nirugger       ║")
        print("║  q) Exit                 ║║  (aka Tom & Gerru)  ║")
        print("╚══════════════════════════╝╚═════════════════════╝")
        print()

    @classmethod
    def maze_menu(cls) -> None:

        msg = ''
        while True:
            cls.maze.print_maze()
            cls.display_maze_menu()
            print(msg)
            choice = input("Re-choose your path: ").strip().lower()
            match choice:
                case "1":
                    cls.maze_generator()
                    msg = ''
                case "2":
                    cls.config_menu()
                    msg = ''
                case "3":
                    cls.color_menu()
                    clear_screen()
                    msg = ''
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
        print("║  1) WIDTH                                ║")
        print("║  2) HEIGHT                               ║")
        print("║  3) ENTRY                                ║")
        print("║  4) EXIT                                 ║")
        print("║  5) STARTING_POINT                       ║")
        print("║  6) PERFECT                              ║")
        print("║  7) ALGORITHM                            ║")
        print("║  8) SEED                                 ║")
        print("║  9) Reset to Default                     ║")
        print("║  q) Back to Main Menu                    ║")
        print("╚══════════════════════════════════════════╝")
        print()

    @classmethod
    def config_menu(cls):

        msg = ''

        while True:
            clear_screen()
            cls.display_config_menu()
            print(msg)
            choice = input("choose an option: ")
            match choice:
                case "1":
                    width = int(input("Choose the width: "))
                    MazeConfig.WIDTH = width
                    cls.maze.width = width
                    msg = f"WIDTH value set to {width}"
                case "2":
                    height = int(input("Choose the height: "))
                    MazeConfig.HEIGHT = height
                    cls.maze.height = height
                    msg = f"HEIGHT value set to {height}"
                case "3":
                    x = int(input("Choose the x: "))
                    y = int(input("Choose the y: "))
                    MazeConfig.ENTRY = (x, y)
                    cls.maze.entry = (x, y)
                    msg = f"ENTRY POINT set to [{x}, {y}]"
                case "4":
                    x = int(input("Choose the x: "))
                    y = int(input("Choose the y: "))
                    MazeConfig.EXIT = (x, y)
                    cls.maze.exit = (x, y)
                    msg = f"EXIT POINT set to [{x}, {y}]"
                case "5":
                    x = int(input("Choose the x: "))
                    y = int(input("Choose the y: "))
                    MazeConfig.STARTING_POINT = (x, y)
                    cls.maze.start = (x, y)
                    msg = f"STARTING POINT set to [{x}, {y}]"
                case "6":
                    cls.algorithm_menu()
                    msg = ''
                case "7":
                    cls.algorithm_menu()
                    msg = ''
                # case "8":
                #     seed = input("Choose the seed: ")
                #     MazeConfig.WIDTH = choice
                #     cls.maze.width = choice
                # case "9":
                #     choice = int(input("Choose the width: "))
                #     MazeConfig.WIDTH = choice
                #     cls.maze.width = choice
                case "q":
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

        msg = ''
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
                    msg = "You choose 'PRIM'. Overall, just another backtrack.\n"
                case "3":
                    MazeConfig.ALGORITHM = 'krusal'
                    cls.maze.algo = 'krusal'
                    msg = "You choose 'KRUSKAL'. Slow but steady.\n"
                case "q":
                    return
                case _:
                    msg = "error: invalid input\n"

    def display_color_menu():

        print()
        print()
        print("╔══════════════════════════════════════════╗")
        print("║  1) DEFAULT                              ║")
        print("║  2) OCEAN                                ║")
        print("║  3) FOREST                               ║")
        print("║  4) DESERT                               ║")
        print("║  5) VOLCANIC                             ║")
        print("║  6) CYBERPUNK                            ║")
        print("║  0) R4ND0M                               ║")
        print("║  q) Back to Menu                         ║")
        print("╚══════════════════════════════════════════╝")
        print()

    @classmethod
    def color_menu(cls):

        msg = ''
        while True:
            random = {
                "wall":    f"\033[48;2;{r(0, 254)};{r(0, 254)};{r(0, 254)}m  \033[0m",
                "path":    f"\033[48;2;{r(0, 254)};{r(0, 254)};{r(0, 254)}m  \033[0m",
                "ft":      f"\033[48;2;{r(0, 254)};{r(0, 254)};{r(0, 254)}m  \033[0m",
                "ft_wall": f"\033[48;2;{r(0, 254)};{r(0, 254)};{r(0, 254)}m  \033[0m",
                "start":   f"\033[48;2;{r(0, 254)};{r(0, 254)};{r(0, 254)}m  \033[0m",
                "end":     f"\033[48;2;{r(0, 254)};{r(0, 254)};{r(0, 254)}m  \033[0m",
                "solved":  f"\033[48;2;{r(0, 254)};{r(0, 254)};{r(0, 254)}m  \033[0m",
            }
            clear_screen()
            cls.maze.print_maze()
            cls.display_color_menu()
            print(msg)
            choice = input("choose your style: ")
            match choice:
                case "1":
                    cls.maze.theme = THEMES['default']
                    msg = "THEME set to 'DEFAULT'"
                case "2":
                    cls.maze.theme = THEMES['ocean']
                    msg = "THEME set to 'OCEAN'"
                case "3":
                    cls.maze.theme = THEMES['forest']
                    msg = "THEME set to 'FOREST'"
                case "4":
                    cls.maze.theme = THEMES['desert']
                    msg = "THEME set to 'DESERT'"
                case "5":
                    cls.maze.theme = THEMES['volcanic']
                    msg = "THEME set to 'VOLCANIC'"
                case "6":
                    cls.maze.theme = THEMES['cyberpunk']
                    msg = "THEME set to 'CYBERPUNK'"
                case "0":
                    cls.maze.theme = random
                    msg = "THEME set to 'RANDOM' (warning)"
                case "q":
                    return
                case _:
                    msg = "error: invalid input\n"

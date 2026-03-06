"""Module for menu management and program initialization."""

from mazegen.requirement_parser import Parser, MazeConfig
from mazegen.maze import Maze, clear_screen
from typing import Optional, Any, Dict
from pydantic import ValidationError
from mazegen.themes import THEMES
from random import seed, shuffle
from random import randint as r
import copy


class Menu:
    """Class representing the menu."""

    maze: Optional[Maze] = None
    model_config: Optional[MazeConfig] = None
    config: Optional[Dict[str, Any]] = None
    first: bool = True
    menu_chars: str = " ╦ ╩ ╔ ╗ ═ ╚ ╝ ║ ╠ ╣ ╬ "

    @classmethod
    def a_maze_init(cls, file: str) -> None:
        """Initialize the maze.

        Args:
            file: the configuration file needed for initialization.
        """
        try:
            cls.model_config = Parser.parse_config(file)
            cls.config = cls.model_config.model_dump()
            cls.maze = Maze(cls.model_config)
        except (EOFError, Exception) as e:
            print(repr(e))
            exit(1)

    @classmethod
    def output(cls) -> None:
        """Write an output file with maze representation and solution."""
        try:
            if cls.maze:
                with open(cls.maze.output, 'w') as f:
                    f.write(str(cls.maze) + "\n")
                    if (len(cls.maze.entry) == 2 and len(cls.maze.exit) == 2):
                        f.write(str(cls.maze.entry[0]) + "," +
                                str(cls.maze.entry[1]) + "\n")
                        f.write(str(cls.maze.exit[0]) + "," +
                                str(cls.maze.exit[1]) + "\n")
                        f.write(str(cls.maze.path) + "\n")
            else:
                print("[ERROR] "
                      "MAZE OBJ NOT INITIALIZED")
        except Exception as e:
            print(str(e))

    @classmethod
    def maze_generator(cls) -> None:
        """Initialize, generate, print, solve the maze."""
        if cls.maze:
            cls.maze.init_maze()
            cls.maze.create_maze()
            cls.maze.print_maze()
            if not cls.maze.perfect and cls.maze.algo != 'nirugger':
                cls.maze.make_it_wrong()
            cls.maze.never_been_there()
            cls.maze.breadth_first_search_solver()
            cls.maze.assign_solution()
            cls.output()
            if cls.maze.error_message:
                print(cls.maze.error_message)
        else:
            print("[ERROR] "
                  "MAZE OBJ NOT INITIALIZED")
            exit(1)

    @classmethod
    def display_main_menu(cls) -> None:
        """Display of the main menu (first time launching a_maze_ing)."""
        print("\n" * 10)
        print("    ╔═════════════════════════════════════════════════╗    ")
        print("    ║                    W31C0M3 2                    ║    ")
        print("    ║    ▗▄▖ ▗▖  ▗▖ ▗▄▖ ▗▄▄▄▄▖▗▄▄▄▖▗▄▄▄▖▗▖  ▗▖ ▗▄▄▖   ║    ")
        print("    ║   ▐▌ ▐▌▐▛▚▞▜▌▐▌ ▐▌   ▗▞▘▐▌     █  ▐▛▚▖▐▌▐▌      ║    ")
        print("    ║   ▐▛▀▜▌▐▌  ▐▌▐▛▀▜▌ ▗▞▘  ▐▛▀▀▘  █  ▐▌ ▝▜▌▐▌▝▜▌   ║    ")
        print("    ║   ▐▌ ▐▌▐▌  ▐▌▐▌ ▐▌▐▙▄▄▄▖▐▙▄▄▖▗▄█▄▖▐▌  ▐▌▝▚▄▞▘   ║    ")
        print("    ║                                                 ║    ")
        print("    ║            a  wond_err_full  project            ║    ")
        print("    ╚═════════════════════════════════════════════════╝    ")
        print("                                                           ")
        print("    ╔══════════════════════════╗╔═════════════════════╗    ")
        print("    ║  1: Generate Maze        ║║                     ║    ")
        print("    ║  2: Select Algorithm     ║║   coded by:         ║    ")
        print("    ║  3: Configure Maze       ║║                     ║    ")
        print("    ║  4: Colors!              ║║      tvanni &       ║    ")
        print("    ║  5: Animation  [ON/OFF]  ║║      nirugger       ║    ")
        print("    ║  6: Solution   [ON/OFF]  ║║                     ║    ")
        print("    ║                          ║║  &: special guests  ║    ")
        print("    ║  q: Exit                 ║║                     ║    ")
        print("    ╚══════════════════════════╝╚═════════════════════╝    ")
        print("\n" * 3)

    @classmethod
    def display_maze_menu(cls) -> None:
        """Display of the main menu (from the second time on)."""
        print("    ╔═════════════════════════════════════════════════╗    ")
        print("    ║                    THAT  WAS                    ║    ")
        print("    ║    ▗▄▖ ▗▖  ▗▖ ▗▄▖ ▗▄▄▄▄▖▗▄▄▄▖▗▄▄▄▖▗▖  ▗▖ ▗▄▄▖   ║    ")
        print("    ║   ▐▌ ▐▌▐▛▚▞▜▌▐▌ ▐▌   ▗▞▘▐▌     █  ▐▛▚▖▐▌▐▌      ║    ")
        print("    ║   ▐▛▀▜▌▐▌  ▐▌▐▛▀▜▌ ▗▞▘  ▐▛▀▀▘  █  ▐▌ ▝▜▌▐▌▝▜▌   ║    ")
        print("    ║   ▐▌ ▐▌▐▌  ▐▌▐▌ ▐▌▐▙▄▄▄▖▐▙▄▄▖▗▄█▄▖▐▌  ▐▌▝▚▄▞▘   ║    ")
        print("    ║                                                 ║    ")
        print("    ║             HOW ABOUT ANOTHER TRY ?             ║    ")
        print("    ╚═════════════════════════════════════════════════╝    ")
        print("                                                           ")
        print("    ╔══════════════════════════╗╔═════════════════════╗    ")
        print("    ║  1: Generate Maze        ║║                     ║    ")
        print("    ║  2: Select Algorithm     ║║   coded by:         ║    ")
        print("    ║  3: Configure Maze       ║║                     ║    ")
        print("    ║  4: Colors!              ║║      tvanni &       ║    ")
        print("    ║  5: Animation  [ON/OFF]  ║║      nirugger       ║    ")
        print("    ║  6: Solution   [ON/OFF]  ║║                     ║    ")
        print("    ║                          ║║  &: special guests  ║    ")
        print("    ║  q: Exit                 ║║                     ║    ")
        print("    ╚══════════════════════════╝╚═════════════════════╝    ")

    @classmethod
    def display_guest_menu(cls) -> None:
        """Display of the guest menu - because friendship is awesome."""
        fbertozz: str = (
            "                                                      \n"
            "              for topology lessons                    \n"
            "                 late night talks                     \n"
            "               & for making it obvious                \n"
            "      ▄▄ ▄▄                                           \n"
            "     ██  ██                 ██                        \n"
            "    ▀██▀ ████▄ ▄█▀█▄ ████▄ ▀██▀▀ ▄███▄ ▀▀▀██ ▀▀▀██    \n"
            "     ██  ██ ██ ██▄█▀ ██ ▀▀  ██   ██ ██   ▄█▀   ▄█▀    \n"
            "     ██  ████▀ ▀█▄▄▄ ██     ██   ▀███▀ ▄██▄▄ ▄██▄▄    \n"
            "                                                      \n"
            "      (also, for his deep hatred for recursions)      \n"
            "                                                      \n"
            )

        aflorea: str = (
            "                                                      \n"
            "                 for algorithm magic                  \n"
            "  powerful optimization strategies (that we ignored)  \n"
            "     & for doing everything everywhere all at once    \n"
            "              ▄▄ ▄▄                                   \n"
            "             ██  ██                                   \n"
            "       ▀▀█▄ ▀██▀ ██ ▄███▄ ████▄ ▄█▀█▄  ▀▀█▄           \n"
            "      ▄█▀██  ██  ██ ██ ██ ██ ▀▀ ██▄█▀ ▄█▀██           \n"
            "      ▀█▄██  ██  ██ ▀███▀ ██    ▀█▄▄▄ ▀█▄██           \n"
            "                                                      \n"
            "         (and a ton of other important stuff)         \n"
            "                                                      \n"
        )

        guests = [aflorea, fbertozz]
        shuffle(guests)
        clear_screen()
        print("\n" * 3)

        for guest in guests:
            print(guest)
            print("\n" * 3)

        print("press ENTER for return")
        choice = input()
        match choice:
            case _:
                return

    @classmethod
    def main_menu(cls) -> None:
        """Display the main menu and waits for user input."""
        msg = "\n"

        while True:
            if cls.first:
                clear_screen()
                cls.display_main_menu()
            else:
                if cls.maze:
                    cls.maze.print_maze()
                    print(cls.maze.error_message)
                    cls.display_maze_menu()

            print(msg, end='')
            quest = "" if cls.first else "Re-"
            choice = input(f"{quest}Choose your path: ").strip().lower()
            match choice:

                case "1":
                    try:
                        cls.first = False
                        cls.maze_generator()
                        msg = "\n"
                    except ValueError as e:
                        msg = e.args[0]

                case "2":
                    cls.algorithm_menu()
                    msg = "\n"

                case "3":
                    try:
                        cls.config_menu()
                        msg = "\n"
                    except ValidationError as e:
                        for err in e.errors():
                            msg += err['msg'] + "\n"

                case "4":
                    cls.color_menu()
                    clear_screen()
                    msg = "\n"

                case "5":
                    if cls.maze:
                        cls.maze.animation = not cls.maze.animation
                        msg = ("ANIMATION set to "
                               f"{cls.maze.animation}\n")

                case "6":
                    if cls.maze:
                        cls.maze.solution = not cls.maze.solution
                        state = "VISIBLE" if cls.maze.solution else "INVISIBLE"
                        msg = f"SOLUTION set to '{state}'\n"

                case "&":
                    cls.display_guest_menu()
                    msg = "\n"

                case "q":
                    choice = input("Are you sure you want to quit? [y/n]")
                    match choice:
                        case "y":
                            cls.closure()
                        case _:
                            msg = "\n"

                case _:
                    msg = "\n"

    @staticmethod
    def closure() -> None:
        """Close the program gracefully with a bit of salt."""
        print("\n" * 3)
        print("“A labyrinth is not a place to be lost, "
              "but a path to be found.”"
              "\n  — Anonymous")
        print("\n")
        print("“A labyrinth is not a maze, though.”"
              "\n  — nirugger")
        print("\n" * 6)
        exit(1)

    @staticmethod
    def display_config_menu() -> None:
        """Display of the configuration menu."""
        print("\n" * 10)
        print("    ╔══════════════════════════════════════════╗    ")
        print("    ║  1: WIDTH                                ║    ")
        print("    ║  2: HEIGHT                               ║    ")
        print("    ║  3: ENTRY                                ║    ")
        print("    ║  4: EXIT                                 ║    ")
        print("    ║  5: STARTING POINT                       ║    ")
        print("    ║  6: PERFECT [ON/OFF]                     ║    ")
        print("    ║  7:                                      ║    ")
        print("    ║  8: SEED                                 ║    ")
        print("    ║  9: RESET                                ║    ")
        print("    ║                                          ║    ")
        print("    ║  q: back to Main Menu                    ║    ")
        print("    ╚══════════════════════════════════════════╝    ")
        print()

    @staticmethod
    def display_error_menu() -> None:
        """Display of the error menu."""
        print("\n" * 10)
        print("    ╔═════════════════════════════════════════════════╗    ")
        print("    ║  !!!  WARNING  !!!  WARNING  !!!  WARNING  !!!  ║    ")
        print("    ║                                                 ║    ")
        print("    ║  ---------------------------------------------  ║    ")
        print("    ║   YOUR  CONFIGURATION  HAS  BEEN  INVALIDATED   ║    ")
        print("    ║  ---------------------------------------------  ║    ")
        print("    ║                                                 ║    ")
        print("    ║  !!!  WARNING  !!!  WARNING  !!!  WARNING  !!!  ║    ")
        print("    ╚═════════════════════════════════════════════════╝    ")
        print()

    @classmethod
    def config_menu(cls) -> None:
        """Display config menu and waits for user inputs."""
        if cls.maze:

            mod_config: dict[str, Any] = {
                "WIDTH": cls.maze.width,
                "HEIGHT": cls.maze.height,
                "ENTRY": cls.maze.entry,
                "EXIT": cls.maze.exit,
                "START": cls.maze.entry,
                "PERFECT": cls.maze.perfect,
                "ALGORITHM": cls.maze.algo,
                "OUTPUT_FILE": cls.maze.output
                }

            msg = "\n"
            while True:
                clear_screen()
                cls.display_config_menu()
                print(msg, end='')

                choice = input("Choose an option: ")
                match choice:

                    case "1":
                        try:
                            width = int(input("Choose the width of the maze "
                                        "(>=2, <=41): "))
                            if 1 < width < 42:
                                mod_config['WIDTH'] = width
                                msg = f"WIDTH value set to {width}\n"
                            else:
                                msg = ("WIDTH value unacceptable "
                                       "(2 <= WIDTH <= 41)\n")

                        except Exception:
                            msg = "[ERROR]: WIDTH has to be a valid number.\n"

                    case "2":
                        try:
                            height = int(input("Choose the height of the maze "
                                         "(>=2, <=21): "))
                            if 1 < height < 22:
                                mod_config['HEIGHT'] = height
                                msg = f"HEIGHT value set to {height}\n"
                            else:
                                msg = ("HEIGHT value unacceptable "
                                       "(2 <= HEIGHT <= 21)\n")

                        except Exception:
                            msg = "[ERROR]: HEIGHT has to be a valid number.\n"

                    case "3":
                        try:
                            x = int(input("Choose the x (>=0): "))
                            y = int(input("Choose the y (>=0): "))
                            if x >= 0 and y >= 0:
                                mod_config['ENTRY'] = f"{x},{y}"
                                msg = f"ENTRY set to ({x}, {y})\n"
                            else:
                                msg = "ENTRY value unacceptable (x,y >= 0)\n"
                        except Exception:
                            msg = "[ERROR]: HEIGHT has to be a valid number.\n"

                    case "4":
                        try:
                            x = int(input("Choose the x (>=0): "))
                            y = int(input("Choose the y (>=0): "))
                            if x >= 0 and y >= 0:
                                mod_config['EXIT'] = f"{x},{y}"
                                msg = f"EXIT set to ({x}, {y})\n"
                            else:
                                msg = "EXIT value unacceptable (x,y >= 0)\n"
                        except Exception:
                            msg = "[ERROR]: x, y have to be valid numbers.\n"

                    case "5":
                        try:
                            x = int(input("Choose the x (>=0): "))
                            y = int(input("Choose the y (>=0): "))
                            if x >= 0 and y >= 0:
                                mod_config['START'] = f"{x},{y}"
                                msg = f"STARTING POINT set to ({x}, {y})\n"
                            else:
                                msg = ("STARTING POINT value unacceptable "
                                       "(x,y >= 0)\n")
                        except Exception:
                            msg = "[ERROR]: x, y have to be valid numbers.\n"

                    case "6":
                        mod_config['PERFECT'] = not mod_config['PERFECT']
                        msg = f"PERFECT set to '{mod_config['PERFECT']}'\n"

                    case "7":
                        msg = "\n"

                    case "8":
                        new = input("Choose the seed "
                                    "(leave empty for RANDOM): ")
                        if not new:
                            seed()
                            cls.maze.random = True
                            new = Maze.get_random_seed()
                            msg = ("SEED set to RANDOM\n"
                                   f"for next run will be: << {new} >>'\n")
                        else:
                            cls.maze.random = False
                            msg = f"SEED set to << {new} >>\n"
                        cls.maze.seed = new

                    case "9":
                        if cls.config:
                            mod_config = copy.deepcopy(cls.config)
                            msg = "Configuration set to 'DEFAULT'\n"
                        else:
                            msg = "[ERROR] CONFIGURATION FILE not found\n"
                            print(msg)
                            exit(1)

                    case "q":

                        try:
                            mod_config = MazeConfig(**mod_config).model_dump()
                            cls.maze.width = mod_config['WIDTH']
                            cls.maze.height = mod_config['HEIGHT']
                            cls.maze.entry = mod_config['ENTRY']
                            cls.maze.exit = mod_config['EXIT']
                            cls.maze.start = mod_config['START']
                            cls.maze.perfect = mod_config['PERFECT']

                            coord = cls.maze.entry
                            if cls.maze.maze[coord[1]][coord[0]].visited == 42:
                                raise ValueError("[ERROR]: "
                                                 "ENTRY inside the 42!\n")

                            coord = cls.maze.exit
                            if cls.maze.maze[coord[1]][coord[0]].visited == 42:
                                raise ValueError("[ERROR]: "
                                                 "EXIT inside the 42!\n")

                            coord = cls.maze.start
                            if cls.maze.maze[coord[1]][coord[0]].visited == 42:
                                raise ValueError("[ERROR]: "
                                                 "STARTING POINT inside the "
                                                 "42!\n")

                            msg = "\n"
                            return

                        except (ValidationError, ValueError) as e:

                            while True:
                                clear_screen()
                                cls.display_error_menu()
                                print("The following error(s) "
                                      "have been detected:\n")

                                if type(e).__name__ == 'ValueError':
                                    print(str(e))

                                else:
                                    i = 1
                                    for err in e.errors():
                                        print(f"{i}) {err['msg']}")
                                        i += 1
                                        print()

                                choice = input("1: Reconfigure\n"
                                               "2: Go back to menu\n")
                                match choice:
                                    case "1":
                                        msg = "\n"
                                        break
                                    case "2":
                                        return
                                    case _:
                                        continue
                            continue

                    case "42":
                        cls.maze.two_forty = not cls.maze.two_forty
                        msg = "\n"

                    case _:
                        msg = "\n"

    @staticmethod
    def display_algorithm_menu() -> None:
        """Display of the algorithm menu."""
        print("\n" * 10)
        print("    ╔══════════════════════════════════════════╗    ")
        print("    ║  1: BACKTRACK                            ║    ")
        print("    ║  2: PRIM                                 ║    ")
        print("    ║  3: ELLER                                ║    ")
        print("    ║  4: KRUSKAL                              ║    ")
        print("    ║  5: ALDOUS-BRODER                        ║    ")
        print("    ║  6: WILSON                               ║    ")
        print("    ║  7: RECURSIVE DIVISION                   ║    ")
        print("    ║  8: HUNT AND KILL                        ║    ")
        print("    ║  9: BINARY TREE                          ║    ")
        print("    ║  0: NIRUGGER                             ║    ")
        print("    ║                                          ║    ")
        print("    ║  q: back to configuration menu           ║    ")
        print("    ╚══════════════════════════════════════════╝    ")
        print()

    @classmethod
    def algorithm_menu(cls) -> None:
        """Display the algorithm menu and wait for user input."""
        msg = "\n"
        while True:
            clear_screen()
            cls.display_algorithm_menu()
            print(msg)

            choice = input("Choose an option: ")
            if cls.maze:

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
                        MazeConfig.ALGORITHM = 'eller'
                        cls.maze.algo = 'eller'
                        msg = "You choose 'ELLER'. IT WON'T WORK!!.\n"

                    case "4":
                        MazeConfig.ALGORITHM = 'kruskal'
                        cls.maze.algo = 'kruskal'
                        msg = "You choose 'KRUSKAL'. Slow but steady.\n"

                    case "4":
                        MazeConfig.ALGORITHM = 'eller'
                        cls.maze.algo = 'eller'
                        msg = "You choose 'ELLER'. IT WON'T WORK!!.\n"

                    case "5":
                        MazeConfig.ALGORITHM = 'aldous_broder'
                        cls.maze.algo = 'aldous_broder'
                        msg = "You choose 'ALDOUS-BRODER'. Prepare to wait.\n"

                    case "6":
                        MazeConfig.ALGORITHM = 'wilson'
                        cls.maze.algo = 'wilson'
                        msg = "You choose 'WILSON'. .\n"

                    case "7":
                        MazeConfig.ALGORITHM = 'recursive_division'
                        cls.maze.algo = 'recursive_division'
                        msg = "You choose 'RECURSIVE DIVISION'. EZ.\n"

                    case "8":
                        MazeConfig.ALGORITHM = 'hunt_and_kill'
                        cls.maze.algo = 'hunt_and_kill'
                        msg = "You choose 'HUNT AND KILL'. In progress.\n"

                    case "9":
                        MazeConfig.ALGORITHM = 'binary_tree'
                        cls.maze.algo = 'binary_tree'
                        msg = "You choose 'BINARY TREE'. Not that amazing.\n"

                    case "0":
                        MazeConfig.ALGORITHM = 'nirugger'
                        cls.maze.algo = 'nirugger'
                        msg = "You choose 'NIRUGGER'. I'm flattered!\n"

                    case "q":
                        return

                    case _:
                        msg = "\n"

    @staticmethod
    def display_color_menu() -> None:
        """Display of the color menu."""
        print("                                             ")
        print("╔═════════════════════╦═════════════════════╗")
        print("║  1: DEFAULT         ║  3: R4ND0M          ║")
        print("║  2: COLORBLIND      ║  4: CHOOSE YOUR     ║")
        print("║     FRIENDLY :)     ║     COLORS!!!       ║")
        print("║                     ║                     ║")
        print("╠═════════════════════╩═════════════════════╣")
        print("║  +: MORE COLORS        q: Back to Menu    ║")
        print("╚═══════════════════════════════════════════╝")

    @classmethod
    def color_menu(cls) -> None:
        """Display the color menu and wait for user input."""
        seed()
        msg = ''
        while True:

            random = {
                "wall":
                    f"\033[48;2;{r(0, 255)};{r(0, 255)};{r(0, 255)}m  \033[0m",
                "path":
                    f"\033[48;2;{r(0, 255)};{r(0, 255)};{r(0, 255)}m  \033[0m",
                "ft":
                    f"\033[48;2;{r(0, 255)};{r(0, 255)};{r(0, 255)}m  \033[0m",
                "ft_wall":
                    f"\033[48;2;{r(0, 255)};{r(0, 255)};{r(0, 255)}m  \033[0m",
                "entry":
                    f"\033[48;2;{r(0, 255)};{r(0, 255)};{r(0, 255)}m  \033[0m",
                "exit":
                    f"\033[48;2;{r(0, 255)};{r(0, 255)};{r(0, 255)}m  \033[0m",
                "solved":
                    f"\033[48;2;{r(0, 255)};{r(0, 255)};{r(0, 255)}m  \033[0m"
            }
            if cls.maze:

                clear_screen()
                cls.maze.print_maze()
                cls.display_color_menu()
                print(msg)
                choice = input("Choose your style: ")
                match choice:

                    case "1":
                        cls.maze.theme = THEMES['default']
                        msg = "THEME set to 'DEFAULT'\n"

                    case "2":
                        cls.maze.theme = THEMES['colorblind_friendly']
                        msg = "THEME set to 'COLORBLIND :)'\n"

                    case "3":
                        cls.maze.theme = random
                        msg = "THEME set to 'R4ND0M'\n"

                    case "4":
                        cls.personalized_color_menu()
                        msg = "\n"

                    case "+":
                        cls.more_color_menu()
                        return

                    case "q":
                        seed(cls.maze.seed)
                        return

                    case _:
                        msg = "\n"

    @staticmethod
    def display_more_color_menu() -> None:
        """Display of the more color menu."""
        print()
        print("╔════════════════════════════╦═════════════════════╗")
        print("║  1: IRIDE     (mpagano)    ║  a: OCEAN           ║")
        print("║  2: BAUGIGI   (alfiorav)   ║  b: FOREST          ║")
        print("║  3: NICOLAS   (ndavidso)   ║  c: DESERT          ║")
        print("║  4: EFARISTO  (mcicconi)   ║  d: ARCTIC          ║")
        print("║  5: FIRENZE   (acentron)   ║  e: VOLCANIC        ║")
        print("║  6: LIFE      (gbotti)     ║  f: CYBERPUNK       ║")
        print("║  7: LIXI      (lmongili)   ║  g: SPACE           ║")
        print("║  8:                        ║  h: FREEDOM         ║")
        print("║  9:                        ║  i:                 ║")
        print("║  0:                        ║  j: COLORBLIND      ║")
        print("║                            ║     UN-FRIENDLY (:  ║")
        print("║                            ║                     ║")
        print("╠════════════════════════════╩═════════════════════╣")
        print("║  -: LESS COLORS               q: Back to Menu    ║")
        print("╚══════════════════════════════════════════════════╝")

    @classmethod
    def more_color_menu(cls) -> None:
        """Display the more color menu and wait for user input."""
        seed()
        msg = ''
        while True:

            if cls.maze:

                clear_screen()
                cls.maze.print_maze()
                cls.display_more_color_menu()
                print(msg)
                choice = input("Choose your style: ")
                match choice:

                    case "1":
                        cls.maze.theme = THEMES['iride']
                        msg = "THEME set to 'IRIDE'\n"

                    case "2":
                        cls.maze.theme = THEMES['baugigi']
                        msg = "THEME set to 'BAUGIGI'\n"

                    case "3":
                        cls.maze.theme = THEMES['baugigi']
                        msg = "THEME set to 'BAUGIGI'\n"

                    case "4":
                        cls.maze.theme = THEMES['efaristo']
                        msg = "THEME set to 'EFARISTO'\n"

                    case "5":
                        cls.maze.theme = THEMES['firenze']
                        msg = "THEME set to 'FIRENZE'\n"

                    case "6":
                        cls.maze.theme = THEMES['life_palette']
                        msg = "THEME set to 'LIFE'\n"

                    case "7":
                        cls.maze.theme = THEMES['lixi']
                        msg = "THEME set to 'LIXI'\n"

                    case "8":
                        pass

                    case "9":
                        pass

                    case "0":
                        pass

                    case "a":
                        cls.maze.theme = THEMES['ocean']
                        msg = "THEME set to 'OCEAN'\n"

                    case "b":
                        cls.maze.theme = THEMES['forest']
                        msg = "THEME set to 'FOREST'\n"

                    case "c":
                        cls.maze.theme = THEMES['desert']
                        msg = "THEME set to 'DESERT'\n"

                    case "d":
                        cls.maze.theme = THEMES['arctic']
                        msg = "THEME set to 'ARCTIC'\n"

                    case "e":
                        cls.maze.theme = THEMES['volcanic']
                        msg = "THEME set to 'VOLCANIC'\n"

                    case "f":
                        cls.maze.theme = THEMES['cyberpunk']
                        msg = "THEME set to 'CYBERPUNK'\n"

                    case "g":
                        cls.maze.theme = THEMES['space']
                        msg = "THEME set to 'SPACE'\n"

                    case "h":
                        cls.maze.theme = THEMES['freedom']
                        msg = "THEME set to 'FREEDOM'\n"

                    case "i":
                        pass

                    case "j":
                        cls.maze.theme = THEMES['colorblind_unfriendly']
                        msg = "THEME set to 'COLORBLIND UN-FRIENDLY (:'\n"

                    case "-":
                        cls.color_menu()
                        return

                    case "q":
                        seed(cls.maze.seed)
                        return

                    case _:
                        msg = "\n"

    @staticmethod
    def display_personalized_color_menu() -> None:
        """Display of the personalized color menu."""
        print()
        print("╔══════════════════════════════════════════╗")
        print("║  1: WALL                                 ║")
        print("║  2: PATH          [VALID SYNTAX]: R;G;B  ║")
        print("║  3: FORTYTWO                             ║")
        print("║  4: ENTRY POINT           0 <= R <= 255  ║")
        print("║  5: EXIT POINT            0 <= G <= 255  ║")
        print("║  6: SOLUTION              0 <= B <= 255  ║")
        print("║                                          ║")
        print("║  0: RESET                                ║")
        print("║  q: Back to Color Menu                   ║")
        print("╚══════════════════════════════════════════╝")
        print()

    @staticmethod
    def validate_color(color: str) -> None:
        """Validate the color

        Args:
            color: the color to validate
        """
        parts = color.split(';')
        if len(parts) != 3 or color[len(color) - 1] == ';':
            raise ValueError("[ERROR]: "
                             "invalid SYNTAX")
        for part in parts:
            value = int(part)
            if not 0 <= value <= 255:
                raise ValueError("[ERROR]: "
                                 "COLOR VALUE must be between 0 and 255")

    @classmethod
    def personalized_color_menu(cls) -> None:
        """Display the personalized color menu and wait for user input."""
        msg = ''
        default = cls.maze.theme
        modified = copy.deepcopy(cls.maze.theme)
        while True:

            if cls.maze:

                clear_screen()
                cls.maze.print_maze()
                cls.display_personalized_color_menu()
                print(msg)
                choice = input("Choose the element you want to color: ")
                match choice:

                    case "1":
                        wall = input("Set WALL color: ")
                        try:
                            cls.validate_color(wall)
                            color_str = f"\033[48;2;{wall}m  \033[0m"
                            modified['wall'] = color_str
                            cls.maze.theme = modified
                            msg = "WALL color set'\n"
                        except Exception as e:
                            msg = str(e) + "\n"

                    case "2":
                        path = input("Set PATH color: ")
                        try:
                            cls.validate_color(path)
                            color_str = f"\033[48;2;{path}m  \033[0m"
                            modified['path'] = color_str
                            cls.maze.theme = modified
                            msg = "PATH color set'\n"
                        except Exception as e:
                            msg = str(e) + "\n"

                    case "3":
                        ft = input("Set FORTYTWO color: ")
                        try:
                            cls.validate_color(ft)
                            color_str = f"\033[48;2;{ft}m  \033[0m"
                            modified['ft'] = color_str
                            modified['ft_wall'] = color_str
                            cls.maze.theme = modified
                            msg = "FORTYTWO color set'\n"

                        except Exception as e:
                            msg = str(e) + "\n"

                    case "4":
                        entry = input("Set ENTRY color: ")
                        try:
                            cls.validate_color(entry)
                            color_str = f"\033[48;2;{entry}m  \033[0m"
                            modified['entry'] = color_str
                            cls.maze.theme = modified
                            msg = "ENTRY color set'\n"
                        except Exception as e:
                            msg = str(e) + "\n"

                    case "5":
                        exit = input("Set EXIT color: ")
                        try:
                            cls.validate_color(exit)
                            color_str = f"\033[48;2;{exit}m  \033[0m"
                            modified['exit'] = color_str
                            cls.maze.theme = modified
                            msg = "EXIT color set'\n"
                        except Exception as e:
                            msg = str(e) + "\n"

                    case "6":
                        solution = input("Set SOLUTION color: ")
                        try:
                            cls.validate_color(solution)
                            color_str = f"\033[48;2;{solution}m  \033[0m"
                            modified['solved'] = color_str
                            cls.maze.theme = modified
                            msg = "SOLUTION color set'\n"
                        except Exception as e:
                            msg = str(e) + "\n"

                    case "0":
                        cls.maze.theme = default
                        msg = "CHANGES UNDONE\n"

                    case "q":
                        return

                    case _:
                        msg = "\n"

from src.maze import Maze
from src.maze import clear_screen
from src.requirement_parser import Parser
from typing import Optional


class Menu:

    maze: Optional[Maze] = None

    @classmethod
    def maze_generator(cls, file: str) -> None:
        try:
            config = Parser.parse_config(file)
            cls.maze = Maze(config)
        except Exception as e:
            print(repr(e))
            exit(1)
        try:
            cls.maze.create_maze()
            cls.maze.print_maze()
            cls.maze.never_been_there()
            cls.maze.backtrack_solver(cls.maze.entry[0], cls.maze.entry[1], path="")
            cls.maze.assign_solution()
            cls.maze.print_maze()
            # print(cls.maze)
            # print(f"\n\n{cls.maze.path}\n\n")
            if cls.maze.error_message:
                print(cls.maze.error_message)
        except Exception as e:
            print(str(e))

    @classmethod
    def display_main_menu(cls) -> None:
        print("\n\n\n")
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

    @classmethod
    def menu(cls, file: str) -> None:

        clear_screen()

        while True:
            cls.display_main_menu()
            choice = input("Choose your path: ").strip().lower()
            if choice == "1":
                pass
            if choice == "2":
                pass
            if choice == "3":
                pass
            if choice == "q":
                print("“A labyrinth is not a place to be lost, "
                      "but a path to be found.”"
                      "\n  — Anonymous")
                print("\n\n")
                print("“A labyrinth is not a maze though"
                      "\n  — nirugger")

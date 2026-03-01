from src.maze import Maze
from src.maze import clear_screen
from src.requirement_parser import Parser
from typing import Optional
from src.themes import THEMES
import subprocess


class Menu:

    maze: Optional[Maze] = None
    current_theme: dict = THEMES['default']

    @classmethod
    def maze_generator(cls, file: str) -> None:
        try:
            config = Parser.parse_config(file)
            cls.maze = Maze(config)
        except Exception as e:
            print(repr(e))
            exit(1)
        try:
            cls.maze.theme = cls.current_theme

            cls.maze.create_maze()
            cls.maze.print_maze()
            cls.maze.never_been_there()
            cls.maze.backtrack_solver(cls.maze.entry[0],
                                      cls.maze.entry[1],
                                      path="")
            cls.maze.assign_solution()
            cls.maze.print_maze()
            # print(cls.maze)
            # print(f"\n\n{cls.maze.path}\n\n")
            if cls.maze.error_message:
                print(cls.maze.error_message)
            cls.maze_menu(file)

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
    def main_menu(cls, file: str) -> None:

        # clear_screen()
        subprocess.run("clear", shell=True)
        while True:
            subprocess.run("clear", shell=True)
            cls.display_main_menu()
            choice = input("Choose your path: ").strip().lower()
            if choice == "1":
                cls.maze_generator(file)
            elif choice == "2":
                print("Still to be implemented!")
            elif choice == "3":
                print("Still to be implemented!")
            elif choice == "q":
                print("\n" * 3)
                print("“A labyrinth is not a place to be lost, "
                      "but a path to be found.”"
                      "\n  — Anonymous")
                print("\n")
                print("“A labyrinth is not a maze, though.”"
                      "\n  — nirugger")
                print("\n" * 6)
                exit(1)

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
            print("║  1) Generate Maze        ║║   coded by:         ║")
            print("║  2) Configure Maze       ║║      tvanni &       ║")
            print("║  3) Colors!              ║║      nirugger       ║")
            print("║  q) Exit                 ║║  (aka Tom & Gerru)  ║")
            print("╚══════════════════════════╝╚═════════════════════╝")
            print()


    @classmethod
    def maze_menu(cls, file: str) -> None:

        while True:
            cls.display_maze_menu()
            choice = input("Re-choose your path: ").strip().lower()
            if choice == "1":
                cls.maze_generator(file)
            elif choice == "2":
                print("Still to be implemented!")
            elif choice == "3":
                print("Still to be implemented!")
            elif choice == "q":
                print("\n" * 3)
                print("“A labyrinth is not a place to be lost, "
                      "but a path to be found.”"
                      "\n  — Anonymous")
                print("\n")
                print("“A labyrinth is not a maze, though.”"
                      "\n  — nirugger")
                print("\n" * 6)
                exit(1)

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
            # cls.maze.print_maze()
            # print(cls.maze)
            # print(f"\n\n{cls.maze.path}\n\n")
            if cls.maze.error_message:
                print(cls.maze.error_message)
        except Exception as e:
            print(str(e))

from src.requirement_parser import Parser
from src.maze import Maze
from src.cell import Cell


def main():

    try:
        d = Parser.parse_config("src/config.txt")
        print(d)
    except Exception as e:
        print(repr(e))
        return

    maze = Maze(d)
    print(maze)


if __name__ == "__main__":
    main()

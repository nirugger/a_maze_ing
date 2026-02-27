from src.requirement_parser import Parser
from src.maze import Maze
# from src.cell import Direction
# from src.cell import Cell


def main():

    try:
        d = Parser.parse_config("src/config.txt")
    except Exception as e:
        print(repr(e))
        return

    maze = Maze(d)
    # try:
    maze.create_maze(maze.entry[0], maze.entry[1])
    # except Exception as e:
    #     print(repr(e))
    print(maze)
    maze.print_maze()


if __name__ == "__main__":
    main()

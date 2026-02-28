from src.requirement_parser import Parser
from src.maze import Maze
from src.cell import Cell
# from src.cell import Direction
# from src.cell import Cell


def main():

    try:
        d = Parser.parse_config("src/config.txt")
    except Exception as e:
        print(repr(e))
        return

    maze = Maze(d)
    try:
        maze.backtrack(maze.entry[0], maze.entry[1], path="")
        # maze.prim(maze.entry[0], maze.entry[1], frontiera=[(maze.entry[0], maze.entry[1])])
    except Exception as e:
        print(repr(e))

    print(maze)
    print(f"\n\n{maze.path}\n\n")
    maze.print_maze()


    # path = "ABCDEFG"
    # print(path)
    # newpath = path[:-0]
    # print(newpath)
    # newpath = path[:-4]
    # print(newpath)

if __name__ == "__main__":
    main()

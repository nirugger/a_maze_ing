from src.menu import Menu
from src.cell import Cell
import sys
# from src.cell import Direction
# from src.cell import Cell


def main():

    sys.setrecursionlimit(2000)
    Menu.maze_generator(sys.argv[1])
    # while True:


if __name__ == "__main__":
    main()

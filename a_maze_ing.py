from src.menu import Menu
from src.cell import Cell
import sys
# from src.cell import Direction
# from src.cell import Cell


def main():

    sys.setrecursionlimit(2000)
    Menu.main_menu("src/config.txt")
    # Menu.maze_generator(sys.argv[1])


if __name__ == "__main__":
    main()

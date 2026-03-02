from src.menu import Menu
from src.cell import Cell
import sys
# from src.cell import Direction
# from src.cell import Cell


def main():

    sys.setrecursionlimit(2000)
    Menu.amazinit("src/config.txt")
    Menu.main_menu()
    # Menu.maze_generator(sys.argv[1])


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print(Menu.closure())

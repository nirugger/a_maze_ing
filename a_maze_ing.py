from mazegen.menu import Menu
import sys


def main():

    sys.setrecursionlimit(2000)
    Menu.a_maze_init("mazegen/config.txt")
    Menu.main_menu()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print(Menu.closure())

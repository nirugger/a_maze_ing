from src.requirement_parser import Parser
from src.maze import Maze


def main():

    try:
        d = Parser.parse_config("src/config.txt")
        print(d)
    except Exception as e:
        print(repr(e))
        return

    maze = Maze(d)



if __name__ == "__main__":
    main()

class Maze:

    def __init__(self, config: dict[str, any]) -> None:

        self.width: int = config["WIDTH"]
        self.height: int = config["HEIGHT"]
        self.entry: tuple[int] = config["ENTRY"]
        self.exit: tuple[int] = config["EXIT"]
        self.output: str = config["OUTPUT_FILE"]
        self.perfect: bool = config["PERFECT"]

    def create_maze():
        pass

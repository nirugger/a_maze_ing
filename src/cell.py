from enum import Enum


class Direction(Enum):
    """Enum class used for walls direction
    Each number represents a cardinal direction, and also a bit
    value from LSB (0) to MSB (3)
    """

    north = 1
    east = 2
    south = 4
    west = 8


class Cell:
    """Class of a maze cell, with walls represented by an hexadecimal number
    Initialized as a full-closed cell (1111)
    """

    def __init__(self) -> None:
        """Initializes the cell as a full-closed cell (1111)"""

        self.walls = 0xf
        self.is_entry = False
        self.is_exit = False
        self.is_solved = False
        self.visited = 0

    def is_closed(self, direction: Direction) -> bool:
        """Checks if a specific wall is closed
        Args:
            direction (Direction): The wall to be checked
        Returns:
            1 (truthy) if the wall is closed
            0 (falsy) if the wall is open
        """

        return self.walls & direction.value

    def is_open(self, direction: Direction) -> bool:
        """Checks if a specific wall is open
        Args:
            direction (Direction): The wall to be checked
        Returns:
            1 (truthy) if the wall is open
            0 (falsy) if the wall is closed
        """

        return ~ self.walls & direction.value

    def open_wall(self, direction: Direction) -> None:
        """Opens one wall of the cell
        Do nothing if the wall is already open
        Args:
            direction (Direction): The wall to be opened
        """

        self.walls &= ~ direction.value

    def close_wall(self, direction: Direction) -> None:
        """Closes one wall of the cell
        Do nothing if the wall is already closed
        Args:
            direction (Direction): The wall to be closed
        """

        self.walls |= direction.value

    def __repr__(self) -> str:
        return hex(self.walls)[2].upper()

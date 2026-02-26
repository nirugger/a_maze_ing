from enum import Enum


class Direction(Enum):
    """Enum class used for walls direction
    Each number represents a cardinal direction, and also a bit
    value from LSB (0) to MSB (3)
    """

    north = 0
    east = 1
    south = 2
    west = 3


class Cell:
    """Class of a maze cell, with walls represented by an hexadecimal number
    Initialized as a full-closed cell (1111)
    """

    def __init__(self) -> None:
        """Initializes the cell as a full-closed cell (1111)"""

        self.walls = 0xf

    def is_wall_closed(self, direction: int) -> bool:
        """Checks if a specific wall is close or open
        Args:
            direction (Direction): The wall to be checked
        Returns:
            1 (truthy) if the wall is closed
            0 (falsy) if the wall is open
        """

        return self.walls & (1 << direction) == 1 << direction

    def open_wall(self, direction: int) -> None:
        """Opens one wall of the cell
        Do nothing if the wall is already open
        Args:
            direction (Direction): The wall to be opened
        """

        self.walls &= ~ (1 << direction)

    def close_wall(self, direction: int) -> None:
        """Closes one wall of the cell
        Do nothing if the wall is already closed
        Args:
            direction (Direction): The wall to be closed
        """

        self.walls |= 1 << direction

    def __repr__(self) -> str:
        return hex(self.walls)[2].upper()

"""Module for manage Cells of the Maze."""

from enum import Enum


class Direction(Enum):
    """Enum class used for walls direction.

    Each number represents a cardinal direction, and also a bit
    value used for bitshifting.
    """

    north = 1
    east = 2
    south = 4
    west = 8


class Cell:
    """Class representing a Cell of the Maze."""

    def __init__(self) -> None:
        """Initialize the cell as a full-closed cell (1111)."""
        self.walls = 0xf
        self.is_entry = False
        self.is_exit = False
        self.is_solved = False
        self.visited = 0
        self.steps = 0
        self.target = False
        self.is_player = False
        self.x_sub = 0
        self.y_sub = 0

    def is_closed(self, direction: Direction) -> int:
        """Check if a specific wall is closed.

        Args:
            direction (Direction): The wall to be checked.
        Returns:
            1,2,4,8 based on direction (truthy) if the wall is closed,
            0 (falsy) if the wall is open.
        """
        return self.walls & direction.value

    def is_open(self, direction: Direction) -> int:
        """Check if a specific wall is open.

        Args:
            direction (Direction): The wall to be checked.
        Returns:
            1,2,4,8 based on direction (truthy) if the wall is open.
            0 (falsy) if the wall is closed.
        """
        return (~ self.walls) & direction.value

    def open_wall(self, direction: Direction) -> None:
        """Open one wall of the cell.

        Args:
            direction (Direction): The wall to be opened.
        """
        self.walls &= ~ direction.value

    def close_wall(self, direction: Direction) -> None:
        """Close one wall of the cell.

        Args:
            direction (Direction): The wall to be closed.
        """
        self.walls |= direction.value

    def total_open(self) -> int:
        """Count how many walls are open.

        Returns:
            total: the number of open walls.
        """
        directions = [
            Direction.north,
            Direction.east,
            Direction.south,
            Direction.west
            ]

        total: int = 0
        for direction in directions:
            if self.is_open(direction):
                total += 1
        return total

    def total_closed(self) -> int:
        """Count how many walls are closed.

        Returns:
            total: the number of closed walls.
        """
        directions = [
            Direction.north,
            Direction.east,
            Direction.south,
            Direction.west
            ]

        total: int = 0
        for direction in directions:
            if self.is_closed(direction):
                total += 1
        return total

    def __repr__(self) -> str:
        """Format a string representation of the Cell.

        Returns:
            the string of an hexadecimal number between 0 and F.
        """
        return hex(self.walls)[2].upper()

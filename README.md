# A_MAZE_ING

## Todo


1) Config parser — legge e valida il file di configurazione
2) Maze generator — genera il labirinto
3) Maze validator — verifica che il labirinto rispetti le regole
4) File writer — salva il labirinto in esadecimale + coordinate + soluzione
5) Solver — trova il percorso più breve
6) Visualizer — mostra il labirinto graficamente


## Documentazione del Processo

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

    def __init__(self):
        """Initializes the cell as a full-closed cell (1111)"""

        self.walls = 0b1111

    # def is_north_closed(self) -> bool:
    #     return self.walls & 0b0001 == 0b0001

    # def open_north(self):
    #     self.walls &= 0b1110

    # def close_north(self):
    #     self.walls |= 0b0001

    def is_wall_closed(self, direction: Direction) -> bool:
        """Checks if a specific wall is close or open
        Args:
            direction (Direction): The wall to be checked
        Returns:
            True if the wall is closed
            False if the wall is open
        """

        return self.walls & 1 << direction.value == 1 << direction.value

        # if direction.value is 0:
        #     return self.walls & 0b0001 == 0b0001

        # if direction.value is 1:
        #     return self.walls & 0b0010 == 0b0010

        # if direction.value is 2:
        #     return self.walls & 0b0100 == 0b0100

        # if direction.value is 3:
        #     return self.walls & 0b1000 == 0b1000

    def open_wall(self, direction: Direction) -> None:
        """Opens one wall of the cell
        Do nothing if the wall is already open
        Args:
            direction (Direction): The wall to be opened
        """

        self.walls &= ~ (1 << direction.value)

        # if direction.value is 0:
        #     self.walls &= 0b1110

        # if direction.value is 1:
        #     self.walls &= 0b1101

        # if direction.value is 2:
        #     self.walls &= 0b1011

        # if direction.value is 3:
        #     self.walls &= 0b0111

    def close_wall(self, direction: Direction) -> None:
        """Closes one wall of the cell
        Do nothing if the wall is already closed
        Args:
            direction (Direction): The wall to be closed
        """

        self.walls |= 1 << direction.value

        # if direction.value is 0:
        #     self.walls |= 0b0001

        # if direction.value is 1:
        #     self.walls |= 0b0010

        # if direction.value is 2:
        #     self.walls |= 0b0100

        # if direction.value is 3:
        #     self.walls |= 0b1000

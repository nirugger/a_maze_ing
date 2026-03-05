"""Module for parsing and validating the configuration file."""

from pydantic import Field, field_validator, model_validator, ValidationError
from typing import (Optional, Tuple, Any, Union)
from pydantic import BaseModel
from abc import ABC


class MazeConfig(BaseModel):
    """BaseModel class for data validation."""

    WIDTH: int = Field(ge=2, le=41)
    HEIGHT: int = Field(ge=2, le=21)
    ENTRY: Tuple[int, int] = Field(min_length=2, max_length=2)
    EXIT: Tuple[int, int] = Field(min_length=2, max_length=2)
    START: Optional[Tuple[int, int]] = Field(default=None,
                                             min_length=2,
                                             max_length=2)
    OUTPUT_FILE: str
    PERFECT: bool
    ALGORITHM: Optional[str] = None
    SEED: Optional[str] = None

    @field_validator('ENTRY', 'EXIT', 'START', mode='before')
    @classmethod
    def parse_coordinates(cls,
                          v: Union[str, tuple[int, int]]) -> Tuple[int, int]:
        """Parse and validate coordinates types/format."""
        if isinstance(v, str):
            parts = v.split(',')
            if len(parts) != 2:
                raise ValueError("Coordinates must be in 'x,y' format")
            x, y = int(parts[0].strip()), int(parts[1].strip())
            if x < 0 or y < 0:
                raise ValueError("Coordinates must be greater than zero")
            return x, y
        return v

    @model_validator(mode='after')
    def check_coordinates_in_bounds(self) -> 'MazeConfig':
        """Parse and validate coordinates values."""
        if self.START is None:
            self.START = self.ENTRY
        for point_name, point in [('ENTRY', self.ENTRY),
                                  ('EXIT', self.EXIT),
                                  ('START', self.START)]:
            x, y = point
            if x >= self.WIDTH or y >= self.HEIGHT:
                raise ValueError(f"{point_name} {point} "
                                 "must be inside grid dimensions "
                                 f"({self.WIDTH - 1} x {self.HEIGHT - 1})")
        return self

    @model_validator(mode='after')
    def check_coordinates_overlap(self) -> 'MazeConfig':
        """Check if EntryPoint is the same as ExitPoint."""
        if self.ENTRY == self.EXIT:
            raise ValueError(f"ENTRY POINT {self.ENTRY} must be different "
                             f"from EXIT POINT {self.EXIT}")
        return self

    @field_validator('PERFECT', mode='before')
    @classmethod
    def parse_bool(cls, v: Any) -> bool:
        """Parse boolean value from configuration.

        Returns:
            v: boolean value
        """
        if isinstance(v, str):
            return v.strip().lower() == 'true'
        return bool(v)


class Parser(ABC):
    """Abstract class for configuration parse."""

    @classmethod
    def parse_config(cls, file_name: str) -> MazeConfig:
        """Parse and validate configuration file."""
        with open(file_name, 'r') as f:
            content = f.read()

        lines = content.split('\n')
        split_lines = [
            line.split('=') for line in lines
            if len(line.split('=')) == 2 and not line.strip().startswith('#')
            ]
        config = {k.strip(' '): v.strip(' ') for k, v in split_lines}

        model_config = cls.config_validator(config)
        return model_config

    @staticmethod
    def config_validator(config: dict[str, str]) -> MazeConfig:
        """Validate configuration."""
        mandatory_keys = [
            'WIDTH',
            'HEIGHT',
            'ENTRY',
            'EXIT',
            'OUTPUT_FILE',
            'PERFECT'
            ]

        val_config: dict[str, Any] = {}
        if (not all(key in config.keys() for key in mandatory_keys)):
            raise KeyError("one or more mandatory keys missing")
        entry_point = config['ENTRY'].split(',')
        exit_point = config['EXIT'].split(',')
        val_config['WIDTH'] = int(config['WIDTH'])
        val_config['HEIGHT'] = int(config['HEIGHT'])
        val_config['ENTRY'] = (int(entry_point[0]), int(entry_point[1]))
        val_config['EXIT'] = (int(exit_point[0]), int(exit_point[1]))
        val_config['OUTPUT_FILE'] = config['OUTPUT_FILE']
        val_config['PERFECT'] = True \
            if config['PERFECT'].strip().lower() == 'true' else False
        val_config['ALGORITHM'] = config['ALGORITHM']
        val_config['SEED'] = config['SEED']

        try:
            model = MazeConfig(**val_config)
            return model
        except ValidationError as e:
            raise KeyError(f"Validation error: {str(e)}")

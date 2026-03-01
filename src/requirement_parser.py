from pydantic import BaseModel
from pydantic import Field, field_validator, model_validator, ValidationError
from abc import ABC
from typing import Any, Tuple, Optional


class MazeConfig(BaseModel):

    WIDTH: int = Field(ge=2, le=41)
    HEIGHT: int = Field(ge=2, le=21)
    ENTRY: Tuple[int, int] = Field(min_length=2, max_length=2)
    EXIT: Tuple[int, int] = Field(min_length=2, max_length=2)
    OUTPUT_FILE: str
    PERFECT: bool
    ALGORITHM: Optional[str]

    @field_validator('ENTRY', 'EXIT', mode='before')
    @classmethod
    def parse_coordinates(cls, v: Any) -> Tuple[int, int]:
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
        for point_name, point in [('ENTRY', self.ENTRY), ('EXIT', self.EXIT)]:
            x, y = point
            if x >= self.WIDTH or y >= self.HEIGHT:
                raise ValueError(f"{point_name} {point} must be inside grid "
                                 f"dimensions ({self.WIDTH}x{self.HEIGHT})")
        return self

    @field_validator('PERFECT', mode='before')
    @classmethod
    def parse_bool(cls, v: Any) -> bool:
        if isinstance(v, str):
            return v.strip().lower() == 'true'
        return bool(v)


class Parser(ABC):

    @classmethod
    def parse_config(cls, file_name: str) -> dict[str, Any]:

        with open(file_name, 'r') as f:
            content = f.read()

        lines = content.split('\n')
        split_lines = [line.split('=') for line in lines
                       if not (line.strip().startswith('#') or
                       not line.strip())]
        config = {k: v for k, v in split_lines}

        config = cls.config_validator(config)
        return config

    @staticmethod
    def config_validator(config: dict[str, str]) -> dict[str, Any]:

        try:
            model = MazeConfig(**config)
            return model.model_dump()
        except ValidationError as e:
            raise KeyError(f"Validation error: {str(e)}")

    # mandatory_keys = [
    #     'WIDTH',
    #     'HEIGHT',
    #     'ENTRY',
    #     'EXIT',
    #     'OUTPUT_FILE',
    #     'PERFECT'
    #     ]
    # str_to_bool = {
    #     'true': True,
    #     'false': False
    #     }
    # val_config: dict[str, Any] = {}
    # if (not all(key in config.keys() for key in mandatory_keys)):
    #     raise KeyError("one or more mandatory keys missing")
    # entry_point = config['ENTRY'].split(',')
    # exit_point = config['EXIT'].split(',')
    # val_config['WIDTH'] = int(config['WIDTH'])
    # val_config['HEIGHT'] = int(config['HEIGHT'])
    # val_config['ENTRY'] = (int(entry_point[0]), int(entry_point[1]))
    # val_config['EXIT'] = (int(exit_point[0]), int(exit_point[1]))
    # val_config['OUTPUT_FILE'] = config['OUTPUT_FILE']
    # val_config['PERFECT'] = str_to_bool[config['PERFECT'].strip().lower()]
    # val_config['ALGORITHM'] = config['ALGORITHM']
    # return val_config

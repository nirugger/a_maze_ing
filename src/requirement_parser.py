from abc import ABC
from typing import Any


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

        mandatory_keys = [
            'WIDTH',
            'HEIGHT',
            'ENTRY',
            'EXIT',
            'OUTPUT_FILE',
            'PERFECT'
            ]

        str_to_bool = {
            'true': True,
            'false': False
            }

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
        val_config['PERFECT'] = str_to_bool[config['PERFECT'].strip().lower()]

        return val_config

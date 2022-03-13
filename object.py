from dataclasses import dataclass
from itertools import chain

from abilities import *
from constants import *


__all__ = ['Piece']


@dataclass
class Piece:
    name: str
    piece_type: str
    abilities: set[str] = S_NONE

    @classmethod
    def is_valid(cls, obj):
        return all((
            isinstance(obj, dict),
            'name' in obj,
            'piece_type' in obj,
            isinstance(obj.get('name', ''), str),
            isinstance((piece_type := obj.get('piece_type', 0)), int),
            isinstance((abilities := obj.get('abilities', 0)), int),
            0 <= piece_type <= 5,
            abilities & (B_TYPE[piece_type] | B_UNIQUE_TYPE[piece_type]) == abilities,
            (abilities & B_UNIQUE_TYPE[piece_type]).bit_count() <= 1,
        ))

    @classmethod
    def loads(cls, obj):
        piece_type = PIECE_TYPES[obj['piece_type']]
        abilities_flag = obj.get('abilities', 0)
        abilities = {*()}
        for name, flag in FLAGS.items():
            if abilities_flag & flag != 0:
                abilities.add(name)
        return cls(obj['name'], piece_type, abilities)

    def dumps(self):
        flag = 0
        for ability in self.abilities:
            flag |= FLAGS[ability]
        return {
            'name': self.name,
            'piece_type': PIECE_TYPES.index(self.piece_type),
            'abilities': flag,
        }

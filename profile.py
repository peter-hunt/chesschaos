from dataclasses import dataclass, field
from json import load as json_load
from os.path import join
from time import time

from object import Piece
from myjson import dump as json_dump

__all__ = ['Profile']


DEFAULT_INV = [
    Piece('Pawn', 'pawn'),
    Piece('Pawn', 'pawn'),
    Piece('Pawn', 'pawn'),
    Piece('Pawn', 'pawn'),
    Piece('Pawn', 'pawn'),
    Piece('Pawn', 'pawn'),
    Piece('Pawn', 'pawn'),
    Piece('Pawn', 'pawn'),
    Piece('Knight', 'knight'),
    Piece('Knight', 'knight'),
    Piece('Bishop', 'bishop'),
    Piece('Bishop', 'bishop'),
    Piece('Rook', 'rook'),
    Piece('Rook', 'rook'),
    Piece('Queen', 'queen'),
    Piece('King', 'king'),
]

@dataclass
class Profile:
    name: str
    inventory: list[Piece] = field(default_factory=lambda: DEFAULT_INV)
    coins: int | float = 0
    penalty: list[list[int, int]] = field(default_factory=list)

    last_update: float = 0.0

    @classmethod
    def is_valid(cls, obj):
        return all((
            isinstance(obj, dict),
            'name' in obj,
            isinstance(obj.get('name', ''), str),
            isinstance(obj.get('inventory', []), list),
            isinstance(obj.get('coins', 0), int | float),
            isinstance(obj.get('penalty', []), list),
            isinstance(obj.get('last_update', 0.0), float),
            all((Piece.is_valid(piece) for piece in obj.get('inventory', []))),
            all((isinstance(ls, list) and len(ls) == 2 for ls in obj.get('penalty', []))),
            all((isinstance(ls[0], int) and isinstance(ls[1], int)
                 for ls in obj.get('penalty', []))),
        ))

    @classmethod
    def loads(cls, obj: dict[str, str | list | int | float]):
        return cls(
            obj['name'],
            ([Piece.loads(piece) for piece in obj['inventory']]
             if 'inventory' in obj else DEFAULT_INV),
            obj.get('coins', 0),
            obj.get('penalty', []),
            obj.get('last_update', 0),
        )

    @classmethod
    def load(cls, name: str):
        with open(join('saves', f'{name}.json')) as file:
            obj = json_load(file)
        if cls.is_valid(obj):
            return cls.loads(obj)

    def dumps(self):
        return {
            'name': self.name,
            'inventory': [piece.dumps() for piece in self.inventory],
            'coins': self.coins,
            'penalty': self.penalty,
            'last_update': time(),
        }

    def dump(self):
        with open(join('saves', f'{self.name}.json'), 'w') as file:
            json_dump(self.dumps(), file)

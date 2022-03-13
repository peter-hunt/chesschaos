from dataclasses import dataclass, field
from json import load as json_load
from os.path import join
from time import time

from function import is_valid_piece, loads_piece, dumps_piece
from myjson import dump as json_dump
from numchess import Piece

__all__ = ['Profile']


DEFAULT_DECK = [
    Piece(3), Piece(1), Piece(2), Piece(4),
    Piece(5), Piece(2), Piece(1), Piece(3),
    Piece(0), Piece(0), Piece(0), Piece(0),
    Piece(0), Piece(0), Piece(0), Piece(0),
]

@dataclass
class Profile:
    name: str
    coins: int | float = 0
    inventory: list[Piece] = field(default_factory=list)
    deck: list[Piece] = field(default_factory=lambda: DEFAULT_DECK)
    penalty: list[list[int, int]] = field(default_factory=list)

    last_update: float = 0.0

    def __init__(self, name, coins=0, inventory=None, deck=None, penalty=None,
                 last_update=0.0):
        self.name = name
        self.inventory = inventory if inventory is not None else []
        self.deck = deck if deck is not None else DEFAULT_DECK
        self.coins = coins
        self.penalty = penalty if penalty is not None else []
        self.last_update = last_update

    @classmethod
    def is_valid(cls, obj):
        return all(cls._is_valid(obj))

    @classmethod
    def _is_valid(cls, obj):
        return (
            isinstance(obj, dict),
            'name' in obj,
            isinstance(obj.get('name', ''), str),
            isinstance(obj.get('coins', 0), int | float),
            isinstance(obj.get('inventory', []), list),
            isinstance(obj.get('deck', []), list),
            isinstance(obj.get('penalty', []), list),
            isinstance(obj.get('last_update', 0.0), float),
            all((is_valid_piece(piece) for piece in obj.get('inventory', []))),
            all((is_valid_piece(piece) for piece in obj.get('deck', []))),
            all((isinstance(ls, list) and len(ls) == 2 for ls in obj.get('penalty', []))),
            all((isinstance(ls[0], int) and isinstance(ls[1], int)
                 for ls in obj.get('penalty', []))),
        )

    @classmethod
    def loads(cls, obj: dict[str, str | list | int | float]):
        return cls(
            obj['name'],
            obj.get('coins', 0),
            ([loads_piece(piece) for piece in obj['inventory']]
             if 'inventory' in obj else []),
            ([loads_piece(piece) for piece in obj['deck']]
             if 'deck' in obj else DEFAULT_DECK),
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
            'coins': self.coins,
            'inventory': [dumps_piece(piece) for piece in self.inventory],
            'deck': [dumps_piece(piece) for piece in self.deck],
            'penalty': self.penalty,
            'last_update': time(),
        }

    def dump(self):
        with open(join('saves', f'{self.name}.json'), 'w') as file:
            json_dump(self.dumps(), file)


if __name__ == '__main__':
    from json import load as json_load
    from os.path import join
    with open(join('saves', 'castle.json')) as file:
        obj = json_load(file)
        print(Profile._is_valid(obj))

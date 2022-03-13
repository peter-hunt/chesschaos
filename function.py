from pygame.surface import Surface

from abilities import *
from numchess import *

__all__ = [
    'get_surface',
    '_is_valid_piece', 'is_valid_piece',
    'loads_piece', 'dumps_piece',
]

NoneType = type(None)


def get_surface(size, color=None, /):
    surface = Surface(size).convert_alpha()
    if color is not None:
        surface.fill(color)
    return surface


def _is_valid_piece(obj, /):
    return (
        isinstance(obj, dict),
        'piece_type' in obj,
        isinstance((piece_type := obj.get('piece_type', 0)), int),
        isinstance(obj.get('color', WHITE), bool),
        isinstance((abilities := obj.get('abilities', 0)), int),
        isinstance((unique_ability := obj.get('unique_ability', 0)), int),
        0 <= piece_type < 6,
        abilities & B_TYPE[(piece_type := min(max(piece_type, 0), 5))] == abilities,
        0 <= unique_ability <= B_UNIQUE_TYPE[piece_type],
    )


def is_valid_piece(obj, /):
    return all(_is_valid_piece(obj))


def loads_piece(obj, /):
    return Piece(obj['piece_type'], obj.get('color', WHITE), obj.get('abilities', 0),
                 obj.get('unique_ability', 0))


def dumps_piece(piece, /):
    obj = {'piece_type': piece.piece_type}
    if piece.abilities != 0:
        obj['abilities'] = piece.abilities
    if piece.unique_ability != 0:
        obj['unique_ability'] = piece.unique_ability
    return obj

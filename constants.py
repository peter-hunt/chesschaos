__all__ = [
    'DEFAULT_WINDOW_SIZE',
    'BACKGROUND_COLOR', 'MENU_COLOR',
    'LIGHT_SQUARE_COLOR', 'DARK_SQUARE_COLOR',
    'LIGHT_MOVE_COLOR', 'DARK_MOVE_COLOR',

    'PIECE_TYPES', 'PROFILE_NAMES',
]

DEFAULT_WINDOW_SIZE = (1280, 720)

BACKGROUND_COLOR = (49, 46, 43)
MENU_COLOR = (39, 37, 34)
LIGHT_SQUARE_COLOR = (238, 238, 210)
DARK_SQUARE_COLOR = (118, 150, 86)
LIGHT_MOVE_COLOR = (246, 246, 105)
DARK_MOVE_COLOR = (186, 202, 43)

PIECE_TYPES = ('pawn', 'knight', 'bishop', 'rook', 'queen', 'king')
PROFILE_NAMES = (
    'chess', 'board', 'light_square', 'dark_square',
    'pawn', 'knight', 'bishop', 'rook', 'queen', 'king',

    'enpassant', 'castle', 'check', 'checkmate', 'stalemate',
    'material', 'fork', 'pin',

    'sicilian_defense', 'kings_gambit', 'queens_gambit', 'bongcloud',

    'opening', 'midgame', 'endgame', 'zugzwang', 'puzzle', 'elo',
)

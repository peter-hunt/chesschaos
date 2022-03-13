__all__ = [
    'DEFAULT_WINDOW_SIZE',
    'BACKGROUND_COLOR', 'MENU_COLOR',
    'LIGHT_SQUARE_COLOR', 'DARK_SQUARE_COLOR',
    'LIGHT_MOVE_COLOR', 'DARK_MOVE_COLOR',

    'PIECE_TYPES', 'PROFILE_NAMES',

    'CLASSIC_LEVELS',
]

DEFAULT_WINDOW_SIZE = (1280, 720)

BACKGROUND_COLOR = (49, 46, 43)
MENU_COLOR = (39, 37, 34)
LIGHT_SQUARE_COLOR = (238, 238, 210)
DARK_SQUARE_COLOR = (118, 150, 86)
LIGHT_MOVE_COLOR = (246, 246, 105)
DARK_MOVE_COLOR = (186, 202, 43)

PIECE_TYPES = ('pawn', 'knight', 'bishop', 'rook', 'queen', 'king')
PROFILE_NAMES = ('pawn', 'knight', 'bishop', 'rook', 'queen', 'king')

CLASSIC_LEVELS = (
    ("Queen Checkmate",
     '4k3/8/8/8/8/8/8/3QK3 w - - 0 1'),
    ("Ladder Checkmate",
     '4k3/8/8/8/8/8/8/R3K2R w - - 0 1'),
    ("Bishop and Knight",
     '4k3/8/8/8/8/8/8/1N2KB2 w - - 0 1'),
    ("Bishops Checkmate",
     '4k3/8/8/8/8/8/8/2B1KB2 w - - 0 1'),
    ("Pawn Overwhelm",
     '4k3/8/8/8/8/8/PPPPPPPP/4K3 w - - 0 1'),

    ("Polygyny",
     'rnbqkbnr/pppppppp/8/8/8/8/QQQQQQQQ/QQQQKQQQ w KQkq - 0 1'),
    ("Fast and Furious",
     'rnbqkbnr/pppppppp/8/8/8/8/RRRRRRRR/RRRRKRRR w KQkq - 0 1'),
    ("Horsepower",
     'rnbqkbnr/pppppppp/8/8/8/8/NNNNNNNN/NNNNKNNN w KQkq - 0 1'),
    ("Religion",
     'rnbqkbnr/pppppppp/8/8/8/8/BBBBBBBB/BBBBKBBB w KQkq - 0 1'),
    ("Half Blood Horde",
     'rnbqkbnr/pppppppp/8/1PP2PP1/PPPPPPPP/PPPPPPPP/PPPPPPPP/RNBQKBNR w KQkq - 0 1'),

    ("King Hunt",
     '4k3/8/8/8/8/8/PPPPPPPP/RNBQKBNR w KQ - 0 1'),
    ("Easy Chess",
     '4k3/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQ - 0 1'),
    ("Who Needs Castling",
     '4k3/pppppppp/8/8/8/8/PPPPPPPP/1NBQKBN1 w - - 0 1'),
    ("Diagonal Firepower",
     '4k3/pppppppp/8/8/8/8/PPPPPPPP/2BQKB2 w - - 0 1'),
    ("Queen vs Pawns",
     '4k3/pppppppp/8/8/8/8/8/3QK3 w - - 0 1'),

    ("Excursion",
     'rnbqkbnr/pppppppp/8/4K3/8/8/PPPPPPPP/RNBQ1BNR b kq - 0 1'),
    ("Development",
     'r2q1rk1/pb4pp/1pnb1n2/2pppp2/8/8/PPPPPPPP/RNBQKBNR b KQ - 0 1'),
    ("Eccentric Opening",
     'rnbqkbnr/pppppppp/8/1B4B1/2N2N2/8/PPPPPPPP/R2QK2R b KQkq - 0 1'),
    ("Doubled Pawns",
     'rnbqkbnr/pppppppp/8/8/8/P1P2P1P/P1P2P1P/RNBQKBNR b KQkq - 0 1'),
    ("Backwards Pawns",
     'rnbqkbnr/pppppppp/8/8/8/RNBQ1BNR/PPPPPPPP/4K3 b kq - 0 1'),
)

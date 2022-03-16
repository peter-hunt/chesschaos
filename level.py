from numchess import *

__all__ = ['LEVELS', 'get_level_name', 'get_level', 'LEVEL_BOARDS']

LEVELS = [
    (
        'pawns',
        [
            None, None, None, None,
            Piece(5), None, None, None,
            Piece(0), Piece(0), Piece(0), Piece(0),
            Piece(0), Piece(0), Piece(0), Piece(0),
        ]
    ),
    (
        'pawns and queen',
        [
            None, None, None, Piece(4),
            Piece(5), None, None, None,
            Piece(0), Piece(0), Piece(0), Piece(0),
            Piece(0), Piece(0), Piece(0), Piece(0),
        ]
    ),
    (
        'major',
        [
            Piece(3), None, None, Piece(4),
            Piece(5), None, None, Piece(3),
            Piece(0), Piece(0), Piece(0), Piece(0),
            Piece(0), Piece(0), Piece(0), Piece(0),
        ]
    ),
    (
        'horsey',
        [
            Piece(3), Piece(1), None, Piece(4),
            Piece(5), None, Piece(1), Piece(3),
            Piece(0), Piece(0), Piece(0), Piece(0),
            Piece(0), Piece(0), Piece(0), Piece(0),
        ]
    ),
    (
        'full army',
        [
            Piece(3), Piece(1), Piece(2), Piece(4),
            Piece(5), Piece(2), Piece(1), Piece(3),
            Piece(0), Piece(0), Piece(0), Piece(0),
            Piece(0), Piece(0), Piece(0), Piece(0),
        ]
    )
]


def get_level_name(index) -> str:
    return LEVELS[index][0]


def get_level(index) -> Board:
    pieces = [
        (setattr(piece, 'color', BLACK),
         piece)[-1] if piece is not None
        else None for piece in LEVELS[index][1]
    ]

    board = Board()
    for rank in range(len(pieces) // 8):
        for file in range(8):
            piece = pieces[rank * 8 + file]
            if piece is not None:
                board.set_piece_at((7 - rank, file), piece)

    king_file = board.king(BLACK)[1]
    for file in range(king_file - 1, 8):
        if board.rooks[7, file]:
            board.castling_rights |= BB_SQUARES[SQUARES.index((7, file))]
            break
    for file in range(king_file - 1, -1, -1):
        if board.rooks[7, file]:
            board.castling_rights |= BB_SQUARES[SQUARES.index((7, file))]
            break

    return board


LEVEL_BOARDS = [get_level(i) for i in range(len(LEVELS))]

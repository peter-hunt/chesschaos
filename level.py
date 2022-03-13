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
    )
]


def get_level_name(index) -> str:
    return LEVELS[index][0]


def get_level(index) -> Board:
    pieces = LEVELS[index][1]
    pieces = [
        (setattr(piece, 'color', BLACK),
         piece)[-1] if piece is not None
        else None for piece in pieces
    ]
    board = Board()
    for rank in range(len(pieces) // 8):
        for file in range(8):
            piece = pieces[rank * 8 + file]
            if piece is not None:
                board.set_piece_at((7 - rank, file), piece)
    king_file = board.king(BLACK)[1]
    for i in range(king_file - 1, 8):
        if (board.rooks & BB_RANK_8 & BB_FILES[i]).any():
            board.castling_rights |= BB_RANK_8 & BB_FILES[i]
            break
    for i in range(king_file - 1, -1, -1):
        if (board.rooks & BB_RANK_8 & BB_FILES[i]).any():
            board.castling_rights |= BB_RANK_8 & BB_FILES[i]
            break

    return board


LEVEL_BOARDS = [get_level(i) for i in range(len(LEVELS))]

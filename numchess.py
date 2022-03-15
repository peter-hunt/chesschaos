from numpy import arange, array, ndarray, ones, where, zeros

from dataclasses import dataclass, field
from enum import Enum, auto as enumauto
from typing import Hashable, Iterable, Iterator, Optional

from abilities import *
from constants import *


PieceType = int
PIECE_TYPES = [PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING] = range(6)
PIECE_NAMES = ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']

Color = bool
# BUG: Color Code in use is reversed
COLORS = [WHITE, BLACK] = [True, False]
COLOR_NAMES = ['black', 'white']

Square = tuple[int, int]
SQUARES = [
    A1, B1, C1, D1, E1, F1, G1, H1,
    A2, B2, C2, D2, E2, F2, G2, H2,
    A3, B3, C3, D3, E3, F3, G3, H3,
    A4, B4, C4, D4, E4, F4, G4, H4,
    A5, B5, C5, D5, E5, F5, G5, H5,
    A6, B6, C6, D6, E6, F6, G6, H6,
    A7, B7, C7, D7, E7, F7, G7, H7,
    A8, B8, C8, D8, E8, F8, G8, H8,
] = [(r, f) for r in range(8) for f in range(8)]
FILE_NAMES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
RANK_NAMES = ['1', '2', '3', '4', '5', '6', '7', '8']
SQUARE_NAMES = {(ri, fi): f + r
                for ri, r in enumerate(RANK_NAMES)
                for fi, f in enumerate(FILE_NAMES)}


class Termination(Enum):
    CHECKMATE = enumauto()
    STALEMATE = enumauto()
    SEVENTYFIVE_MOVES = enumauto()
    FIVEFOLD_REPETITION = enumauto()


@dataclass
class Outcome:
    termination: Termination
    winner: Optional[Color]

    def result(self) -> str:
        return '1/2-1/2' if self.winner is None else ('1-0' if self.winner else '0-1')


def square_distance(a: Square, b: Square) -> int:
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))

def square_mirror(square: Square) -> Square:
    return (square[0], 7 - square[1])

SQUARES_180 = [square_mirror(sq) for sq in SQUARES]

BoolBoard = ndarray
BB_EMPTY = zeros((8, 8), dtype=bool)
BB_ALL = ones((8, 8), dtype=bool)
BB_SQUARES = [
    BB_A1, BB_B1, BB_C1, BB_D1, BB_E1, BB_F1, BB_G1, BB_H1,
    BB_A2, BB_B2, BB_C2, BB_D2, BB_E2, BB_F2, BB_G2, BB_H2,
    BB_A3, BB_B3, BB_C3, BB_D3, BB_E3, BB_F3, BB_G3, BB_H3,
    BB_A4, BB_B4, BB_C4, BB_D4, BB_E4, BB_F4, BB_G4, BB_H4,
    BB_A5, BB_B5, BB_C5, BB_D5, BB_E5, BB_F5, BB_G5, BB_H5,
    BB_A6, BB_B6, BB_C6, BB_D6, BB_E6, BB_F6, BB_G6, BB_H6,
    BB_A7, BB_B7, BB_C7, BB_D7, BB_E7, BB_F7, BB_G7, BB_H7,
    BB_A8, BB_B8, BB_C8, BB_D8, BB_E8, BB_F8, BB_G8, BB_H8,
] = [
    (
        board := BB_EMPTY.copy(),
        board.__setitem__((r, f), True),
        board,
    )[-1]
    for r in range(8) for f in range(8)
]
BB_FILES = [
    BB_FILE_A,
    BB_FILE_B,
    BB_FILE_C,
    BB_FILE_D,
    BB_FILE_E,
    BB_FILE_F,
    BB_FILE_G,
    BB_FILE_H,
] = [
    (
        board := BB_EMPTY.copy(),
        board.__setitem__((None, f), True),
        board,
    )[-1]
    for f in range(8)
]
BB_RANKS = [
    BB_RANK_1,
    BB_RANK_2,
    BB_RANK_3,
    BB_RANK_4,
    BB_RANK_5,
    BB_RANK_6,
    BB_RANK_7,
    BB_RANK_8,
] = [
    (
        board := BB_EMPTY.copy(),
        board.__setitem__((r, None), True),
        board,
    )[-1]
    for r in range(8)
]
BB_TO_FLAG = 2 ** arange(64, dtype='int64').reshape((8, 8))

BB_BACKRANKS = BB_RANK_1 | BB_RANK_8


def lsb(bb: BoolBoard) -> int:
    if not bb.any():
        return -1
    else:
        return where(bb.reshape((64,)))[0][-1]

def scan_forward(bb: BoolBoard) -> Iterator[Square]:
    for i in where(bb.reshape((64,)))[0]:
        yield SQUARES[i]

def msb(bb: BoolBoard) -> int:
    if not bb.any():
        return -1
    else:
        return where(bb.reshape((64,)))[0][0]

def scan_reversed(bb: BoolBoard) -> Iterator[Square]:
    for i in where(bb.reshape((64,)))[0][::-1]:
        yield SQUARES[i]

def flip_vertical(bb: BoolBoard) -> BoolBoard:
    return bb[::-1,:]

def flip_horizontal(bb: BoolBoard) -> BoolBoard:
    return bb[:,::-1]

def flip_diagonal(bb: BoolBoard) -> BoolBoard:
    return bb.T

def flip_anti_diagonal(bb: BoolBoard) -> BoolBoard:
    return bb[::-1,::-1].T

def shift_down(b: BoolBoard) -> BoolBoard:
    new = BB_EMPTY.copy()
    new[:7, :] = b[1:, :]
    return new

def shift_2_down(b: BoolBoard) -> BoolBoard:
    new = BB_EMPTY.copy()
    new[:6, :] = b[2:, :]
    return new

def shift_up(b: BoolBoard) -> BoolBoard:
    new = BB_EMPTY.copy()
    new[1:, :] = b[:7, :]
    return new

def shift_2_up(b: BoolBoard) -> BoolBoard:
    new = BB_EMPTY.copy()
    new[2:, :] = b[:6, :]
    return new

def shift_right(b: BoolBoard) -> BoolBoard:
    new = BB_EMPTY.copy()
    new[:, 1:] = b[:, :7]
    return new

def shift_2_right(b: BoolBoard) -> BoolBoard:
    new = BB_EMPTY.copy()
    new[:, 2:] = b[:, :6]
    return new

def shift_left(b: BoolBoard) -> BoolBoard:
    new = BB_EMPTY.copy()
    new[:, :7] = b[:, 1:]
    return new

def shift_2_left(b: BoolBoard) -> BoolBoard:
    new = BB_EMPTY.copy()
    new[:, :6] = b[:, 2:]
    return new

def shift_up_left(b: BoolBoard) -> BoolBoard:
    new = BB_EMPTY.copy()
    new[1:, :7] = b[:7, 1:]
    return new

def shift_up_right(b: BoolBoard) -> BoolBoard:
    new = BB_EMPTY.copy()
    new[:7, 1:] = b[1:, :7]
    return new

def shift_down_left(b: BoolBoard) -> BoolBoard:
    new = BB_EMPTY.copy()
    new[1:, :7] = b[:7, 1:]
    return new

def shift_down_right(b: BoolBoard) -> BoolBoard:
    new = BB_EMPTY.copy()
    new[1:, 1:] = b[:7, :7]
    return new


def _sliding_attacks(square: Square, occupied: BoolBoard, deltas: Iterable[int]) -> BoolBoard:
    attacks = BB_EMPTY.copy()

    for delta in deltas:
        sq = SQUARES.index(square)

        while True:
            sq += delta
            if not (0 <= sq < 64) or square_distance(SQUARES[sq], SQUARES[sq - delta]) > 2:
                break

            attacks |= BB_SQUARES[sq]

            if occupied[SQUARES[sq]]:
                break

    return attacks

def _step_attacks(square: Square, deltas: Iterable[int]) -> BoolBoard:
    return _sliding_attacks(square, BB_ALL, deltas)

BB_KNIGHT_ATTACKS = [_step_attacks(sq, [17, 15, 10, 6, -17, -15, -10, -6]) for sq in SQUARES]
BB_KING_ATTACKS = [_step_attacks(sq, [9, 8, 7, 1, -9, -8, -7, -1]) for sq in SQUARES]
BB_PAWN_ATTACKS = [[_step_attacks(sq, deltas) for sq in SQUARES] for deltas in [[-7, -9], [7, 9]]]
BB_PAWN_ATTACKS = [[_step_attacks(sq, deltas) for sq in SQUARES] for deltas in [[-7, -9], [7, 9]]]


def _edges(square: Square) -> BoolBoard:
    return (((BB_RANK_1 | BB_RANK_8) & ~BB_RANKS[square[0]]) |
            ((BB_FILE_A | BB_FILE_H) & ~BB_FILES[square[1]]))

def _carry_rippler(mask: BoolBoard) -> Iterator[BoolBoard]:
    # Carry-Rippler trick to iterate subsets of mask.
    _mask = (mask * BB_TO_FLAG).sum()
    subset = 0
    while True:
        yield (subset & BB_TO_FLAG).astype(bool)
        subset = (subset - _mask) & _mask
        if not subset:
            break

def _attack_table(deltas: list[int]) -> tuple[list[BoolBoard], list[dict[int, BoolBoard]]]:
    mask_table = []
    attack_table = []

    for square in SQUARES:
        attacks = {}

        mask = _sliding_attacks(square, BB_EMPTY.copy(), deltas) & ~_edges(square)
        for subset in _carry_rippler(mask):
            attacks[(BB_TO_FLAG * subset).sum()] = _sliding_attacks(square, subset, deltas)

        attack_table.append(attacks)
        mask_table.append(mask)

    return mask_table, attack_table

BB_DIAG_MASKS, BB_DIAG_ATTACKS = _attack_table([-9, -7, 7, 9])
BB_FILE_MASKS, BB_FILE_ATTACKS = _attack_table([-8, 8])
BB_RANK_MASKS, BB_RANK_ATTACKS = _attack_table([-1, 1])
BB_RIDER_MASKS, BB_RIDER_ATTACKS = _attack_table([17, 15, 10, 6, -17, -15, -10, -6])


def _rays() -> list[list[BoolBoard]]:
    rays = []
    for a, bb_a in enumerate(BB_SQUARES):
        rays_row = []
        for b, bb_b in enumerate(BB_SQUARES):
            if (BB_DIAG_ATTACKS[a][0] & bb_b).any():
                rays_row.append((BB_DIAG_ATTACKS[a][0] & BB_DIAG_ATTACKS[b][0]) | bb_a | bb_b)
            elif (BB_RANK_ATTACKS[a][0] & bb_b).any():
                rays_row.append(BB_RANK_ATTACKS[a][0] | bb_a)
            elif (BB_FILE_ATTACKS[a][0] & bb_b).any():
                rays_row.append(BB_FILE_ATTACKS[a][0] | bb_a)
            elif (BB_RIDER_ATTACKS[a][0] & bb_b).any():
                rays_row.append(BB_RIDER_ATTACKS[a][0] | bb_a)
            else:
                rays_row.append(BB_EMPTY.copy())
        rays.append(rays_row)
    return rays

BB_RAYS = _rays()

def ray(a: Square, b: Square) -> BoolBoard:
    return BB_RAYS[SQUARES.index(a)][SQUARES.index(b)]

def between(a: Square, b: Square) -> BoolBoard:
    mask = BB_EMPTY.copy().reshape((64,))
    mask[SQUARES.index(a):SQUARES.index(b)] = True
    bb = BB_RAYS[SQUARES.index(a)][SQUARES.index(b)] & mask.reshape((8, 8))
    bb = bb.reshape((64,))
    bb[lsb(bb)] = False
    return bb.reshape((8, 8))


AbBoard = ndarray
AB_EMPTY = zeros((8, 8), dtype='int32')
UnqAbBoard = ndarray
UB_EMPTY = zeros((8, 8), dtype='int8')


@dataclass
class Piece:
    piece_type: int
    color: int = WHITE
    abilities: int = B_NONE
    unique_ability: int = B_NONE


@dataclass
class Move:
    from_square: Square
    to_square: Square
    promotion: Optional[PieceType] = None

    def __repr__(self):
        return f'Move({SQUARE_NAMES[self.from_square]}{SQUARE_NAMES[self.to_square]})'


class _BoardState:

    def __init__(self, board) -> None:
        self.pawns = board.pawns.copy()
        self.knights = board.knights.copy()
        self.bishops = board.bishops.copy()
        self.rooks = board.rooks.copy()
        self.queens = board.queens.copy()
        self.kings = board.kings.copy()

        self.occupied_w = board.occupied_co[WHITE].copy()
        self.occupied_b = board.occupied_co[BLACK].copy()
        self.occupied = board.occupied.copy()

        self.turn = board.turn
        self.castling_rights = board.castling_rights.copy()
        self.halfmove_clock = board.halfmove_clock

    def restore(self, board) -> None:
        board.pawns = self.pawns.copy()
        board.knights = self.knights.copy()
        board.bishops = self.bishops.copy()
        board.rooks = self.rooks.copy()
        board.queens = self.queens.copy()
        board.kings = self.kings.copy()

        board.occupied_co[WHITE] = self.occupied_w.copy()
        board.occupied_co[BLACK] = self.occupied_b.copy()
        board.occupied = self.occupied.copy()

        board.turn = self.turn
        board.castling_rights = self.castling_rights.copy()
        board.halfmove_clock = self.halfmove_clock


class Board:
    turn: Color = WHITE
    pawns: BoolBoard = BB_EMPTY.copy()
    knights: BoolBoard = BB_EMPTY.copy()
    bishops: BoolBoard = BB_EMPTY.copy()
    rooks: BoolBoard = BB_EMPTY.copy()
    queens: BoolBoard = BB_EMPTY.copy()
    kings: BoolBoard = BB_EMPTY.copy()
    occupied_co: list[BoolBoard] = [BB_EMPTY.copy(), BB_EMPTY.copy()]
    occupied: BoolBoard = BB_EMPTY.copy()

    abilities: AbBoard = AB_EMPTY
    unique_ability: UnqAbBoard = UB_EMPTY

    castling_rights: BoolBoard = BB_EMPTY.copy()
    last_move: Optional[Move] = None
    halfmove_clock: int = 0
    move_stack: list[Move] = []
    _stack: list[_BoardState] = []

    def clear_board(self) -> None:
        self.pawns = BB_EMPTY.copy()
        self.knights = BB_EMPTY.copy()
        self.bishops = BB_EMPTY.copy()
        self.rooks = BB_EMPTY.copy()
        self.queens = BB_EMPTY.copy()
        self.kings = BB_EMPTY.copy()

        self.occupied_co[BLACK] = BB_EMPTY.copy()
        self.occupied_co[WHITE] = BB_EMPTY.copy()
        self.occupied = BB_EMPTY.copy()

        self.abilities = AB_EMPTY
        self.unique_ability = UB_EMPTY

        self.castling_rights = BB_EMPTY.copy()
        self.last_move = None
        self.halfmove_clock = 0

        self.clear_stack()

    def clear_stack(self) -> None:
        self.move_stack.clear()
        self._stack.clear()

    def piece_at(self, square: Square) -> Optional[Piece]:
        piece_type = self.piece_type_at(square)
        if piece_type is not None:
            color = self.occupied_co[WHITE][square]
            return Piece(piece_type, color, self.abilities[square],
                         self.unique_ability[square])

    def piece_type_at(self, square: Square) -> Optional[PieceType]:
        mask = BB_SQUARES[SQUARES.index(square)]

        if not self.occupied[square]:
            return
        elif (self.pawns & mask).any():
            return PAWN
        elif (self.knights & mask).any():
            return KNIGHT
        elif (self.bishops & mask).any():
            return BISHOP
        elif (self.rooks & mask).any():
            return ROOK
        elif (self.queens & mask).any():
            return QUEEN
        else:
            return KING

    def color_at(self, square: Square) -> Optional[Color]:
        if self.occupied_co[WHITE][square]:
            return WHITE
        elif self.occupied_co[BLACK][square]:
            return BLACK

    @property
    def legal_moves(self):
        return LegalMoveGenerator(self)

    def get_ep_square(self) -> Optional[Move]:
        ep_square = None
        if self.last_move is not None:
            lm_from, lm_to = self.last_move.from_square, self.last_move.to_square
            if abs(lm_to[0] - lm_from[0]) == 2 or abs(lm_to[1] - lm_from[1]) == 2:
                ep_square = (lm_to[0] + lm_from[0]) // 2, (lm_to[1] + lm_from[1]) // 2
        return ep_square

    def king(self, color: Color) -> Optional[Square]:
        king_mask = self.occupied_co[color] & self.kings
        return SQUARES[msb(king_mask)] if king_mask.any() else None

    def attacks_mask(self, square: Square) -> BoolBoard:
        square_index = SQUARES.index(square)
        bb_square = BB_SQUARES[square_index]

        if (bb_square & self.pawns).any():
            color = self.occupied_co[WHITE][square_index]
            return BB_PAWN_ATTACKS[color][square_index]
        elif (bb_square & self.knights).any():
            return BB_KNIGHT_ATTACKS[square_index]
        elif (bb_square & self.kings).any():
            return BB_KING_ATTACKS[square_index]
        else:
            attacks = 0
            if (bb_square & self.bishops).any() or (bb_square & self.queens).any():
                attacks = BB_DIAG_ATTACKS[square_index][(BB_TO_FLAG * (BB_DIAG_MASKS[square_index] & self.occupied)).sum()]
            if (bb_square & self.rooks).any() or (bb_square & self.queens).any():
                attacks |= (BB_RANK_ATTACKS[square_index][(BB_TO_FLAG * (BB_RANK_MASKS[square_index] & self.occupied)).sum()] |
                            BB_FILE_ATTACKS[square_index][(BB_TO_FLAG * (BB_FILE_MASKS[square_index] & self.occupied)).sum()])
            return attacks

    def _attackers_mask(self, color: Color, square: Square, occupied: BoolBoard) -> BoolBoard:
        index = SQUARES.index(square)
        rank_pieces = BB_RANK_MASKS[index] & occupied
        file_pieces = BB_FILE_MASKS[index] & occupied
        diag_pieces = BB_DIAG_MASKS[index] & occupied
        rider_pieces = BB_RIDER_MASKS[index] & occupied

        kings = self.kings | (self.abilities & B_SNEAKER).astype(bool)
        riders = (self.abilities & B_RIDER).astype(bool)
        knights = (self.knights | (self.abilities & B_LEAPER).astype(bool)) & ~riders
        queens_and_rooks = self.queens | self.rooks | (self.abilities & B_RUTHLESS).astype(bool)
        queens_and_bishops = self.queens | self.bishops | (self.abilities & B_SHIFTY).astype(bool)

        attackers = (
            (BB_KING_ATTACKS[index] & kings) |
            (BB_KNIGHT_ATTACKS[index] & knights) |
            (BB_RANK_ATTACKS[index][(BB_TO_FLAG * rank_pieces).sum()] & queens_and_rooks) |
            (BB_FILE_ATTACKS[index][(BB_TO_FLAG * file_pieces).sum()] & queens_and_rooks) |
            (BB_DIAG_ATTACKS[index][(BB_TO_FLAG * diag_pieces).sum()] & queens_and_bishops) |
            (BB_RIDER_ATTACKS[index][(BB_TO_FLAG * rider_pieces).sum()] & riders) |
            (BB_PAWN_ATTACKS[not color][index] & self.pawns))

        return attackers & self.occupied_co[color]

    def attackers_mask(self, color: Color, square: Square) -> BoolBoard:
        return self._attackers_mask(color, square, self.occupied)

    def is_attacked_by(self, color: Color, square: Square) -> bool:
        return (self.attackers_mask(color, square)).any()

    def pin_mask(self, color: Color, square: Square) -> BoolBoard:
        king = self.king(color)
        if king is None:
            return BB_ALL.copy()

        square_mask = BB_SQUARES[SQUARES.index(square)]

        riders = (self.abilities & B_RIDER).astype(bool)
        for attacks, sliders in [(BB_FILE_ATTACKS, self.rooks | self.queens),
                                 (BB_RANK_ATTACKS, self.rooks | self.queens),
                                 (BB_DIAG_ATTACKS, self.bishops | self.queens),
                                 (BB_RIDER_ATTACKS, riders)]:
            rays = attacks[king][0]
            if rays & square_mask:
                snipers = rays & sliders & self.occupied_co[not color]
                for sniper in scan_reversed(snipers):
                    if between(sniper, king) & (self.occupied | square_mask) == square_mask:
                        return ray(king, sniper)

                break

        return BB_ALL.copy()

    def remove_piece_at(self, square: Square) -> Optional[Piece]:
        if not self.occupied[square]:
            return
        mask = BB_SQUARES[SQUARES.index(square)]
        color = self.occupied_co[WHITE][square]

        if (self.pawns & mask).any():
            self.pawns[square] = False
            piece_type = PAWN
        elif (self.knights & mask).any():
            self.knights[square] = False
            piece_type = KNIGHT
        elif (self.bishops & mask).any():
            self.bishops[square] = False
            piece_type = BISHOP
        elif (self.rooks & mask).any():
            self.rooks[square] = False
            piece_type = ROOK
        elif (self.queens & mask).any():
            self.queens[square] = False
            piece_type = QUEEN
        else:
            self.kings[square] = False
            piece_type = KING

        self.occupied[square] = False
        self.occupied_co[color][square] = False
        abilities = self.abilities[square]
        unique_ability = self.unique_ability[square]
        self.abilities[square] = 0
        self.unique_ability[square] = 0

        return Piece(piece_type, color, abilities, unique_ability)

    def set_piece_at(self, square: Square, piece: Optional[Piece]):
        self.remove_piece_at(square)
        if piece is None:
            return

        piece_type = piece.piece_type

        mask = BB_SQUARES[SQUARES.index(square)]

        if piece_type == PAWN:
            self.pawns |= mask
        elif piece_type == KNIGHT:
            self.knights |= mask
        elif piece_type == BISHOP:
            self.bishops |= mask
        elif piece_type == ROOK:
            self.rooks |= mask
        elif piece_type == QUEEN:
            self.queens |= mask
        elif piece_type == KING:
            self.kings |= mask
        else:
            return

        self.occupied[square] = True
        self.occupied_co[piece.color][square] = True

        self.abilities[square] = piece.abilities
        self.unique_ability[square] = piece.unique_ability

    def copy(self):
        board = type(self)

        board.pawns = self.pawns
        board.knights = self.knights
        board.bishops = self.bishops
        board.rooks = self.rooks
        board.queens = self.queens
        board.kings = self.kings

        board.occupied_co[WHITE] = self.occupied_co[WHITE]
        board.occupied_co[BLACK] = self.occupied_co[BLACK]
        board.occupied = self.occupied

        board.castling_rights = self.castling_rights
        board.last_move = self.last_move
        board.halfmove_clock = self.halfmove_clock
        board.move_stack = self.move_stack
        board._stack = self._stack

        return board

    __copy__ = copy

    def clean_castling_rights(self) -> BoolBoard:
        if self._stack:
            # No new castling rights are assigned in a game, so we can assume
            # they were filtered already.
            return self.castling_rights

        castling = self.castling_rights & self.rooks
        white_castling = castling & BB_RANK_1 & self.occupied_co[WHITE]
        black_castling = castling & BB_RANK_8 & self.occupied_co[BLACK]

        # The kings must be on the back rank.
        white_king_mask = self.occupied_co[WHITE] & self.kings & BB_RANK_1
        black_king_mask = self.occupied_co[BLACK] & self.kings & BB_RANK_8
        if not white_king_mask.any():
            white_castling = BB_EMPTY.copy()
        if not black_king_mask.any():
            black_castling = BB_EMPTY.copy()

        # There are only two ways of castling, a-side and h-side, and the
        # king must be between the rooks.
        white_a_side = white_castling & ~white_castling
        white_h_side = BB_SQUARES[msb(white_castling)] if white_castling.any() else BB_EMPTY.copy()

        if white_a_side.any() and msb(white_a_side) > msb(white_king_mask):
            white_a_side = 0
        if white_h_side.any() and msb(white_h_side) < msb(white_king_mask):
            white_h_side = 0

        black_a_side = black_castling & ~black_castling
        black_h_side = BB_SQUARES[msb(black_castling)] if black_castling.any() else BB_EMPTY.copy()

        if black_a_side.any() and msb(black_a_side) > msb(black_king_mask):
            black_a_side = 0
        if black_h_side.any() and msb(black_h_side) < msb(black_king_mask):
            black_h_side = 0

        # Done.
        return black_a_side | black_h_side | white_a_side | white_h_side

    def generate_pseudo_legal_moves(self, from_mask: Optional[BoolBoard] = None, to_mask: Optional[BoolBoard] = None) -> Iterator[Move]:
        if from_mask is None:
            from_mask = BB_ALL.copy()
        if to_mask is None:
            to_mask = BB_ALL.copy()

        our_pieces = self.occupied_co[self.turn]
        unexpendable = our_pieces & ~(self.abilities & B_EXPENDABLE).astype(bool)

        # Generate piece moves.
        non_pawns = our_pieces & ~self.pawns & from_mask
        for from_square in scan_reversed(non_pawns):
            moves = self.attacks_mask(from_square) & ~unexpendable & to_mask
            for to_square in scan_reversed(moves):
                yield Move(from_square, to_square)

        # Generate castling moves.
        if (from_mask & self.kings).any():
            yield from self.generate_castling_moves(from_mask, to_mask)

        # The remaining moves are all pawn moves.
        pawns = self.pawns & self.occupied_co[self.turn] & from_mask
        if not pawns.any():
            return

        # Generate pawn captures.
        capturers = pawns
        for from_square in scan_reversed(capturers):
            targets = (
                BB_PAWN_ATTACKS[self.turn][SQUARES.index(from_square)] &
                (self.occupied_co[not self.turn] |
                 (self.abilities & B_EXPENDABLE).astype(bool)) & to_mask)

            for to_square in scan_reversed(targets):
                if to_square[0] in {0, 7}:
                    yield Move(from_square, to_square, QUEEN)
                    yield Move(from_square, to_square, ROOK)
                    yield Move(from_square, to_square, BISHOP)
                    yield Move(from_square, to_square, KNIGHT)
                elif self.abilities[from_square] & B_EAGLE and to_square[0] in {1, 6}:
                    yield Move(from_square, to_square, QUEEN)
                    yield Move(from_square, to_square, ROOK)
                    yield Move(from_square, to_square, BISHOP)
                    yield Move(from_square, to_square, KNIGHT)
                    yield Move(from_square, to_square)
                else:
                    yield Move(from_square, to_square)

        # Prepare pawn advance generation.
        if self.turn == WHITE:
            single_moves = shift_up(pawns) & ~self.occupied
            double_moves = shift_up(single_moves) & ~self.occupied & (BB_RANK_3 | BB_RANK_4)
        else:
            single_moves = shift_down(pawns) & ~self.occupied
            double_moves = shift_down(single_moves) & ~self.occupied & (BB_RANK_6 | BB_RANK_5)

        single_moves &= to_mask
        double_moves &= to_mask

        # Generate single pawn moves.
        for to_square in scan_reversed(single_moves):
            from_square = (
                to_square[0] + (1 if self.turn == BLACK else -1), to_square[1])

            if to_square[0] in [0, 7]:
                yield Move(from_square, to_square, QUEEN)
                yield Move(from_square, to_square, ROOK)
                yield Move(from_square, to_square, BISHOP)
                yield Move(from_square, to_square, KNIGHT)
            elif self.abilities[from_square] & B_EAGLE and to_square[0] in [1, 6]:
                yield Move(from_square, to_square, QUEEN)
                yield Move(from_square, to_square, ROOK)
                yield Move(from_square, to_square, BISHOP)
                yield Move(from_square, to_square, KNIGHT)
                yield Move(from_square, to_square)
            else:
                yield Move(from_square, to_square)

        # Generate double pawn moves.
        for to_square in scan_reversed(double_moves):
            from_square = (
                to_square[0] + (2 if self.turn == BLACK else -2), to_square[1])
            yield Move(from_square, to_square)

        # Generate en passant captures.
        yield from self.generate_pseudo_legal_ep(from_mask, to_mask)

    def generate_pseudo_legal_ep(self, from_mask: Optional[BoolBoard] = None,
                                 to_mask: Optional[BoolBoard] = None) -> Iterator[Move]:
        if from_mask is None:
            from_mask = BB_ALL.copy()
        if to_mask is None:
            to_mask = BB_ALL.copy()

        if self.last_move is None:
            return
        if self.piece_type_at(self.last_move.to_square) != PAWN:
            return
        lm_from, lm_to = self.last_move.from_square, self.last_move.to_square
        if abs(lm_to[0] - lm_from[0]) == 2 or abs(lm_to[1] - lm_from[1]) == 2:
            ep_square = (lm_to[0] + lm_from[0]) // 2, (lm_to[1] + lm_from[1]) // 2
        else:
            return

        if not (BB_SQUARES[ep_square] & to_mask).any():
            return

        if (BB_SQUARES[ep_square] & self.occupied).any():
            return

        capturers = (
            self.pawns & self.occupied_co[self.turn] & from_mask &
            BB_PAWN_ATTACKS[not self.turn][ep_square] &
            BB_RANKS[4 if self.turn else 3])

        for capturer in scan_reversed(capturers):
            yield Move(capturer, ep_square)

    def _attacked_for_king(self, path: BoolBoard, occupied: BoolBoard) -> bool:
        return any(self._attackers_mask(not self.turn, sq, occupied) for sq in scan_reversed(path))

    def generate_castling_moves(self, from_mask: Optional[BoolBoard] = None,
                                to_mask: Optional[BoolBoard] = None) -> Iterator[Move]:
        if from_mask is None:
            from_mask = BB_ALL.copy()
        if to_mask is None:
            to_mask = BB_ALL.copy()

        backrank = BB_RANK_1 if self.turn == WHITE else BB_RANK_8
        king = self.occupied_co[self.turn] & self.kings & backrank & from_mask
        king &= ~king
        king_sq = self.king(self.turn)
        if not king.any():
            return

        bb_c = BB_FILE_C & backrank
        bb_d = BB_FILE_D & backrank
        bb_f = BB_FILE_F & backrank
        bb_g = BB_FILE_G & backrank

        for candidate in scan_reversed(self.clean_castling_rights() & backrank & to_mask):
            rook = BB_SQUARES[SQUARES.index(candidate)]

            a_side = rook < king
            king_to = bb_c if a_side else bb_g
            rook_to = bb_d if a_side else bb_f

            king_path = between(SQUARES[msb(king)], SQUARES[msb(king_to)])
            rook_path = between(candidate, SQUARES[msb(rook_to)])

            if self.abilities[king_sq] & (B_STUBBORN | B_GHOST):
                if not ((self.occupied ^ king ^ rook) & (king_path | rook_path | king_to | rook_to) or
                        self._attacked_for_king(king_to, self.occupied ^ king ^ rook ^ rook_to)):
                    yield Move(SQUARES[msb(king)], candidate)
            else:
                if not ((self.occupied ^ king ^ rook) & (king_path | rook_path | king_to | rook_to) or
                        self._attacked_for_king(king_path | king, self.occupied ^ king) or
                        self._attacked_for_king(king_to, self.occupied ^ king ^ rook ^ rook_to)):
                    yield Move(SQUARES[msb(king)], candidate)

    def _to_chess960(self, move: Move) -> Move:
        if move.from_square == E1 and (self.kings & BB_E1).any():
            if move.to_square == G1 and not (self.rooks & BB_G1).any():
                return Move(E1, H1)
            elif move.to_square == C1 and not (self.rooks & BB_C1).any():
                return Move(E1, A1)
        elif move.from_square == E8 and (self.kings & BB_E8).any():
            if move.to_square == G8 and not (self.rooks & BB_G8).any():
                return Move(E8, H8)
            elif move.to_square == C8 and not (self.rooks & BB_C8).any():
                return Move(E8, A8)

        return move

    def checkers_mask(self) -> BoolBoard:
        king = self.king(self.turn)
        return BB_EMPTY.copy() if king is None else self.attackers_mask(not self.turn, king)

    def is_check(self) -> bool:
        return self.checkers_mask().any()

    def gives_check(self, move: Move) -> bool:
        self.push(move)
        try:
            return self.is_check()
        finally:
            self.pop()

    def is_into_check(self, move: Move) -> bool:
        king = self.king(self.turn)
        if king is None:
            return False

        # If already in check, look if it is an evasion.
        checkers = self.attackers_mask(not self.turn, king)
        if checkers.any() and move not in self._generate_evasions(
                king, checkers, BB_SQUARES[SQUARES.index(move.from_square)],
                BB_SQUARES[SQUARES.index(move.to_square)]):
            return True

        return not self._is_safe(king, self._slider_blockers(king), move)

    def was_into_check(self) -> bool:
        king = self.king(not self.turn)
        return king is not None and self.is_attacked_by(self.turn, king)

    def is_pseudo_legal(self, move: Move) -> bool:
        # Null moves are not pseudo-legal.
        if not move:
            return False

        # Source square must not be vacant.
        piece = self.piece_type_at(move.from_square)
        if piece is None:
            return False
        elif piece == PAWN:
            if self.piece_type_at(move.to_square) == PAWN:
                if (self.occupied_co[not self.turn]).any():
                    if self.abilities[move.from_square] & B_PACIFIST:
                        return False
                    if self.abilities[move.to_square] & B_PACIFIST:
                        return False

        # Get square masks.
        from_mask = BB_SQUARES[SQUARES.index(move.from_square)]
        to_mask = BB_SQUARES[SQUARES.index(move.to_square)]

        # Check turn.
        if not (self.occupied_co[self.turn] & from_mask).any():
            return False

        # Only pawns can promote and only on the backrank.
        if move.promotion:
            if piece != PAWN:
                return False

            if self.abilities[move.from_square] & B_EAGLE:
                if self.turn == WHITE and move.to_square[0] not in {6, 7}:
                    return False
                elif self.turn == BLACK and move.to_square[0] not in {0, 1}:
                    return False
            else:
                if self.turn == WHITE and move.to_square[0] != 7:
                    return False
                elif self.turn == BLACK and move.to_square[0] != 0:
                    return False

        # Handle castling.
        if piece == KING:
            move = Move(move.from_square, move.to_square)
            if move in self.generate_castling_moves():
                return True

        # Destination square can not be occupied.
        unexpendable = self.occupied_co[self.turn] & ~(self.abilities & B_EXPENDABLE).astype(bool)
        if (unexpendable & to_mask).any():
            return False

        # Handle pawn moves.
        if piece == PAWN:
            return move in self.generate_pseudo_legal_moves(from_mask, to_mask)

        # Handle all other pieces.
        return (self.attacks_mask(move.from_square) & to_mask).any()

    def is_legal(self, move: Move) -> bool:
        return self.is_pseudo_legal(move) and not self.is_into_check(move)

    def is_game_over(self, *, claim_draw: bool = False) -> bool:
        return self.outcome(claim_draw=claim_draw) is not None

    def outcome(self, *, claim_draw: bool = False) -> Optional[Outcome]:
        # Normal game end.
        if self.is_checkmate():
            return Outcome(Termination.CHECKMATE, not self.turn)
        if not any(self.generate_legal_moves()):
            return Outcome(Termination.STALEMATE, None)

        if self.is_seventyfive_moves():
            return Outcome(Termination.SEVENTYFIVE_MOVES, None)
        if self.is_fivefold_repetition():
            return Outcome(Termination.FIVEFOLD_REPETITION, None)

        return

    def is_checkmate(self) -> bool:
        if not self.is_check():
            return False

        return not any(self.generate_legal_moves())

    def is_stalemate(self) -> bool:
        if self.is_check():
            return False

        return not any(self.generate_legal_moves())

    def _is_halfmoves(self, n: int) -> bool:
        return self.halfmove_clock >= n and any(self.generate_legal_moves())

    def is_seventyfive_moves(self) -> bool:
        return self._is_halfmoves(150)

    def is_fivefold_repetition(self) -> bool:
        return self.is_repetition(5)

    def is_repetition(self, count: int = 3) -> bool:
        # Fast check, based on occupancy only.
        maybe_repetitions = 1
        for state in reversed(self._stack):
            if (state.occupied == self.occupied).all():
                maybe_repetitions += 1
                if maybe_repetitions >= count:
                    break
        if maybe_repetitions < count:
            return False

        # Check full replay.
        transposition_key = self._transposition_key()
        switchyard = []

        try:
            while True:
                if count <= 1:
                    return True

                if len(self.move_stack) < count - 1:
                    break

                move = self.pop()
                switchyard.append(move)

                if self.is_irreversible(move):
                    break

                if self._transposition_key() == transposition_key:
                    count -= 1
        finally:
            while switchyard:
                self.push(switchyard.pop())

        return False

    def is_en_passant(self, move: Move) -> bool:
        ep_square = self.get_ep_square()
        if ep_square is None:
            return False
        return (ep_square == move.to_square and
                self.pawns & BB_SQUARES[SQUARES.index(move.from_square)].any() and
                abs(move.to_square - move.from_square) in {7, 8, 9} and
                not self.occupied[move.to_square])

    def is_zeroing(self, move: Move) -> bool:
        touched = BB_SQUARES[SQUARES.index(move.from_square)] ^ BB_SQUARES[SQUARES.index(move.to_square)]
        return (touched & self.pawns).any() or (touched & self.occupied_co[not self.turn]).any()

    def _reduces_castling_rights(self, move: Move) -> bool:
        cr = self.clean_castling_rights()
        touched = BB_SQUARES[(move.from_square)] ^ BB_SQUARES[(move.to_square)]
        return bool((touched & cr).any() or
                    (cr & BB_RANK_1).any() and (touched & self.kings & self.occupied_co[WHITE]).any() or
                    (cr & BB_RANK_8).any() and (touched & self.kings & self.occupied_co[BLACK]).any())

    def is_irreversible(self, move: Move) -> bool:
        return self.is_zeroing(move) or self._reduces_castling_rights(move) or self.has_legal_en_passant()

    def is_castling(self, move: Move) -> bool:
        if (self.kings & BB_SQUARES[SQUARES.index(move.from_square)]).any():
            diff = move.from_square[1] - move.to_square[1]
            return abs(diff) > 1 or (self.rooks & self.occupied_co[self.turn] & BB_SQUARES[SQUARES.index(move.to_square)]).any()
        return False

    def _board_state(self) -> _BoardState:
        return _BoardState(self)

    def push(self, move: Move) -> None:
        # Push move and remember board state.
        move = self._to_chess960(move)
        board_state = self._board_state()
        self.castling_rights = self.clean_castling_rights()  # Before pushing stack
        self.move_stack.append(move)
        self._stack.append(board_state)

        # Increment move counters.
        self.halfmove_clock += 1

        # On a null move, simply swap turns and reset the en passant square.
        if not move:
            self.turn = not self.turn
            return

        # Zero the half-move clock.
        if self.is_zeroing(move):
            self.halfmove_clock = 0

        from_bb = BB_SQUARES[SQUARES.index(move.from_square)]
        to_bb = BB_SQUARES[SQUARES.index(move.to_square)]

        piece = self.remove_piece_at(move.from_square)
        assert piece is not None, f'push() expects move to be pseudo-legal, but got {move}'
        piece_type = piece.piece_type
        capture_square = move.to_square
        captured_piece_type = self.piece_type_at(capture_square)

        # Update castling rights.
        king_sq = self.king(self.turn)
        if not (self.abilities[king_sq] & B_GHOST).any():
            self.castling_rights &= ~to_bb & ~from_bb
            if piece_type == KING:
                if self.turn == WHITE:
                    self.castling_rights &= ~BB_RANK_1
                else:
                    self.castling_rights &= ~BB_RANK_8
            elif captured_piece_type == KING:
                if self.turn == WHITE and move.to_square[0] == 7:
                    self.castling_rights &= ~BB_RANK_8
                elif self.turn == BLACK and move.to_square[0] == 0:
                    self.castling_rights &= ~BB_RANK_1

        # Promotion.
        if move.promotion:
            piece_type = move.promotion

        # Castling.
        castling = (piece_type == KING) and (self.occupied_co[self.turn] & to_bb).any()
        if castling:
            a_side = move.to_square[1] < move.from_square[1]

            rook = self.remove_piece_at(move.to_square)

            if a_side:
                self.set_piece_at(C1 if self.turn == WHITE else C8, piece)
                self.set_piece_at(D1 if self.turn == WHITE else D8, rook)
            else:
                self.set_piece_at(G1 if self.turn == WHITE else G8, piece)
                self.set_piece_at(F1 if self.turn == WHITE else F8, rook)
        # Put the piece on the target square.
        else:
            self.set_piece_at(move.to_square, piece)

        # Swap turn.
        self.turn = not self.turn

    def pop(self) -> Move:
        move = self.move_stack.pop()
        self._stack.pop().restore(self)
        return move

    def _ep_skewered(self, king: Square, capturer: Square) -> bool:
        # Handle the special case where the king would be in check if the
        # pawn and its capturer disappear from the rank.

        # Vertical skewers of the captured pawn are not possible. (Pins on
        # the capturer are not handled here.)
        ep_square = self.get_ep_square()
        assert ep_square is not None

        last_double = ep_square + (-8 if self.turn == WHITE else 8)

        occupancy = (self.occupied[SQUARES[last_double]] &
                     ~BB_SQUARES[capturer] | BB_SQUARES[ep_square])

        # Horizontal attack on the fifth or fourth rank.
        horizontal_attackers = self.occupied_co[not self.turn] & (self.rooks | self.queens)
        if (BB_RANK_ATTACKS[king][BB_RANK_MASKS[king] & occupancy] & horizontal_attackers).any():
            return True

        # Diagonal skewers. These are not actually possible in a real game,
        # because if the latest double pawn move covers a diagonal attack,
        # then the other side would have been in check already.
        diagonal_attackers = self.occupied_co[not self.turn] & (self.bishops | self.queens)
        if (BB_DIAG_ATTACKS[king][BB_DIAG_MASKS[king] & occupancy] & diagonal_attackers).any():
            return True

        return False

    def _slider_blockers(self, king: Square) -> BoolBoard:
        rooks_and_queens = self.rooks | self.queens
        bishops_and_queens = self.bishops | self.queens
        riders = (self.abilities & B_RIDER).astype(bool)

        snipers = ((BB_RANK_ATTACKS[SQUARES.index(king)][0] & rooks_and_queens) |
                   (BB_FILE_ATTACKS[SQUARES.index(king)][0] & rooks_and_queens) |
                   (BB_DIAG_ATTACKS[SQUARES.index(king)][0] & bishops_and_queens) |
                   (BB_RIDER_ATTACKS[SQUARES.index(king)][0] & riders))

        blockers = 0

        for sniper in scan_reversed(snipers & self.occupied_co[not self.turn]):
            b = between(king, sniper) & self.occupied

            # Add to blockers if exactly one piece in-between.
            if b.any() and (BB_SQUARES[msb(b)] == b).all():
                blockers |= b

        return blockers & self.occupied_co[self.turn]

    def _is_safe(self, king: Square, blockers: BoolBoard, move: Move) -> bool:
        if move.from_square == king:
            if self.is_castling(move):
                return True
            else:
                return not self.is_attacked_by(not self.turn, move.to_square)
        elif self.is_en_passant(move):
            return bool((self.pin_mask(self.turn, move.from_square) & BB_SQUARES[SQUARES.index(move.to_square)]).any() and
                        not self._ep_skewered(king, move.from_square))
        else:
            return bool(not (blockers & BB_SQUARES[SQUARES.index(move.from_square)]).any() or
                        (ray(move.from_square, move.to_square) & BB_SQUARES[king]).any())

    def _generate_evasions(self, king: Square, checkers: BoolBoard,
                           from_mask: Optional[BoolBoard] = None, to_mask: Optional[BoolBoard] = None) -> Iterator[Move]:
        if from_mask is None:
            from_mask = BB_ALL.copy()
        if to_mask is None:
            to_mask = BB_ALL.copy()

        sliders = checkers & (self.bishops | self.rooks | self.queens)

        attacked = 0
        for checker in scan_reversed(sliders):
            attacked |= ray(king, checker) & ~BB_SQUARES[SQUARES.index(checker)]

        if (BB_SQUARES[SQUARES.index(king)] & from_mask).any():
            for to_square in scan_reversed(BB_KING_ATTACKS[SQUARES.index(king)] & ~self.occupied_co[self.turn] & ~attacked & to_mask):
                yield Move(king, to_square)

        checker = msb(checkers)
        if (BB_SQUARES[checker] == checkers).all():
            # Capture or block a single checker.
            target = between(king, SQUARES[checker]) | checkers

            yield from self.generate_pseudo_legal_moves(~self.kings & from_mask, target & to_mask)

            ep_square = self.get_ep_square()
            # Capture the checking pawn en passant (but avoid yielding
            # duplicate moves).
            if ep_square is not None and not (BB_SQUARES[ep_square] & target).any():
                last_double = ep_square + (-8 if self.turn == WHITE else 8)
                if last_double == checker:
                    yield from self.generate_pseudo_legal_ep(from_mask, to_mask)

    def generate_legal_ep(self, from_mask: Optional[BoolBoard] = None,
                          to_mask: Optional[BoolBoard] = None) -> Iterator[Move]:
        if from_mask is None:
            from_mask = BB_ALL.copy()
        if to_mask is None:
            to_mask = BB_ALL.copy()

        for move in self.generate_pseudo_legal_ep(from_mask, to_mask):
            if not self.is_into_check(move):
                yield move

    def generate_legal_moves(self, from_mask: Optional[BoolBoard] = None,
                             to_mask: Optional[BoolBoard] = None) -> Iterator[Move]:
        if from_mask is None:
            from_mask = BB_ALL.copy()
        if to_mask is None:
            to_mask = BB_ALL.copy()

        king_mask = self.kings & self.occupied_co[self.turn]
        if king_mask.any():
            king = SQUARES[msb(king_mask)]
            blockers = self._slider_blockers(king)
            checkers = self.attackers_mask(not self.turn, king)
            if checkers.any():
                for move in self._generate_evasions(king, checkers, from_mask, to_mask):
                    if self._is_safe(king, blockers, move):
                        yield move
            else:
                for move in self.generate_pseudo_legal_moves(from_mask, to_mask):
                    if self._is_safe(king, blockers, move):
                        yield move
        else:
            yield from self.generate_pseudo_legal_moves(from_mask, to_mask)

    def has_legal_en_passant(self) -> bool:
        return self.get_ep_square() is not None and any(self.generate_legal_ep())

    def _transposition_key(self) -> Hashable:
        keys = [self.pawns, self.knights, self.bishops, self.rooks,
                self.queens, self.kings,
                self.occupied_co[WHITE], self.occupied_co[BLACK],
                self.turn, self.clean_castling_rights(),
                self.ep_square if self.has_legal_en_passant() else None]
        return tuple(
            (BB_TO_FLAG * item).sum() if isinstance(item, ndarray) else item
            for item in keys
        )


class PseudoLegalMoveGenerator:
    def __init__(self, board: Board) -> None:
        self.board = board

    def __bool__(self) -> bool:
        return any(self.board.generate_pseudo_legal_moves())

    def count(self) -> int:
        # List conversion is faster than iterating.
        return len(list(self))

    def __iter__(self) -> Iterator[Move]:
        return self.board.generate_pseudo_legal_moves()

    def __contains__(self, move: Move) -> bool:
        return self.board.is_pseudo_legal(move)

    def __repr__(self) -> str:
        return '<PseudoLegalMoveGenerator>'


class LegalMoveGenerator:
    def __init__(self, board: Board) -> None:
        self.board = board

    def __bool__(self) -> bool:
        return any(self.board.generate_legal_moves())

    def count(self) -> int:
        # List conversion is faster than iterating.
        return len(list(self))

    def __iter__(self) -> Iterator[Move]:
        return self.board.generate_legal_moves()

    def __contains__(self, move: Move) -> bool:
        return self.board.is_legal(move)

    def __repr__(self) -> str:
        return '<LegalMoveGenerator>'

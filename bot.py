from chess import (
    BB_SQUARES, WHITE, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING)
from chess import Board
from chess.polyglot import zobrist_hash as hash_board
Board.__hash__ = hash_board

from functools import lru_cache
from math import inf
from random import choice as random_choice


__all__ = [
    'eval_board', 'search_openings', 'move_engine']


# pawn, knight, bishop, rook, queen, king
PIECE_VALUES = [None, 1, 3.2, 3.33, 5.1, 8.8, 0]
PAWN_POS_VALUES = [
     0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,
     0.05,  0.1 ,  0.1 , -0.2 , -0.2 ,  0.1 ,  0.1 ,  0.05,
     0.05, -0.05, -0.1 ,  0.0 ,  0.0 , -0.1 , -0.05,  0.05,
     0.0 ,  0.0 ,  0.0 ,  0.2 ,  0.2 ,  0.0 ,  0.0 ,  0.0 ,
     0.05,  0.05,  0.1 ,  0.25,  0.25,  0.1 ,  0.05,  0.05,
     0.1 ,  0.1 ,  0.2 ,  0.3 ,  0.3 ,  0.2 ,  0.1 ,  0.1 ,
     0.5 ,  0.5 ,  0.5 ,  0.5 ,  0.5 ,  0.5 ,  0.5 ,  0.5 ,
     0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,
]
KNIGHT_POS_VALUES = [
    -0.5 , -0.4 , -0.3 , -0.3 , -0.3 , -0.3 , -0.4 , -0.5 ,
    -0.4 , -0.2 ,  0.0 ,  0.05,  0.05,  0.0 , -0.2 , -0.4 ,
    -0.3 ,  0.05,  0.1 ,  0.15,  0.15,  0.1 ,  0.05, -0.3 ,
    -0.3 ,  0.0 ,  0.15,  0.2 ,  0.2 ,  0.15,  0.0 , -0.3 ,
    -0.3 ,  0.05,  0.15,  0.2 ,  0.2 ,  0.15,  0.05, -0.3 ,
    -0.3 ,  0.0 ,  0.1 ,  0.15,  0.15,  0.1 ,  0.0 , -0.3 ,
    -0.4 , -0.2 ,  0.0 ,  0.0 ,  0.0 ,  0.0 , -0.2 , -0.4 ,
    -0.5 , -0.4 , -0.3 , -0.3 , -0.3 , -0.3 , -0.4 , -0.5 ,
]
BISHOP_POS_VALUES = [
    -0.2 , -0.1 , -0.1 , -0.1 , -0.1 , -0.1 , -0.1 , -0.2 ,
    -0.1 ,  0.05,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.05, -0.1 ,
    -0.1 ,  0.1 ,  0.1 ,  0.1 ,  0.1 ,  0.1 ,  0.1 , -0.1 ,
    -0.1 ,  0.0 ,  0.1 ,  0.1 ,  0.1 ,  0.1 ,  0.0 , -0.1 ,
    -0.1 ,  0.05,  0.05,  0.1 ,  0.1 ,  0.05,  0.05, -0.1 ,
    -0.1 ,  0.0 ,  0.05,  0.1 ,  0.1 ,  0.05,  0.0 , -0.1 ,
    -0.1 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 , -0.1 ,
    -0.2 , -0.1 , -0.1 , -0.1 , -0.1 , -0.1 , -0.1 , -0.2 ,
]
ROOK_POS_VALUES = [
     0.0 ,  0.0 ,  0.0 ,  0.05,  0.05,  0.0 ,  0.0 ,  0.0 ,
    -0.05,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 , -0.05,
    -0.05,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 , -0.05,
    -0.05,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 , -0.05,
    -0.05,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 , -0.05,
    -0.05,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 , -0.05,
     0.05,  0.1 ,  0.1 ,  0.1 ,  0.1 ,  0.1 ,  0.1 ,  0.05,
     0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,
]
QUEEN_POS_VALUES = [
    -0.2 , -0.1 , -0.1 , -0.05, -0.05, -0.1 , -0.1 , -0.2 ,
    -0.1 ,  0.0 ,  0.05,  0.0 ,  0.0 ,  0.0 ,  0.0 , -0.1 ,
    -0.1 ,  0.05,  0.05,  0.05,  0.05,  0.05,  0.0 , -0.1 ,
     0.0 ,  0.0 ,  0.05,  0.05,  0.05,  0.05,  0.0 , -0.05,
    -0.05,  0.0 ,  0.05,  0.05,  0.05,  0.05,  0.0 , -0.05,
    -0.1 ,  0.0 ,  0.05,  0.05,  0.05,  0.05,  0.0 , -0.1 ,
    -0.1 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 , -0.1 ,
    -0.2 , -0.1 , -0.1 , -0.05, -0.05, -0.1 , -0.1 , -0.2 ,
]
KING_POS_VALUES = [
     0.2 ,  0.3 ,  0.1 ,  0.0 ,  0.0 ,  0.1 ,  0.3 ,  0.2 ,
     0.2 ,  0.2 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.2 ,  0.2 ,
    -0.1 , -0.2 , -0.2 , -0.2 , -0.2 , -0.2 , -0.2 , -0.1 ,
    -0.2 , -0.3 , -0.3 , -0.4 , -0.4 , -0.3 , -0.3 , -0.2 ,
    -0.3 , -0.4 , -0.4 , -0.5 , -0.5 , -0.4 , -0.4 , -0.3 ,
    -0.3 , -0.4 , -0.4 , -0.5 , -0.5 , -0.4 , -0.4 , -0.3 ,
    -0.3 , -0.4 , -0.4 , -0.5 , -0.5 , -0.4 , -0.4 , -0.3 ,
    -0.3 , -0.4 , -0.4 , -0.5 , -0.5 , -0.4 , -0.4 , -0.3 ,
]

POS_VALUES = [[], PAWN_POS_VALUES, KNIGHT_POS_VALUES, BISHOP_POS_VALUES,
              ROOK_POS_VALUES, QUEEN_POS_VALUES, KING_POS_VALUES]
for i in range(1, 7):
    for j in range(64):
        POS_VALUES[i][j] += PIECE_VALUES[i]

OPENINGS = {
    ('d4',),
    ('g3',),
    ('Nf3',),
    ('f4',),
    ('b3',),
    ('e4',),
    ('c4',),
    ('c4', 'c5'),
    ('e4', 'Nf6'),
    ('e4', 'c6'),
    ('d4', 'g6'),
    ('e4', 'c5'),
    ('e4', 'd5'),
    ('d4', 'f5'),
    ('e4', 'e6'),
    ('e4', 'd6'),
    ('d4', 'c5'),
    ('c4', 'e5'),
    ('e4', 'c5', 'Nc3'),
    ('d4', 'Nf6', 'Bg5'),
    ('Nf3', 'd5', 'c4'),
    ('e4', 'e5', 'Nc3'),
    ('d4', 'd5', 'c4'),
    ('e4', 'e5', 'f4'),
    ('Nf3', 'd5', 'g3'),
    ('d4', 'Nf6', 'c4', 'd6'),
    ('d4', 'Nf6', 'c4', 'e5'),
    ('d4', 'Nf6', 'c4', 'e6', 'g3'),
    ('d4', 'Nf6', 'c4', 'g6'),
    ('d4', 'd5', 'Nf3', 'Nf6', 'Bf4'),
    ('d4', 'd5', 'Nf3', 'Nf6', 'Bg5'),
    ('d4', 'd5', 'c4', 'Nc6'),
    ('d4', 'd5', 'c4', 'c6'),
    ('d4', 'd5', 'c4', 'dxc4'),
    ('d4', 'd5', 'c4', 'e5'),
    ('d4', 'd5', 'e4'),
    ('d4', 'f5', 'e4', 'fxe4'),
    ('e4', 'c5', 'Nc3', 'Nc6', 'f4'),
    ('e4', 'c5', 'c3'),
    ('e4', 'c5', 'd4'),
    ('e4', 'c6', 'd4', 'd5', 'exd5'),
    ('e4', 'd5', 'exd5', 'Nf6'),
    ('e4', 'e5', 'Bc4'),
    ('e4', 'e5', 'Nf3', 'Nf6'),
    ('e4', 'e5', 'Nf3', 'Nf6', 'd4'),
    ('e4', 'e5', 'Nf3', 'd6'),
    ('e4', 'e5', 'f4', 'Bc5'),
    ('e4', 'e5', 'f4', 'd5'),
    ('e4', 'e5', 'f4', 'exf4'),
    ('e4', 'e6', 'd4', 'd5', 'e5'),
    ('d4', 'Nf6', 'c4', 'c5', 'd5', 'b5'),
    ('d4', 'Nf6', 'c4', 'c5', 'd5', 'e6'),
    ('d4', 'Nf6', 'c4', 'e6', 'Nc3', 'Bb4'),
    ('d4', 'Nf6', 'c4', 'e6', 'Nf3', 'b6'),
    ('d4', 'Nf6', 'c4', 'g6', 'Nc3', 'Bg7'),
    ('d4', 'Nf6', 'c4', 'g6', 'Nc3', 'd5'),
    ('d4', 'd5', 'Nc3', 'Nf6', 'Bg5'),
    ('e4', 'c6', 'd4', 'd5', 'e5'),
    ('e4', 'e5', 'Nf3', 'Nc6', 'Bb5'),
    ('e4', 'e5', 'Nf3', 'Nc6', 'Bb5', 'Bc5'),
    ('e4', 'e5', 'Nf3', 'Nc6', 'Bc4'),
    ('e4', 'e5', 'Nf3', 'Nc6', 'Bc4', 'Bc5'),
    ('e4', 'e5', 'Nf3', 'Nc6', 'Bc4', 'Be7'),
    ('e4', 'e5', 'Nf3', 'Nc6', 'Bc4', 'Nf6'),
    ('e4', 'e5', 'Nf3', 'Nc6', 'Nc3', 'Nf6'),
    ('e4', 'e5', 'Nf3', 'Nc6', 'd4'),
    ('e4', 'e5', 'Nf3', 'Nf6', 'Nc3'),
    ('e4', 'e5', 'd4', 'exd4', 'c3'),
    ('e4', 'e5', 'f4', 'exf4', 'Bc4'),
    ('e4', 'e5', 'f4', 'exf4', 'Nf3', 'd5'),
    ('e4', 'e6', 'd4', 'd5', 'Nc3', 'Nf6'),
    ('e4', 'e6', 'd4', 'd5', 'Nc3', 'dxe4'),
    ('e4', 'e6', 'd4', 'd5', 'Nd2'),
    ('e4', 'e6', 'd4', 'd5', 'exd5'),
    ('e4', 'g6', 'd4', 'Bg7', 'Nc3', 'c5'),
    ('d4', 'Nf6', 'c4', 'e6', 'Nc3', 'Bb4', 'Qc2'),
    ('d4', 'Nf6', 'c4', 'e6', 'Nc3', 'Bb4', 'e3', 'c5'),
    ('d4', 'Nf6', 'c4', 'e6', 'Nf3', 'Bb4+'),
    ('d4', 'Nf6', 'c4', 'e6', 'g3', 'd5', 'Bg2'),
    ('d4', 'Nf6', 'c4', 'g6', 'Nc3', 'd5', 'Bf4'),
    ('d4', 'Nf6', 'c4', 'g6', 'Nc3', 'd5', 'Bg5'),
    ('d4', 'Nf6', 'c4', 'g6', 'Nc3', 'd5', 'Nf3'),
    ('d4', 'd5', 'c4', 'e6', 'Nc3', 'Nf6', 'Nf3', 'c6'),
    ('d4', 'd5', 'c4', 'e6', 'Nf3', 'c5'),
    ('e4', 'c5', 'Nf3', 'e6', 'd4', 'cxd4', 'Nxd4', 'Nc6'),
    ('e4', 'c5', 'Nf3', 'e6', 'd4', 'cxd4', 'Nxd4', 'a6'),
    ('e4', 'c6', 'd4', 'd5', 'Nc3', 'dxe4', 'Nxe4', 'Bf5'),
    ('e4', 'c6', 'd4', 'd5', 'exd5', 'cxd5', 'c4'),
    ('e4', 'd6', 'd4', 'Nf6', 'Nc3', 'g6', 'Nf3'),
    ('e4', 'd6', 'd4', 'Nf6', 'Nc3', 'g6', 'f4'),
    ('e4', 'e5', 'Nf3', 'Nc6', 'Bb5', 'Nf6'),
    ('e4', 'e5', 'Nf3', 'Nc6', 'Bb5', 'a6', 'Bxc6'),
    ('e4', 'e5', 'Nf3', 'Nc6', 'Bb5', 'd6'),
    ('e4', 'e5', 'Nf3', 'Nc6', 'Bb5', 'f5'),
    ('e4', 'e5', 'Nf3', 'Nc6', 'Bc4', 'Bc5', 'b4'),
    ('e4', 'e5', 'Nf3', 'Nc6', 'Nc3', 'Nf6', 'd4'),
    ('e4', 'e5', 'Nf3', 'Nc6', 'd4', 'exd4', 'Nxd4', 'Bc5'),
    ('e4', 'e5', 'Nf3', 'Nc6', 'd4', 'exd4', 'Nxd4', 'Qh4'),
    ('e4', 'e6', 'd4', 'd5', 'Nc3', 'Bb4'),
    ('e4', 'e6', 'd4', 'd5', 'Nc3', 'Nf6', 'Bg5', 'dxe4'),
    ('d4', 'Nf6', 'c4', 'e6', 'Nc3', 'Bb4', 'a3', 'Bxc3+', 'bxc3'),
    ('d4', 'Nf6', 'c4', 'e6', 'Nc3', 'Bb4', 'e3', 'c5', 'Ne2'),
    ('d4', 'Nf6', 'c4', 'g6', 'Nc3', 'Bg7', 'Nf3', 'd6', 'g3'),
    ('d4', 'Nf6', 'c4', 'g6', 'Nc3', 'Bg7', 'e4', 'd6', 'Be2', 'O-O', 'Bg5'),
    ('d4', 'Nf6', 'c4', 'g6', 'Nc3', 'Bg7', 'e4', 'd6', 'Nf3', 'O-O', 'Be2'),
    ('d4', 'Nf6', 'c4', 'g6', 'Nc3', 'Bg7', 'e4', 'd6', 'Nf3', 'O-O', 'Be2', 'e5', 'O-O', 'Nc6', 'd5', 'Ne7', 'b4'),
    ('d4', 'Nf6', 'c4', 'g6', 'Nc3', 'Bg7', 'e4', 'd6', 'f3'),
    ('d4', 'Nf6', 'c4', 'g6', 'Nc3', 'Bg7', 'e4', 'd6', 'f4'),
    ('d4', 'Nf6', 'c4', 'g6', 'Nc3', 'd5', 'cxd5', 'Nxd5'),
    ('d4', 'd5', 'c4', 'e6', 'Nc3', 'Nf6', 'Bg5', 'Be7', 'e3', 'O-O', 'Nf3', 'Nbd7'),
    ('d4', 'd5', 'c4', 'e6', 'Nc3', 'Nf6', 'Nf3', 'c5'),
    ('d4', 'f5', 'c4', 'Nf6', 'g3', 'e6', 'Bg2', 'Be7', 'Nf3', 'O-O', 'O-O', 'd5'),
    ('d4', 'f5', 'c4', 'Nf6', 'g3', 'g6', 'Bg2', 'Bg7', 'Nf3'),
    ('e4', 'c5', 'Nf3', 'Nc6', 'd4', 'cxd4', 'Nxd4', 'g6'),
    ('e4', 'c5', 'Nf3', 'd6', 'd4', 'cxd4', 'Nxd4', 'Nf6', 'Nc3', 'Nc6', 'Bg5'),
    ('e4', 'c5', 'Nf3', 'd6', 'd4', 'cxd4', 'Nxd4', 'Nf6', 'Nc3', 'a6'),
    ('e4', 'c5', 'Nf3', 'd6', 'd4', 'cxd4', 'Nxd4', 'Nf6', 'Nc3', 'e6'),
    ('e4', 'c5', 'Nf3', 'd6', 'd4', 'cxd4', 'Nxd4', 'Nf6', 'Nc3', 'g6'),
    ('e4', 'e5', 'Nf3', 'Nc6', 'd4', 'exd4', 'Nxd4', 'Nf6', 'Nxc6', 'bxc6', 'e5'),
    ('e4', 'e5', 'Nf3', 'Nf6', 'Nxe5', 'd6', 'Nf3', 'Nxe4', 'd4'),
}


# Stockfish does 70m/s
def eval_board(board):  # 25k/s
    if board.is_checkmate():
        return -inf if board.turn else inf
    elif board.is_game_over():
        return 0

    weight = 0
    flag = 1
    occupied = board.occupied
    pawns = board.pawns
    knights = board.knights
    bishops = board.bishops
    rooks = board.rooks
    queens = board.queens
    kings = board.kings
    occupied_co = board.occupied_co[WHITE]
    for pos in range(64):
        if not occupied & flag:
            flag <<= 1
            continue
        if pawns & flag:
            piece_type = PAWN
        elif knights & flag:
            piece_type = KNIGHT
        elif bishops & flag:
            piece_type = BISHOP
        elif rooks & flag:
            piece_type = ROOK
        elif queens & flag:
            piece_type = QUEEN
        elif kings & flag:
            piece_type = KING
        if occupied_co & flag:
            weight += POS_VALUES[piece_type][pos]
        else:
            weight -= POS_VALUES[piece_type][pos ^ 0x38]
        flag <<= 1

    return weight


def cmp(a, b):  # 410k/s
    return (a > b) - (a < b)


@lru_cache()
def gen_moves(board):
    return sorted(list(board.legal_moves), key=lambda move: (
        -(move.promotion is not None),
        -(BB_SQUARES[move.to_square] & board.occupied),
        -(BB_SQUARES[move.to_square] & board.pawns),
    ))


def search_openings(board):  # 11k/s
    _board = Board()
    san_moves = []
    for move in board.move_stack:
        san_moves.append(_board.san(move))
        _board.push(move)
    san_moves = tuple(san_moves)
    move_count = len(board.move_stack)
    move_choices = {*()}
    for opening in sorted([*OPENINGS.keys()], key=lambda opening: (len(opening),) + opening):
        if len(opening) <= move_count:
            continue
        if opening[:move_count] == san_moves:
            move_choices.add(opening[move_count])
    if len(move_choices) != 0:
        move_name = random_choice([*move_choices])
        name = None
        all_moves = san_moves + (move_name,)
        for opening in sorted([*OPENINGS.keys()], key=lambda opening: (len(opening),) + opening):
            if len(opening) <= move_count:
                continue
            if opening[:move_count + 1] == all_moves:
                name = OPENINGS[opening]
                break
        return name, board.parse_san(move_name)
    return None, None


def move_search(board, depth, alpha=-inf, beta=inf):
    if depth == 0 or board.is_game_over():
        return eval_board(board), None
    best_move = None
    if board.turn:
        value = -inf
        for move in gen_moves(board):
            board.push(move)
            result, _ = move_search(board, depth - 1, alpha, beta)
            board.pop()
            value = max(value, result)
            if value >= beta:
                break
            if value > alpha:
                alpha = value
                best_move = move
        return value, best_move
    else:
        value = inf
        for move in gen_moves(board):
            board.push(move)
            result, _ = move_search(board, depth - 1, alpha, beta)
            board.pop()
            value = min(value, result)
            if value <= alpha:
                break
            if value < beta:
                beta = value
                best_move = move
        return value, best_move


def move_engine(board: Board, /, depth=4, *, use_openings=True):
    if use_openings:
        name, move = search_openings(board)
        if move is not None:
            return move
    move = move_search(board, depth)[1]
    if move is None:
        move = random_choice([move for move in board.legal_moves])
    return move

from numchess import (
    BB_SQUARES, SQUARES, WHITE, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING)
from numchess import Board

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


def gen_moves(board):
    return sorted(list(board.legal_moves), key=lambda move: (
        -(move.promotion is not None),
        ~(BB_SQUARES[SQUARES.index(move.to_square)] & board.occupied).any(),
        ~(BB_SQUARES[SQUARES.index(move.to_square)] & board.pawns).any(),
    ))


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


def move_engine(board: Board, /, depth=3):
    move = move_search(board, depth)[1]
    if move is None:
        move = random_choice([move for move in board.legal_moves])
    return move

from numchess import *
from numchess import Board

from math import inf
from numpy import array
from random import choice as random_choice


__all__ = [
    'eval_board', 'search_openings', 'move_engine']


# pawn, knight, bishop, rook, queen, king
PIECE_VALUES = [1, 3.2, 3.33, 5.1, 8.8, 0]
PAWN_POS_VALUES = array([
    [ 0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ],
    [ 0.05,  0.1 ,  0.1 , -0.2 , -0.2 ,  0.1 ,  0.1 ,  0.05],
    [ 0.05, -0.05, -0.1 ,  0.0 ,  0.0 , -0.1 , -0.05,  0.05],
    [ 0.0 ,  0.0 ,  0.0 ,  0.2 ,  0.2 ,  0.0 ,  0.0 ,  0.0 ],
    [ 0.05,  0.05,  0.1 ,  0.25,  0.25,  0.1 ,  0.05,  0.05],
    [ 0.1 ,  0.1 ,  0.2 ,  0.3 ,  0.3 ,  0.2 ,  0.1 ,  0.1 ],
    [ 0.5 ,  0.5 ,  0.5 ,  0.5 ,  0.5 ,  0.5 ,  0.5 ,  0.5 ],
    [ 0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ],
]) + 1
KNIGHT_POS_VALUES = array([
    [-0.5 , -0.4 , -0.3 , -0.3 , -0.3 , -0.3 , -0.4 , -0.5 ],
    [-0.4 , -0.2 ,  0.0 ,  0.05,  0.05,  0.0 , -0.2 , -0.4 ],
    [-0.3 ,  0.05,  0.1 ,  0.15,  0.15,  0.1 ,  0.05, -0.3 ],
    [-0.3 ,  0.0 ,  0.15,  0.2 ,  0.2 ,  0.15,  0.0 , -0.3 ],
    [-0.3 ,  0.05,  0.15,  0.2 ,  0.2 ,  0.15,  0.05, -0.3 ],
    [-0.3 ,  0.0 ,  0.1 ,  0.15,  0.15,  0.1 ,  0.0 , -0.3 ],
    [-0.4 , -0.2 ,  0.0 ,  0.0 ,  0.0 ,  0.0 , -0.2 , -0.4 ],
    [-0.5 , -0.4 , -0.3 , -0.3 , -0.3 , -0.3 , -0.4 , -0.5 ],
]) + 3.2
BISHOP_POS_VALUES = array([
    [-0.2 , -0.1 , -0.1 , -0.1 , -0.1 , -0.1 , -0.1 , -0.2 ],
    [-0.1 ,  0.05,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.05, -0.1 ],
    [-0.1 ,  0.1 ,  0.1 ,  0.1 ,  0.1 ,  0.1 ,  0.1 , -0.1 ],
    [-0.1 ,  0.0 ,  0.1 ,  0.1 ,  0.1 ,  0.1 ,  0.0 , -0.1 ],
    [-0.1 ,  0.05,  0.05,  0.1 ,  0.1 ,  0.05,  0.05, -0.1 ],
    [-0.1 ,  0.0 ,  0.05,  0.1 ,  0.1 ,  0.05,  0.0 , -0.1 ],
    [-0.1 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 , -0.1 ],
    [-0.2 , -0.1 , -0.1 , -0.1 , -0.1 , -0.1 , -0.1 , -0.2 ],
]) + 3.33
ROOK_POS_VALUES = array([
    [ 0.0 ,  0.0 ,  0.0 ,  0.05,  0.05,  0.0 ,  0.0 ,  0.0 ],
    [-0.05,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 , -0.05],
    [-0.05,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 , -0.05],
    [-0.05,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 , -0.05],
    [-0.05,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 , -0.05],
    [-0.05,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 , -0.05],
    [ 0.05,  0.1 ,  0.1 ,  0.1 ,  0.1 ,  0.1 ,  0.1 ,  0.05],
    [ 0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ],
]) + 5.1
QUEEN_POS_VALUES = array([
    [-0.2 , -0.1 , -0.1 , -0.05, -0.05, -0.1 , -0.1 , -0.2 ],
    [-0.1 ,  0.0 ,  0.05,  0.0 ,  0.0 ,  0.0 ,  0.0 , -0.1 ],
    [-0.1 ,  0.05,  0.05,  0.05,  0.05,  0.05,  0.0 , -0.1 ],
    [ 0.0 ,  0.0 ,  0.05,  0.05,  0.05,  0.05,  0.0 , -0.05],
    [-0.05,  0.0 ,  0.05,  0.05,  0.05,  0.05,  0.0 , -0.05],
    [-0.1 ,  0.0 ,  0.05,  0.05,  0.05,  0.05,  0.0 , -0.1 ],
    [-0.1 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.0 , -0.1 ],
    [-0.2 , -0.1 , -0.1 , -0.05, -0.05, -0.1 , -0.1 , -0.2 ],
]) + 8.8
KING_POS_VALUES = array([
    [ 0.2 ,  0.3 ,  0.1 ,  0.0 ,  0.0 ,  0.1 ,  0.3 ,  0.2 ],
    [ 0.2 ,  0.2 ,  0.0 ,  0.0 ,  0.0 ,  0.0 ,  0.2 ,  0.2 ],
    [-0.1 , -0.2 , -0.2 , -0.2 , -0.2 , -0.2 , -0.2 , -0.1 ],
    [-0.2 , -0.3 , -0.3 , -0.4 , -0.4 , -0.3 , -0.3 , -0.2 ],
    [-0.3 , -0.4 , -0.4 , -0.5 , -0.5 , -0.4 , -0.4 , -0.3 ],
    [-0.3 , -0.4 , -0.4 , -0.5 , -0.5 , -0.4 , -0.4 , -0.3 ],
    [-0.3 , -0.4 , -0.4 , -0.5 , -0.5 , -0.4 , -0.4 , -0.3 ],
    [-0.3 , -0.4 , -0.4 , -0.5 , -0.5 , -0.4 , -0.4 , -0.3 ],
])

_POS_VALUES = [PAWN_POS_VALUES, KNIGHT_POS_VALUES, BISHOP_POS_VALUES,
               ROOK_POS_VALUES, QUEEN_POS_VALUES, KING_POS_VALUES]
POS_VALUES = [
    [VALUES[::-1, :] for VALUES in _POS_VALUES],
    _POS_VALUES,
]


# Stockfish does 70m/s
def eval_board(board):  # 25k/s
    if board.is_checkmate():
        return -inf if board.turn else inf
    elif board.is_game_over():
        return 0

    weight = 0

    occupied = board.occupied_co[WHITE]
    values = POS_VALUES[WHITE]
    weight += ((board.pawns & occupied) * values[PAWN]).sum()
    weight += ((board.knights & occupied) * values[KNIGHT]).sum()
    weight += ((board.bishops & occupied) * values[BISHOP]).sum()
    weight += ((board.rooks & occupied) * values[ROOK]).sum()
    weight += ((board.queens & occupied) * values[QUEEN]).sum()
    weight += ((board.kings & occupied) * values[KING]).sum()

    occupied = board.occupied_co[BLACK]
    values = POS_VALUES[BLACK]
    weight -= ((board.pawns & occupied) * values[PAWN]).sum()
    weight -= ((board.knights & occupied) * values[KNIGHT]).sum()
    weight -= ((board.bishops & occupied) * values[BISHOP]).sum()
    weight -= ((board.rooks & occupied) * values[ROOK]).sum()
    weight -= ((board.queens & occupied) * values[QUEEN]).sum()
    weight -= ((board.kings & occupied) * values[KING]).sum()

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

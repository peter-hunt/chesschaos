from functools import lru_cache
from math import inf
from random import choice as random_choice

from chess import (
    BB_SQUARES, WHITE, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING)
from chess import Board
from chess.polyglot import zobrist_hash as hash_board
Board.__hash__ = hash_board

from constants import POS_VALUES, OPENINGS


__all__ = [
    'eval_board', 'search_openings', 'move_engine']


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

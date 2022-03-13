from chess import (
    STARTING_FEN, COLOR_NAMES, PIECE_NAMES, BB_SQUARES,
    WHITE, BLACK,
    PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING)
from chess import Board, Move
from chess.polyglot import zobrist_hash as hash_board
Board.__hash__ = hash_board

from pygame.constants import (
    MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT)
from pygame.display import flip as display_flip, set_caption, set_icon, set_mode
from pygame.draw import circle as draw_circle
from pygame.event import get as get_event
from pygame.font import Font
from pygame.image import load as load_image
from pygame.mouse import get_pos as get_mouse_pos, get_pressed as get_mouse_pressed
from pygame.transform import scale
from pygame import Rect, init as pygame_init

from math import ceil
from os.path import join, split

from bot import move_engine
from constants import *
from function import get_surface
from level import get_level_name, get_level
from numchess import *


__all__ = ['Game']


pygame_init()

PIECES = []

folder = split(__file__)[0]
for piece_color in COLOR_NAMES:
    for piece_type in PIECE_NAMES[1:]:
        PIECES.append(load_image(
            join(folder, 'assets', f'{piece_color}-{piece_type}.png')))

ICON = load_image(join(folder, 'assets', 'icon.png'))
FONT = Font(join(folder, 'assets', 'ComicSans.ttf'), 64)


class Game:
    def __init__(self, level_selected=0, deck=list[Piece]):
        self.size = DEFAULT_WINDOW_SIZE
        self.screen = get_surface(self.size)

        self.drag_rank = self.drag_file = -1
        self.drag_xpad = self.drag_ypad = 0

        self.board = get_level(level_selected)

        for rank in range(len(deck) // 8):
            for file in range(8):
                piece = deck[rank * 8 + file]
                if piece is not None:
                    self.board.set_piece_at((rank, file), piece)
        king_file = self.board.king(WHITE)[1]
        for i in range(king_file - 1, 8):
            if (self.board.rooks & BB_RANK_1 & BB_FILES[i]).any():
                self.board.castling_rights |= BB_RANK_1 & BB_FILES[i]
                break
        for i in range(king_file - 1, -1, -1):
            if (self.board.rooks & BB_RANK_1 & BB_FILES[i]).any():
                self.board.castling_rights |= BB_RANK_1 & BB_FILES[i]
                break

        self.level_selected = level_selected
        self.promotion_from_square = -1
        self.promotion_square = -1
        self.promotion_pressed = -1
        self.player_turn = self.board.turn

    def update(self, size=None):
        width, height = self.size if size is None else size

        if width / height < 1.3:
            height = width / 1.3
        elif width / height > 1.8:
            height = width / 1.8

        self.size = width, height
        self.screen = get_surface(self.size)
        rect_size = min(self.size)
        board_size = rect_size * 0.8
        self.block_size = block_size = rect_size * 0.1
        self.board_rect = Rect(
            (width - board_size) / 2, (height - board_size) / 2,
            board_size, board_size)

        self.pieces = []
        for image in PIECES:
            self.pieces.append(
                scale(image, (block_size, block_size)))

        self.board_base = get_surface((board_size, board_size), LIGHT_SQUARE_COLOR)
        dark_square = get_surface((block_size, block_size), DARK_SQUARE_COLOR)
        for rank in range(8):
            for file in range(8):
                if (rank + file) % 2 == 0:
                    self.board_base.blit(
                        dark_square, (file * block_size,
                                      (7 - rank) * block_size))

        self.light_move = get_surface((block_size, block_size), (0, 0, 0, 0))
        draw_circle(self.light_move, (14, 14, 14, 25),
                    (block_size / 2, block_size / 2), block_size / 6)

        self.light_capture = get_surface((block_size, block_size), (0, 0, 0, 0))
        draw_circle(self.light_capture, (14, 14, 14, 25),
                    (block_size / 2, block_size / 2), block_size * 0.5)
        draw_circle(self.light_capture, (0, 0, 0, 0),
                    (block_size / 2, block_size / 2), block_size * 0.375)

        self.dark_move = get_surface((block_size, block_size), (0, 0, 0, 0))
        draw_circle(self.dark_move, (14, 14, 14, 25),
                    (block_size / 2, block_size / 2), block_size / 6)

        self.dark_capture = get_surface((block_size, block_size), (0, 0, 0, 0))
        draw_circle(self.dark_capture, (14, 14, 14, 25),
                    (block_size / 2, block_size / 2), block_size * 0.5)
        draw_circle(self.dark_capture, (0, 0, 0, 0),
                    (block_size / 2, block_size / 2), block_size * 0.375)

        self.white_promotion = get_surface((block_size, block_size * 4), (255, 255, 255, 255))
        for i, piece in enumerate((QUEEN, KNIGHT, ROOK, BISHOP)):
            self.white_promotion.blit(self.pieces[piece + 5], (0, block_size * i))

        self.black_promotion = get_surface((block_size, block_size * 4), (255, 255, 255, 255))
        for i, piece in enumerate((BISHOP, ROOK, KNIGHT, QUEEN)):
            self.black_promotion.blit(self.pieces[piece - 1], (0, block_size * i))

        self.update_menu()

    def update_menu(self):
        self.level_text_num = FONT.render(
            f'Level {self.level_selected + 1}', 0, (255, 255, 255))
        self.level_text_name = FONT.render(
            get_level_name(self.level_selected), 0, (255, 255, 255))
        outcome = self.board.outcome()
        if outcome is not None:
            if outcome.winner == self.player_turn:
                text = 'You won'
            elif outcome.winner == (not self.player_turn):
                text = 'You lost'
            elif self.board.is_stalemate():
                text = 'Stalemate Draw'
            elif self.board.is_insufficient_material():
                text = 'Insufficient Material Draw'
            elif self.board.is_seventyfive_moves():
                text = '75 Moves Draw'
            elif self.board.is_fivefold_repetition():
                text = 'Repetition Draw'
            else:
                text = "It's a draw"
            self.level_text_winner = FONT.render(text, 0, (255, 255, 255))
        else:
            self.level_text_winner = None
        screen_height = self.screen.get_height()
        max_width, max_height = self.board_rect.left * 0.8, screen_height * 3 / 50

        width, height = self.level_text_num.get_size()
        self.level_text_num = scale(
            self.level_text_num,
            (width * max_height / height, max_height))
        if self.level_text_num.get_width() > max_width:
            width, height = self.level_text_num.get_size()
            self.level_text_num = scale(
                self.level_text_num,
                (max_width, height * max_width / width))

        width, height = self.level_text_name.get_size()
        self.level_text_name = scale(
            self.level_text_name,
            (width * max_height / height, max_height))
        if self.level_text_name.get_width() > max_width:
            width, height = self.level_text_num.get_size()
            self.level_text_name = scale(
                self.level_text_name,
                (max_width, height * max_width / width))

        if self.level_text_winner is not None:
            width, height = self.level_text_winner.get_size()
            self.level_text_winner = scale(
                self.level_text_winner,
                (width * max_height / height, max_height))
            if self.level_text_winner.get_width() > max_width:
                width, height = self.level_text_winner.get_size()
                self.level_text_winner = scale(
                    self.level_text_winner,
                    (max_width, height * max_width / width))

    def draw_piece(self, piece_type, color, rank, file):
        self.screen.blit(self.pieces[piece_type + color * 6],
                         (self.board_rect.left + file * self.block_size,
                          self.board_rect.top + (7 - rank) * self.block_size))

    def draw_board(self):
        xpad, ypad = self.board_rect.left, self.board_rect.top
        self.screen.blit(self.board_base, (xpad, ypad))
        if len(self.board.move_stack) != 0:
            last_move = self.board.move_stack[-1]
            from_rank, from_file = divmod(last_move.from_square, 8)
            to_rank, to_file = divmod(last_move.to_square, 8)
            from_color = (DARK_MOVE_COLOR if (from_rank + from_file) % 2 == 0
                          else LIGHT_MOVE_COLOR)
            to_color = (DARK_MOVE_COLOR if (to_rank + to_file) % 2 == 0
                        else LIGHT_MOVE_COLOR)
            self.screen.blit(
                get_surface((self.block_size, self.block_size), from_color),
                (xpad + from_file * self.block_size,
                 ypad + (7 - from_rank) * self.block_size))
            self.screen.blit(
                get_surface((self.block_size, self.block_size), to_color),
                (xpad + to_file * self.block_size,
                 ypad + (7 - to_rank) * self.block_size))

        drag_square = self.drag_rank * 8 + self.drag_file
        for square in range(64):
            if square == drag_square:
                continue
            piece = self.board.piece_at(square)
            if piece is None:
                continue
            self.draw_piece(piece.piece_type - 1, piece.color,
                            square // 8, square % 8)

        if self.drag_rank != -1:
            mx, my = get_mouse_pos()

            for move in self.board.generate_legal_moves(
                    from_mask=BB_SQUARES[self.drag_rank * 8 + self.drag_file]):
                square = move.to_square
                mask = BB_SQUARES[square]
                if (square // 8 + square % 8) % 2 == 0:
                    if self.board.occupied_co[not self.board.turn] & mask:
                        surface = self.dark_capture
                    else:
                        surface = self.dark_move
                else:
                    if self.board.occupied_co[not self.board.turn] & mask:
                        surface = self.light_capture
                    else:
                        surface = self.light_move
                self.screen.blit(
                    surface, (xpad + (square % 8) * self.block_size,
                              ypad + (7 - square // 8) * self.block_size))

            piece = self.board.piece_at(self.drag_rank * 8 + self.drag_file)
            self.screen.blit(
                self.pieces[piece.piece_type - 1 + piece.color * 6],
                (mx - self.drag_xpad, my - self.drag_ypad))

        if self.promotion_square != -1:
            promotion_rank, promotion_file = divmod(self.promotion_square, 8)
            if promotion_rank == 0:
                self.screen.blit(
                    self.black_promotion,
                    (xpad + promotion_file * self.block_size,
                     ypad + 4 * self.block_size))
            else:
                self.screen.blit(
                    self.white_promotion,
                    (xpad + promotion_file * self.block_size, ypad))

    def draw_menu(self):
        screen_width, screen_height = self.screen.get_size()
        text_width, text_height = self.level_text_num.get_size()
        xpad = screen_width - (self.board_rect.left - text_width) / 2 - text_width
        ypad = (screen_height * 2 / 10
                + (screen_height * 3 / 50 - text_height) / 2)
        self.screen.blit(self.level_text_num, (xpad, ypad))

        text_width, text_height = self.level_text_name.get_size()
        xpad = screen_width - (self.board_rect.left - text_width) / 2 - text_width
        ypad = (screen_height * 3 / 10
                + (screen_height * 3 / 50 - text_height) / 2)
        self.screen.blit(self.level_text_name, (xpad, ypad))

        if self.level_text_winner is not None:
            text_width, text_height = self.level_text_winner.get_size()
            xpad = screen_width - (self.board_rect.left - text_width) / 2 - text_width
            ypad = (screen_height * 4 / 10
                    + (screen_height * 3 / 50 - text_height) / 2)
            self.screen.blit(self.level_text_winner, (xpad, ypad))

    def draw(self):
        self.screen.fill((0, 0, 0, 0))
        self.draw_board()
        self.draw_menu()

    def play_move(self, move):
        if self.board.is_legal(move):
            self.board.push(move)
            if self.board.is_game_over():
                self.update_menu()
            else:
                self.draw()
                bot_move = move_engine(self.board)
                self.board.push(bot_move)
                if self.board.is_game_over():
                    self.update_menu()

    def _lmb_up(self):
        self.drag_rank = -1
        self.drag_file = -1
        self.drag_xpad = 0
        self.drag_ypad = 0
        self.promotion_from_square = -1
        self.promotion_square = -1
        self.promotion_pressed = -1

    def tick(self):
        pass

    def on_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button != 1:
                return
            mx, my = event.pos
            if self.board_rect.collidepoint(mx, my) and not self.board.is_game_over():
                rank = int((self.block_size * 8 - (my - self.board_rect.top))
                            // self.block_size)
                file = int((mx - self.board_rect.left)
                            // self.block_size)
                if self.promotion_square != -1:
                    p_rank, p_file = divmod(self.promotion_square, 8)
                    if file == p_file and p_rank - 3 <= rank <= p_rank + 3:
                        self.promotion_pressed = abs(rank - p_rank)
                    else:
                        self.promotion_square = -1
                    return
                piece = self.board.piece_at(rank * 8 + file)
                if piece is not None and piece.color == self.board.turn == self.player_turn:
                    self.drag_rank = rank
                    self.drag_file = file
                    self.drag_xpad = (
                        mx - (self.board_rect.left + file * self.block_size))
                    self.drag_ypad = (
                        my - (self.board_rect.top + (7 - rank) * self.block_size))
                return


        elif event.type == MOUSEBUTTONUP:
            if event.button != 1:
                return
            mx, my = event.pos
            if self.promotion_pressed != -1:
                rank = int((self.block_size * 8 - (my - self.board_rect.top))
                            // self.block_size)
                file = int((mx - self.board_rect.left)
                            // self.block_size)
                p_rank, p_file = divmod(self.promotion_square, 8)
                pressed = self.promotion_pressed
                if file == p_file and rank in {p_rank + pressed, p_rank - pressed}:
                    move = Move(self.promotion_from_square, self.promotion_square,
                                promotion=(QUEEN, KNIGHT, ROOK, BISHOP)[pressed])
                    self.play_move(move)
                self.promotion_from_square = -1
                self.promotion_square = -1
                self.promotion_pressed = -1
                self._lmb_up()
                return
            if self.drag_rank != -1 and self.board_rect.collidepoint(mx, my):
                rank = int((self.block_size * 8 - (my - self.board_rect.top))
                            // self.block_size)
                file = int((mx - self.board_rect.left)
                            // self.block_size)
                from_square = self.drag_rank * 8 + self.drag_file
                to_square = rank * 8 + file
                if from_square != to_square:
                    if rank in {0, 7} and self.board.piece_type_at(from_square) == PAWN:
                        for piece in (QUEEN, KNIGHT, ROOK, BISHOP):
                            move = Move(from_square, to_square, promotion=piece)
                            if not self.board.is_legal(move):
                                continue
                            self.drag_rank = -1
                            self.drag_file = -1
                            self.drag_xpad = 0
                            self.drag_ypad = 0
                            self.menu_pressed = -1

                            self.promotion_from_square = from_square
                            self.promotion_square = to_square
                            self.promotion_pressed = -1
                            return
                        self._lmb_up()
                        return
                    move = Move(from_square, to_square)
                    self.play_move(move)
            self._lmb_up()

    def run(self):
        self.size = self.screen.get_size()
        self.update(self.size)

        while True:
            self.draw()
            self.tick()

            for event in get_event():
                if event.type == QUIT:
                    return
                self.on_event(event)

            size = self.screen.get_size()
            if size != self.size:
                self.size == size
                self.update(size)

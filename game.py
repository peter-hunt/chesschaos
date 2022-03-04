from pygame.constants import (
    MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT,
    RESIZABLE)

from pygame.display import flip as display_flip, set_caption, set_icon, set_mode
from pygame.draw import circle as draw_circle
from pygame.event import get as get_event
from pygame.font import Font
from pygame.image import load as load_image
from pygame.mouse import get_pos as get_mouse_pos, get_pressed as get_mouse_pressed
from pygame.transform import scale
from pygame import Rect, Surface, init as pygame_init

from chess import (
    STARTING_FEN, COLOR_NAMES, PIECE_NAMES, BB_SQUARES,
    WHITE, BLACK,
    PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING)
from chess import Board, Move
from chess.polyglot import zobrist_hash as hash_board
Board.__hash__ = hash_board

from math import ceil
from os.path import join, split

from constants import *
from engine import move_engine


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
    def __init__(self):
        self.screen_size = DEFAULT_WINDOW_SIZE
        self.board = Board(CLASSIC_LEVELS[0][1])
        self.screen = set_mode(self.screen_size, RESIZABLE)
        set_icon(ICON)
        set_caption('Chess++')

        self.drag_rank = self.drag_file = -1
        self.drag_xpad = self.drag_ypad = 0

        self.level_selected = 0
        self.level_fen = CLASSIC_LEVELS[0][1]
        self.menu_pressed = -1
        self.menu_page = 0
        self.promotion_from_square = -1
        self.promotion_square = -1
        self.promotion_pressed = -1
        self.player_turn = WHITE

    def update(self, size=None):
        width, height = self.size if size is None else size

        if width / height < 1.3:
            height = width / 1.3
            self.screen = set_mode((width, height), RESIZABLE)
        elif width / height > 1.8:
            height = width / 1.8
            self.screen = set_mode((width, height), RESIZABLE)

        self.screen_size = width, height
        rect_size = min(width, height)
        board_size = rect_size * 0.8
        self.block_size = block_size = rect_size * 0.1
        self.board_rect = Rect(
            (width - board_size) / 2, (height - board_size) / 2,
            board_size, board_size)

        self.pieces = []
        for image in PIECES:
            self.pieces.append(
                scale(image, (block_size, block_size)))

        self.board_base = Surface((board_size, board_size))
        self.board_base.fill(LIGHT_SQUARE_COLOR)
        dark_square = Surface((block_size, block_size))
        dark_square.fill(DARK_SQUARE_COLOR)
        for rank in range(8):
            for file in range(8):
                if (rank + file) % 2 == 0:
                    self.board_base.blit(
                        dark_square, (file * block_size,
                                      (7 - rank) * block_size))

        menu_xpad, menu_ypad = self.board_rect.left * 0.1, height * 0.05
        menu_width, menu_height = self.board_rect.left * 0.8, height * 0.9
        self.menu_rect = Rect(menu_xpad, menu_ypad, menu_width, menu_height)
        self.menu_rects = []
        self.menu_rects.append(
            Rect(menu_xpad + menu_width * 0.2,
                 menu_ypad + menu_height / 48,
                 menu_width * 0.6, menu_height / 24))
        for index in range(max(min(len(CLASSIC_LEVELS) - 10 * self.menu_page, 10), 0)):
            self.menu_rects.append(
                Rect(menu_xpad + menu_width * 0.1,
                     menu_ypad + menu_height * (6 + index * 5) / 60,
                     menu_width * 0.8, menu_height / 18))
        self.menu_rects.append(
            Rect(menu_xpad + menu_width * 0.2,
                 menu_ypad + menu_height * 45 / 48,
                 menu_width * 0.6, menu_height / 24))
        self.menu_surfaces = []
        for rect in self.menu_rects:
            surface = Surface(rect[2:])
            surface.fill(BACKGROUND_COLOR)
            self.menu_surfaces.append(surface)

        self.light_move = Surface(
            (block_size, block_size)).convert_alpha()
        self.light_move.fill((0, 0, 0, 0))
        draw_circle(self.light_move, (14, 14, 14, 25),
                    (block_size / 2, block_size / 2), block_size / 6)

        self.light_capture = Surface(
            (block_size, block_size)).convert_alpha()
        self.light_capture.fill((0, 0, 0, 0))
        draw_circle(self.light_capture, (14, 14, 14, 25),
                    (block_size / 2, block_size / 2), block_size * 0.5)
        draw_circle(self.light_capture, (0, 0, 0, 0),
                    (block_size / 2, block_size / 2), block_size * 0.375)

        self.dark_move = Surface(
            (block_size, block_size)).convert_alpha()
        self.dark_move.fill((0, 0, 0, 0))
        draw_circle(self.dark_move, (14, 14, 14, 25),
                    (block_size / 2, block_size / 2), block_size / 6)

        self.dark_capture = Surface(
            (block_size, block_size)).convert_alpha()
        self.dark_capture.fill((0, 0, 0, 0))
        draw_circle(self.dark_capture, (14, 14, 14, 25),
                    (block_size / 2, block_size / 2), block_size * 0.5)
        draw_circle(self.dark_capture, (0, 0, 0, 0),
                    (block_size / 2, block_size / 2), block_size * 0.375)

        self.white_promotion = Surface(
            (block_size, block_size * 4)).convert_alpha()
        self.white_promotion.fill((255, 255, 255, 255))
        for i, piece in enumerate((QUEEN, KNIGHT, ROOK, BISHOP)):
            self.white_promotion.blit(self.pieces[piece + 5],
                                      (0, block_size * i))

        self.black_promotion = Surface(
            (block_size, block_size * 4)).convert_alpha()
        self.black_promotion.fill((255, 255, 255, 255))
        for i, piece in enumerate((BISHOP, ROOK, KNIGHT, QUEEN)):
            self.black_promotion.blit(self.pieces[piece - 1],
                                      (0, block_size * i))

        self.update_menu()

    def update_menu(self):
        self.menu_surface = Surface(self.menu_rect[2:])
        self.menu_surface.fill(MENU_COLOR)

        self.level_text_num = FONT.render(
            f'Level {self.level_selected + 1}', 0, (255, 255, 255))
        self.level_text_name = FONT.render(
            CLASSIC_LEVELS[self.level_selected][0], 0, (255, 255, 255))
        outcome = self.board.outcome()
        if outcome is not None:
            if outcome.winner == self.player_turn:
                text = 'You won.'
            elif outcome.winner == (not self.player_turn):
                text = 'You lost.'
            elif self.board.is_stalemate():
                text = 'Stalemate Draw'
            elif self.board.is_insufficient_material():
                text = 'Insufficient Material Draw'
            elif self.board.is_seventyfive_moves():
                text = '75 Moves Draw'
            elif self.board.is_fivefold_repetition():
                text = 'Repetition Draw'
            else:
                text = "It's a draw."
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
            self.level_text_num = scale(
                self.level_text_num,
                (max_width, self.level_text_num.get_width() * max_width / max_height))

        width, height = self.level_text_name.get_size()
        self.level_text_name = scale(
            self.level_text_name,
            (width * max_height / height, max_height))
        if self.level_text_name.get_width() > max_width:
            self.level_text_name = scale(
                self.level_text_name,
                (max_width, self.level_text_name.get_width() * max_width / max_height))

        if self.level_text_winner is not None:
            width, height = self.level_text_winner.get_size()
            self.level_text_winner = scale(
                self.level_text_winner,
                (width * max_height / height, max_height))
            if self.level_text_winner.get_width() > max_width:
                self.level_text_winner = scale(
                    self.level_text_winner,
                    (max_width, self.level_text_winner.get_width() * max_width / max_height))

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
            from_square = Surface((self.block_size, self.block_size))
            from_square.fill(
                DARK_MOVE_COLOR if (from_rank + from_file) % 2 == 0
                else LIGHT_MOVE_COLOR)
            to_square = Surface((self.block_size, self.block_size))
            to_square.fill(
                DARK_MOVE_COLOR if (to_rank + to_file) % 2 == 0
                else LIGHT_MOVE_COLOR)
            self.screen.blit(
                from_square, (xpad + from_file * self.block_size,
                              ypad + (7 - from_rank) * self.block_size))
            self.screen.blit(
                to_square, (xpad + to_file * self.block_size,
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
        self.screen.blit(self.menu_surface, self.menu_rect)
        for i, (rect, surface) in enumerate(
                zip(self.menu_rects, self.menu_surfaces)):
            width, height = rect[2:]
            index = i - 1

            if i == 0 or i == len(self.menu_rects) - 1:
                is_selected = False
            else:
                is_selected = index + 10 * self.menu_page == self.level_selected
            is_pressed = index == (self.menu_pressed - 1)
            if i == 0:
                is_pressed |= self.menu_page == 0
            elif i == len(self.menu_rects) - 1:
                is_pressed |= (
                    self.menu_page == ceil(len(CLASSIC_LEVELS) / 10) - 1)
            color_tune = is_selected - is_pressed
            self.screen.blit(surface, rect[:2])
            if color_tune != 0:
                color_mask = Surface((width, height)).convert_alpha()
                color_mask.fill((255, 255, 255, 30) if color_tune == 1
                                else (0, 0, 0, 30))
                self.screen.blit(color_mask, rect[:2])

            text_mask = Surface((width, height)).convert_alpha()
            text_mask.fill((0, 0, 0, 0))

            level = index + 10 * self.menu_page + 1
            if i == 0:
                content = 'Last Page'
            elif i == len(self.menu_rects) - 1:
                content = 'Next Page'
            else:
                content = f'Level {level}'
            text = FONT.render(content, 0, (255, 255, 255))
            max_width, max_height = width * 4 / 5, height * 3 / 4
            text_width, text_height = text.get_size()
            text = scale(
                text, (text_width * max_height / text_height, max_height))
            if text.get_width() > max_width:
                text = scale(
                    text, (max_width, text.get_width() * max_width / max_height))

            text_width, text_height = text.get_size()
            text_mask.blit(text, ((width - text_width) / 2,
                                  (height - text_height) / 2))
            self.screen.blit(text_mask, rect[:2])

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
        self.screen.fill(BACKGROUND_COLOR)
        self.draw_board()
        self.draw_menu()
        display_flip()

    def play_move(self, move):
        if self.board.is_legal(move):
            self.board.push(move)
            if self.board.is_game_over():
                self.update_menu()
            else:
                bot_move = move_engine(
                    self.board, use_openings=self.level_fen == STARTING_FEN)
                self.board.push(bot_move)
                if self.board.is_game_over():
                    self.update_menu()

    def _lmb_up(self):
        self.drag_rank = -1
        self.drag_file = -1
        self.drag_xpad = 0
        self.drag_ypad = 0
        self.menu_pressed = -1
        self.promotion_from_square = -1
        self.promotion_square = -1
        self.promotion_pressed = -1

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

            for index, rect in enumerate(self.menu_rects):
                if rect.collidepoint(mx, my):
                    self.menu_pressed = index
                    break

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
            if self.menu_pressed != -1:
                if self.menu_pressed == 0:
                    if self.menu_page != 0:
                        self.menu_page -= 1
                        self.update()
                elif self.menu_pressed == len(self.menu_rects) - 1:
                    if self.menu_page != ceil(len(CLASSIC_LEVELS) / 10) - 1:
                        self.menu_page += 1
                        self.update()
                elif self.menu_pressed - 1 + 10 * self.menu_page != self.level_selected:
                    self.level_selected = self.menu_pressed - 1 + 10 * self.menu_page
                    self.level_fen = CLASSIC_LEVELS[self.level_selected][1]
                    self.board = Board(self.level_fen)
                    self.player_turn = self.board.turn
                    self.update_menu()
            self._lmb_up()

    def run(self):
        display_flip()
        self.size = self.screen.get_size()
        self.update(self.size)

        while True:
            self.draw()

            if get_mouse_pressed()[0]:
                mx, my = get_mouse_pos()
                if not self.menu_rects[self.menu_pressed].collidepoint(mx, my):
                    self.menu_pressed = -1

            for event in get_event():
                if event.type == QUIT:
                    return
                self.on_event(event)

            size = self.screen.get_size()
            if size != self.size:
                self.size == size
                self.update(size)

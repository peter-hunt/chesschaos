from pygame.constants import (
    MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT,
    RESIZABLE,
)

from pygame.display import flip as display_flip, set_caption, set_icon, set_mode
from pygame.draw import circle as draw_circle
from pygame.event import get as get_event
from pygame.image import load as load_image
from pygame.mouse import get_pos as get_mouse_pos
from pygame.transform import scale
from pygame import Surface

from chess import (
    COLORS, COLOR_NAMES, WHITE, BLACK,
    PIECE_TYPES, PIECE_NAMES, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING,
    BB_SQUARES,
    Board, Move,
)

from os.path import join, split

from constants import *


__all__ = ['Game']


PIECES = []

folder = split(__file__)[0]
for piece_color in COLOR_NAMES:
    for piece_type in PIECE_NAMES[1:]:
        PIECES.append(load_image(
            join(folder, 'assets', f'{piece_color}-{piece_type}.png')
        ))

ICON = load_image(join(folder, 'assets', 'icon.png'))


class Game:
    def __init__(self):
        self.size = DEFAULT_WINDOW_SIZE
        self.board = Board()
        self.screen = set_mode(self.size, RESIZABLE)
        set_icon(ICON)
        set_caption('Chess++')

        self.drag_rank = -1
        self.drag_file = -1
        self.drag_xpad = 0
        self.drag_ypad = 0

    def check_resize(self, force_update=False):
        size = self.screen.get_size()
        if force_update or size != self.size:
            width, height = size

            if width / height < 1.3:
                height = width / 1.3
                self.screen = set_mode((width, height), RESIZABLE)
            elif width / height > 1.8:
                height = width / 1.8
                self.screen = set_mode((width, height), RESIZABLE)

            self.size = width, height
            rect_size = min(width, height)
            self.board_size = rect_size * 0.8
            self.block_size = bs = rect_size * 0.1
            self.xpad = (width - bs * 8) / 2
            self.ypad = (height - bs * 8) / 2

            self.pieces = []
            for image in PIECES:
                self.pieces.append(
                    scale(image, (bs, bs))
                )

            self.board_base = Surface((self.board_size, self.board_size))
            self.board_base.fill(LIGHT_SQUARE_COLOR)
            dark_square = Surface((bs, bs))
            dark_square.fill(DARK_SQUARE_COLOR)
            for rank in range(8):
                for file in range(8):
                    if (rank + file) % 2 == 0:
                        self.board_base.blit(
                            dark_square, (file * bs,
                                          (7 - rank) * bs)
                        )

            self.light_move = Surface((bs, bs)).convert_alpha()
            self.light_move.fill((0, 0, 0, 0))
            draw_circle(self.light_move, (14, 14, 14, 25),
                        (bs / 2, bs / 2), bs / 6)
            self.light_capture = Surface((bs, bs)).convert_alpha()
            self.light_capture.fill((0, 0, 0, 0))
            draw_circle(self.light_capture, (14, 14, 14, 25),
                        (bs / 2, bs / 2), bs * 0.5)
            draw_circle(self.light_capture, (0, 0, 0, 0),
                        (bs / 2, bs / 2), bs * 0.375)
            self.dark_move = Surface((bs, bs)).convert_alpha()
            self.dark_move.fill((0, 0, 0, 0))
            draw_circle(self.dark_move, (14, 14, 14, 25),
                        (bs / 2, bs / 2), bs / 6)
            self.dark_capture = Surface((bs, bs)).convert_alpha()
            self.dark_capture.fill((0, 0, 0, 0))
            draw_circle(self.dark_capture, (14, 14, 14, 25),
                        (bs / 2, bs / 2), bs * 0.5)
            draw_circle(self.dark_capture, (0, 0, 0, 0),
                        (bs / 2, bs / 2), bs * 0.375)

    def draw_piece(self, piece_type, color, rank, file):
        self.screen.blit(self.pieces[piece_type + color * 6],
                         (self.xpad + file * self.block_size,
                          self.ypad + (7 - rank) * self.block_size))

    def draw_board(self):
        self.screen.blit(self.board_base, (self.xpad, self.ypad))
        if len(self.board.move_stack) != 0:
            last_move = self.board.move_stack[-1]
            from_rank, from_file = divmod(last_move.from_square, 8)
            to_rank, to_file = divmod(last_move.to_square, 8)
            from_square = Surface((self.block_size, self.block_size))
            from_square.fill(
                DARK_MOVE_COLOR if (from_rank + from_file) % 2 == 0
                else LIGHT_MOVE_COLOR
            )
            to_square = Surface((self.block_size, self.block_size))
            to_square.fill(
                DARK_MOVE_COLOR if (to_rank + to_file) % 2 == 0
                else LIGHT_MOVE_COLOR
            )
            self.screen.blit(
                from_square, (self.xpad + from_file * self.block_size,
                              self.ypad + (7 - from_rank) * self.block_size)
            )
            self.screen.blit(
                to_square, (self.xpad + to_file * self.block_size,
                            self.ypad + (7 - to_rank) * self.block_size)
            )

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
                from_mask=BB_SQUARES[self.drag_rank * 8 + self.drag_file]
            ):
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
                self.screen.blit(surface,
                                 (self.xpad + (square % 8) * self.block_size,
                                  self.ypad + (7 - square // 8) * self.block_size))

            piece = self.board.piece_at(self.drag_rank * 8 + self.drag_file)
            self.screen.blit(
                self.pieces[piece.piece_type - 1 + piece.color * 6],
                (mx - self.drag_xpad, my - self.drag_ypad),
            )

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.draw_board()
        display_flip()

    def run(self):
        display_flip()
        self.check_resize(force_update=True)

        while True:
            self.check_resize()
            self.draw()
            for event in get_event():
                if event.type == QUIT:
                    return
                elif event.type == MOUSEBUTTONDOWN:
                    if self.board.is_game_over():
                        continue
                    mx, my = event.pos
                    if (self.xpad <= mx <= self.xpad + self.board_size
                            and self.ypad <= my <= self.ypad + self.board_size):
                        rank = int((self.board_size - (my - self.ypad))
                                   // self.block_size)
                        file = int((mx - self.xpad)
                                   // self.block_size)
                        piece = self.board.piece_at(rank * 8 + file)
                        if piece is not None and piece.color == self.board.turn:
                            self.drag_rank = rank
                            self.drag_file = file
                            self.drag_xpad = (
                                mx - (self.xpad + file * self.block_size)
                            )
                            self.drag_ypad = (
                                my - (self.ypad + (7 - rank) * self.block_size)
                            )

                elif event.type == MOUSEBUTTONUP:
                    mx, my = event.pos
                    if (self.xpad <= mx <= self.xpad + self.board_size
                            and self.ypad <= my <= self.ypad + self.board_size):
                        rank = int((self.board_size - (my - self.ypad))
                                   // self.block_size)
                        file = int((mx - self.xpad)
                                   // self.block_size)
                        from_square = self.drag_rank * 8 + self.drag_file
                        to_square = rank * 8 + file
                        move = Move(from_square, to_square)
                        if self.board.is_legal(move):
                            self.board.push(move)
                    self.drag_rank = -1
                    self.drag_file = -1
                    self.drag_xpad = 0
                    self.drag_ypad = 0

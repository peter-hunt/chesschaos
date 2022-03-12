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
from bot import move_engine
from game import Game


__all__ = ['Window']


pygame_init()

PIECES = []

folder = split(__file__)[0]
for piece_color in COLOR_NAMES:
    for piece_type in PIECE_NAMES[1:]:
        PIECES.append(load_image(
            join(folder, 'assets', f'{piece_color}-{piece_type}.png')))

ICON = load_image(join(folder, 'assets', 'icon.png'))
FONT = Font(join(folder, 'assets', 'ComicSans.ttf'), 64)


class Window:
    def __init__(self):
        self.size = DEFAULT_WINDOW_SIZE
        self.board = Board(CLASSIC_LEVELS[0][1])
        self.screen = set_mode(self.size, RESIZABLE)
        set_icon(ICON)
        set_caption('ChessChaos')

        self.level_selected = 0
        self.level_fen = CLASSIC_LEVELS[0][1]
        self.menu_pressed = -1
        self.menu_page = 0
        self.game = Game(self.level_selected)
        self.game.update()

    def update(self, size=None):
        if size is not None:
            self.size = size
        width, height = self.size

        if width / height < 1.3:
            height = width / 1.3
            self.screen = set_mode((width, height), RESIZABLE)
        elif width / height > 1.8:
            height = width / 1.8
            self.screen = set_mode((width, height), RESIZABLE)

        self.size = width, height
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
        self.menu_surface = Surface(self.menu_rect[2:])
        self.menu_surface.fill(MENU_COLOR)

        self.game.update(self.size)

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

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.draw_menu()

        self.game.draw()
        self.screen.blit(self.game.screen, (0, 0))

        display_flip()

    def _lmb_up(self):
        self.menu_pressed = -1

    def tick(self):
        if get_mouse_pressed()[0]:
            mx, my = get_mouse_pos()
            if not self.menu_rects[self.menu_pressed].collidepoint(mx, my):
                self.menu_pressed = -1

        self.game.tick()

    def on_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button != 1:
                return
            mx, my = event.pos

            for index, rect in enumerate(self.menu_rects):
                if rect.collidepoint(mx, my):
                    self.menu_pressed = index
                    break

        elif event.type == MOUSEBUTTONUP:
            if event.button != 1:
                return
            mx, my = event.pos

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
                    self.game = Game(self.level_selected)
                    self.game.update()
            self._lmb_up()

        self.game.on_event(event)

    def run(self):
        display_flip()
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

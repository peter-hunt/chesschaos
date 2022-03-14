
from numchess import COLOR_NAMES, PIECE_NAMES

from pygame.constants import (
    MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT, RESIZABLE)
from pygame.display import flip as display_flip, set_caption, set_icon, set_mode
from pygame.event import get as get_event
from pygame.font import Font
from pygame.image import load as load_image
from pygame.mouse import get_pos as get_mouse_pos, get_pressed as get_mouse_pressed
from pygame.transform import scale
from pygame import Rect, init as pygame_init

from json import load as json_load
from math import ceil
from os.path import join, split
from os import walk
from random import choice as random_choice

from constants import *
from function import get_surface
from game import Game
from level import get_level_name, LEVEL_BOARDS
from profile import Profile


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


def get_profiles():
    profiles = []
    for name in next(iter(walk('saves')))[2]:
        if not name.endswith('.json'):
            continue
        try:
            with open(join('saves', name)) as file:
                obj = json_load(file)
            if Profile.is_valid(obj):
                profiles.append((name[:-5], obj.get('last_update', 0)))
        except:
            pass
    return [pair[0] for pair in sorted(
            profiles, key=lambda pair: (-pair[1], pair[0]))]


# list[tuple[name, 1: profile, 0: json, -1: scramble]]
profiles = get_profiles()


class Window:
    def __init__(self):
        self.size = DEFAULT_WINDOW_SIZE
        self.screen = set_mode(self.size, RESIZABLE)
        set_icon(ICON)
        set_caption('ChessChaos')

        self.level_selected = -1
        self.menu_page = 0
        self.menu_button_pressed = -1

        self.profile_page = 0
        if len(profiles) != 0:
            self.profile_selected = 0
        else:
            self.profile_selected = -1
        self.is_profile_pressed = False
        self.is_profile_selected = False
        self.profile_button_pressed = -1

        if len(profiles) != 0:
            self.profile = Profile.load(profiles[0])
        else:
            self.profile = None
        self.game = None
        # self.game.update()

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

        self.board_base = get_surface((board_size, board_size), LIGHT_SQUARE_COLOR)
        dark_square = get_surface((block_size, block_size), DARK_SQUARE_COLOR)
        for rank in range(8):
            for file in range(8):
                if (rank + file) % 2 == 0:
                    self.board_base.blit(
                        dark_square, (file * block_size,
                                      (7 - rank) * block_size))

        mn_xpad, mn_ypad = self.board_rect.left * 0.1, height * 0.05
        mn_width, mn_height = self.board_rect.left * 0.8, height * 0.9
        self.menu_rect = Rect(mn_xpad, mn_ypad, mn_width, mn_height)
        self.menu_button_rects = []
        self.menu_button_rects.append(
            Rect(mn_xpad + mn_width * 0.2, mn_ypad + mn_height / 48,
                 mn_width * 0.6, mn_height / 24))
        if self.profile is not None:
            for index in range(max(min(len(LEVEL_BOARDS) - 10 * self.menu_page, 10), 0)):
                self.menu_button_rects.append(
                    Rect(mn_xpad + mn_width * 0.1,
                        mn_ypad + mn_height * (6 + index * 5) / 60,
                        mn_width * 0.8, mn_height / 18))
        self.menu_button_rects.append(
            Rect(mn_xpad + mn_width * 0.2, mn_ypad + mn_height * 45 / 48,
                 mn_width * 0.6, mn_height / 24))
        self.menu_buttons = []
        for rect in self.menu_button_rects:
            self.menu_buttons.append(get_surface(rect[2:], BACKGROUND_COLOR))
        self.menu_surface = get_surface(self.menu_rect[2:], MENU_COLOR)

        self.update_profile()

        if self.game is not None:
            self.game.update(self.size)

    def update_profile(self):
        width, height = self.size
        board_size = self.board_rect[2]
        pf_xpad, pf_ypad = board_size + self.board_rect.left * 1.1, height * 0.05
        pf_width, pf_height = self.board_rect.left * 0.8, height * 0.9
        self.profile_rect = Rect(pf_xpad, pf_ypad, pf_width, pf_height)
        self.profile_surface = get_surface(self.profile_rect[2:], MENU_COLOR)
        self.profile_toggle_rect = Rect(
            pf_xpad, pf_ypad + pf_height * 0.90,
            pf_width, pf_height * 0.1)
        self.profile_toggle = [
            get_surface(self.profile_toggle_rect[2:], MENU_COLOR),
            get_surface(self.profile_toggle_rect[2:], BACKGROUND_COLOR),
        ]
        profile_texts = [
            FONT.render('Profiles', 0, (255, 255, 255)),
            FONT.render('Close', 0, (255, 255, 255)),
        ]
        text_xpad, text_ypad = (self.profile_toggle_rect.width * 0.1,
                                self.profile_toggle_rect.height * 0.1)
        max_width, max_height = (self.profile_toggle_rect.width * 0.8,
                                 self.profile_toggle_rect.height * 0.75)
        for i in range(2):
            text = profile_texts[i]
            width, height = text.get_size()
            text = scale(text, (width * max_height / height, max_height))
            if text.get_width() > max_width:
                width, height = text.get_size()
                text = scale(text, (max_width, height * max_width / width))
            width, height = text.get_size()
            self.profile_toggle[i].blit(
                text, (text_xpad + (max_width - width) / 2,
                       text_ypad + (max_height - height) / 2))

        self.profile_button_rects = []
        self.profile_buttons = []
        self.profile_button_rects.append(Rect(
            pf_xpad + pf_width * 0.2, pf_ypad + pf_height * 0.02,
            pf_width * 0.6, pf_height * 0.06))
        profile_count = len(profiles) + 1
        for i in range(min(max(0, profile_count - 7 * self.profile_page), 7)):
            self.profile_button_rects.append(Rect(
                pf_xpad + pf_width * 0.1, pf_ypad + pf_height * (0.12 + 0.1 * i),
                pf_width * 0.8, pf_height * 0.06))
        self.profile_button_rects.append(Rect(
            pf_xpad + pf_width * 0.2, pf_ypad + pf_height * 0.82,
            pf_width * 0.6, pf_height * 0.06))
        for rect in self.profile_button_rects:
            self.profile_buttons.append(get_surface(rect[2:], BACKGROUND_COLOR))

    def draw_menu(self):
        self.screen.blit(self.menu_surface, self.menu_rect)
        for i, (rect, surface) in enumerate(
                zip(self.menu_button_rects, self.menu_buttons)):
            width, height = rect[2:]
            index = i - 1
            self.screen.blit(surface, rect[:2])

            if i == 0 or i == len(self.menu_button_rects) - 1:
                is_selected = False
            else:
                is_selected = (index + 10 * self.menu_page) == self.level_selected
            is_pressed = i == self.menu_button_pressed
            if i == 0:
                is_pressed |= self.menu_page == 0
                is_pressed |= self.profile is None
            elif i == len(self.menu_button_rects) - 1:
                is_pressed |= (self.menu_page == ceil(len(LEVEL_BOARDS) / 10) - 1)
                is_pressed |= self.profile is None
            color_tune = is_selected - is_pressed
            if color_tune != 0:
                color = (255, 255, 255, 30) if color_tune == 1 else (0, 0, 0, 30)
                self.screen.blit(get_surface((width, height), color), rect[:2])

            text_mask = get_surface((width, height), (0, 0, 0, 0))

            level = index + 10 * self.menu_page
            if i == 0:
                content = 'Last Page'
            elif i == len(self.menu_button_rects) - 1:
                content = 'Next Page'
            else:
                content = get_level_name(level)
            text = FONT.render(content, 0, (255, 255, 255))
            max_width, max_height = width * 4 / 5, height * 3 / 4
            text_width, text_height = text.get_size()
            text = scale(text, (text_width * max_height / text_height, max_height))
            if text.get_width() > max_width:
                text = scale(text, (max_width, text.get_width() * max_width / max_height))

            text_width, text_height = text.get_size()
            text_mask.blit(text, ((width - text_width) / 2,
                                  (height - text_height) / 2))
            self.screen.blit(text_mask, rect[:2])

    def draw_profile_menu(self):
        if self.is_profile_selected:
            self.screen.blit(self.profile_surface, self.profile_rect)
        profile_button = self.profile_toggle[self.is_profile_selected]
        self.screen.blit(profile_button, self.profile_toggle_rect)
        color_tune = self.is_profile_selected - self.is_profile_pressed
        self.screen.blit(profile_button, self.profile_toggle_rect[:2])
        if color_tune != 0:
            color = (255, 255, 255, 30) if color_tune == 1 else (0, 0, 0, 30)
            self.screen.blit(get_surface(self.profile_toggle_rect[2:], color),
                             self.profile_toggle_rect[:2])

        if not self.is_profile_selected:
            return

        for i, (rect, surface) in enumerate(
                zip(self.profile_button_rects, self.profile_buttons)):
            index = i - 1
            width, height = rect[2:]
            self.screen.blit(surface, rect[:2])
            profile_index = index + 7 * self.profile_page - 1

            if i == 0 or i == len(self.profile_button_rects) - 1:
                is_selected = False
            else:
                is_selected = profile_index == self.profile_selected
            is_pressed = i == self.profile_button_pressed
            if i == 0:
                is_pressed |= self.profile_page == 0
            elif i == len(self.profile_button_rects) - 1:
                is_pressed |= self.profile_page == len(profiles) // 7
            color_tune = is_selected - is_pressed
            if color_tune != 0:
                color = (255, 255, 255, 30) if color_tune == 1 else (0, 0, 0, 30)
                self.screen.blit(get_surface((width, height), color), rect[:2])

            text_mask = get_surface((width, height), (0, 0, 0, 0))

            if i == 0:
                content = 'Last Page'
            elif i == len(self.profile_button_rects) - 1:
                content = 'Next Page'
            elif profile_index == -1:
                content = 'New Profile'
            else:
                content = profiles[profile_index]
            text = FONT.render(content, 0, (255, 255, 255))
            max_width, max_height = width * 0.8, height * 0.75
            text_width, text_height = text.get_size()
            text = scale(text, (text_width * max_height / text_height, max_height))
            if text.get_width() > max_width:
                text = scale(text, (max_width, text.get_width() * max_width / max_height))

            text_width, text_height = text.get_size()
            text_mask.blit(text, ((width - text_width) / 2,
                                  (height - text_height) / 2))
            self.screen.blit(text_mask, rect[:2])

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.draw_profile_menu()
        if self.profile is not None:
            self.draw_menu()
        if self.game is not None:
            self.game.draw()
            self.screen.blit(self.game.screen, (0, 0))

        display_flip()

    def _lmb_up(self):
        self.menu_button_pressed = -1
        self.profile_button_pressed = -1
        self.is_profile_pressed = False

    def tick(self):
        if get_mouse_pressed()[0]:
            mx, my = get_mouse_pos()
            if self.is_profile_pressed:
                if not self.profile_toggle_rect.collidepoint(mx, my):
                    self.is_profile_pressed = False
            if self.menu_button_pressed != -1:
                if not self.menu_button_rects[
                        self.menu_button_pressed].collidepoint(mx, my):
                    self.menu_button_pressed = -1
            if self.profile_button_pressed != -1:
                if not self.profile_button_rects[
                        self.profile_button_pressed].collidepoint(mx, my):
                    self.profile_button_pressed = -1

        if self.game is not None:
            self.game.tick()

    def on_event(self, event):
        global profiles
        if event.type == MOUSEBUTTONDOWN:
            if event.button != 1:
                return
            mx, my = event.pos

            if self.profile_toggle_rect.collidepoint(mx, my):
                self.is_profile_pressed = True
                return
            for index, rect in enumerate(self.menu_button_rects):
                if rect.collidepoint(mx, my):
                    self.menu_button_pressed = index
                    return
            for index, rect in enumerate(self.profile_button_rects):
                if rect.collidepoint(mx, my):
                    self.profile_button_pressed = index
                    return

        elif event.type == MOUSEBUTTONUP:
            if event.button != 1:
                return
            mx, my = event.pos

            if self.is_profile_pressed:
                self.is_profile_selected = not self.is_profile_selected
            if self.menu_button_pressed != -1:
                if self.menu_button_pressed == 0:
                    if self.menu_page != 0:
                        self.menu_page -= 1
                        self.update()
                elif self.menu_button_pressed == len(self.menu_button_rects) - 1:
                    if self.menu_page != ceil(len(LEVEL_BOARDS) / 10) - 1:
                        self.menu_page += 1
                        self.update()
                elif self.menu_button_pressed - 1 + 10 * self.menu_page != self.level_selected:
                    self.level_selected = self.menu_button_pressed - 1 + 10 * self.menu_page
                    self.game = Game(self.level_selected, self.profile.deck)
                    self.game.update()
            if self.profile_button_pressed != -1:
                if self.profile_button_pressed == 0:
                    if self.profile_page != 0:
                        self.profile_page -= 1
                        self.update()
                elif self.profile_button_pressed == len(self.profile_button_rects) - 1:
                    if self.profile_page != len(profiles) // 7:
                        self.profile_page += 1
                        self.update()
                elif self.profile_button_pressed == 1 and self.profile_page == 0:
                    base_name = random_choice(PROFILE_NAMES)
                    name = base_name
                    i = 1
                    while name in profiles:
                        name = f'{base_name} {i}'
                        i += 1
                    if self.profile is not None:
                        self.profile.dump()
                    self.profile = Profile(name)
                    self.profile.dump()
                    profiles = get_profiles()
                    self.profile_selected = 0
                    self.menu_page = 0
                    self.update()
                else:
                    profile_index = self.profile_button_pressed + 7 * self.profile_page - 2
                    if self.profile_selected != profile_index:
                        self.profile_selected = profile_index
                        if self.profile is not None:
                            self.profile.dump()
                        profiles = get_profiles()
                        self.profile = Profile.load(profiles[profile_index])
                        self.menu_page = 0
                        self.update()
            self._lmb_up()

        if self.game is not None:
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

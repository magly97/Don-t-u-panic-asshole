import pygame
import pygame.freetype
from .colors import *
import json
import os
from lib import gamestates

game_config = None
file_exists = os.path.isfile("config/game_config.json")
if file_exists:
    with open("config/game_config.json") as json_file:
        game_config = json.load(json_file)

CONTROLS_FONT = game_config['font'] if game_config is not None else "Arial"
CONTROLS_FONT_SIZE = game_config['controls_font_size'] if game_config is not None else 50
CONTROLS_TITLE_SIZE = game_config['controls_title_size'] if game_config is not None else 70


class Controls:
    def __init__(self, game):
        self.__game = game
        self.__size = self.__game.get_screen().get_size()
        self.__menu = pygame.freetype.SysFont(CONTROLS_FONT, CONTROLS_FONT_SIZE)
        self.__title = pygame.freetype.SysFont(CONTROLS_FONT, CONTROLS_TITLE_SIZE)
        self.__text = pygame.freetype.SysFont(CONTROLS_FONT, CONTROLS_FONT_SIZE)

        self.__title_x = 100
        self.__title_y = self.__size[1] / 8

        self.__first_row_text_y = self.__size[1] / 3 + 160
        self.__first_row_icon_y = self.__size[1] / 3 + 80
        self.__second_row_text_y = self.__size[1] * (3 / 4) + 80

        self.__wsad_length_x = 230
        self.__wsad_length_y = 150
        self.__wsad_icon_x = self.__size[0] / 4 - 80
        self.__wsad_icon_y = self.__size[1] / 3
        self.__wsad_text_x = self.__wsad_icon_x + 60

        self.__key_length = 70

        self.__equip_icon_x = self.__size[0] / 2 - 40
        self.__equip_text_x = self.__equip_icon_x - 60

        self.__use_icon_x = self.__size[0] * (3 / 4) - 170

        self.__escape_icon_x = self.__size[0] * (3 / 4) + 30
        self.__escape_text_x = self.__escape_icon_x - 15

        self.__access_x_length = 390
        self.__access_y_length = 70
        self.__access_icon_x = self.__size[0] / 4 - 160
        self.__access_icon_y = self.__size[1] * (3 / 4)
        self.__access_text_x = self.__access_icon_x + 70

        self.__mouse_length = 140
        self.__mouse_icon_y = self.__size[1] * (3 / 4) - 70

        self.__attack_icon_x = self.__size[0] / 2
        self.__attack_text_x = self.__attack_icon_x + 15

        self.__move_icon_x = self.__size[0] * (3 / 4) - 80
        self.__move_text_x = self.__move_icon_x + 40

        self.__exit_x = self.__size[0] * (5 / 6)
        self.__exit_y = self.__size[1] / 8 + 10
        self.__exit_x_length = 100
        self.__exit_y_length = 40

    def loop(self):

        self.__game.get_screen().fill(WHITE)

        self.__title.render_to(self.__game.get_screen(), (self.__title_x, self.__title_y), "Controls", BLACK)

        self.__text.render_to(self.__game.get_screen(), (self.__wsad_text_x, self.__first_row_text_y), "Move", BLACK)
        pygame.draw.rect(self.__game.get_screen(), BLACK, (self.__wsad_icon_x, self.__wsad_icon_y, self.__wsad_length_x,
                                                           self.__wsad_length_y), 2)

        self.__text.render_to(self.__game.get_screen(), (self.__equip_text_x, self.__first_row_text_y), "Equipment", BLACK)
        pygame.draw.rect(self.__game.get_screen(), BLACK, (self.__equip_icon_x, self.__first_row_icon_y,
                                                           self.__key_length, self.__key_length), 2)

        self.__text.render_to(self.__game.get_screen(), (self.__use_icon_x, self.__first_row_text_y), "Use", BLACK)
        pygame.draw.rect(self.__game.get_screen(), BLACK, (self.__use_icon_x, self.__first_row_icon_y,
                                                           self.__key_length, self.__key_length), 2)

        self.__text.render_to(self.__game.get_screen(), (self.__escape_text_x, self.__first_row_text_y), "Menu", BLACK)
        pygame.draw.rect(self.__game.get_screen(), BLACK, (self.__escape_icon_x, self.__first_row_icon_y,
                                                           self.__key_length, self.__key_length), 2)

        self.__text.render_to(self.__game.get_screen(), (self.__access_text_x, self.__second_row_text_y), "Quick access", BLACK)
        pygame.draw.rect(self.__game.get_screen(), BLACK, (self.__access_icon_x, self.__access_icon_y,
                                                           self.__access_x_length, self.__access_y_length), 2)

        self.__text.render_to(self.__game.get_screen(), (self.__attack_text_x, self.__second_row_text_y), "Attack", BLACK)
        pygame.draw.rect(self.__game.get_screen(), BLACK, (self.__attack_icon_x, self.__mouse_icon_y,
                                                           self.__mouse_length, self.__mouse_length), 2)

        self.__text.render_to(self.__game.get_screen(), (self.__move_text_x, self.__second_row_text_y), "Aim", BLACK)
        pygame.draw.rect(self.__game.get_screen(), BLACK, (self.__move_icon_x, self.__mouse_icon_y,
                                                           self.__mouse_length, self.__mouse_length), 2)

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.__exit_x + self.__exit_x_length > mouse[0] > self.__exit_x \
                and self.__exit_y + self.__exit_y_length > mouse[1] > self.__exit_y:
            self.__menu.render_to(self.__game.get_screen(), (self.__exit_x, self.__exit_y), "Back", GREEN)
            pygame.draw.rect(self.__game.get_screen(), GREEN, (self.__exit_x, self.__exit_y,
                                                               self.__exit_x_length, self.__exit_y_length), 2)
            if click[0]:
                self.__game.set_state(gamestates.MAIN_MENU)
        else:
            self.__menu.render_to(self.__game.get_screen(), (self.__exit_x, self.__exit_y), "Back", BLACK)
            pygame.draw.rect(self.__game.get_screen(), BLACK, (self.__exit_x, self.__exit_y,
                                                               self.__exit_x_length, self.__exit_y_length), 2)


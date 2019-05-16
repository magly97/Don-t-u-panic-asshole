import pygame
import json
import os

from lib import gamestates
from lib import interactive_menu
from lib import colors

game_config = None
file_exists = os.path.isfile("game/config/game_config.json")
if file_exists:
    with open("config/game_config.json") as json_file:
        game_config = json.load(json_file)
FONT_STYLE = game_config['font'] if game_config is not None else "Segoe UI"
FONT_SIZE = game_config['intro_font_size'] if game_config is not None else 50


class ServerList:
    def __init__(self, game):
        self.__menu_title = "Servers"
        self.__game = game
        self.__connector = self.__game.get_connector()
        self.__server_list = None
        self.__active_server = 0
        self.__title = pygame.font.SysFont(FONT_STYLE, FONT_SIZE)
        self.__interactive_menu = interactive_menu.InteractiveMenu(0.25, 0.2, 0.5, 0.6)

    def loop(self):
        events = self.__game.get_events()
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.__game.set_state(gamestates.MAIN_MENU)
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if self.__server_list is not None:
                    self.__active_server = self.__interactive_menu.get_marked_line_index
                    self.__game.set_state(gamestates.GAME)
                    print(self.__active_server)

        self.__generate_view(events)

    def __generate_view(self, events):
        display_surface = pygame.display.get_surface()
        title = self.__title.render("Select game server", True, colors.BLACK)
        title_rect = title.get_rect()
        title_rect.center = (display_surface.get_width() / 2, display_surface.get_height() * 0.1)
        display_surface.blit(title, title_rect)
        self.__interactive_menu.draw(events)

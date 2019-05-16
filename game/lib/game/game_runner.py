import pygame
from lib.game.heroes.main_hero import MainHero
from lib.game.map import Map

IDLE_SPEED = 0


class GameRunner:

    def __init__(self, game_object):
        self.__game = game_object
        self.__main_hero_pos = tuple(map(lambda x: x/2, self.__game.get_screen().get_size()))
        self.__screen = self.__game.get_screen()
        self.__main_hero = MainHero()
        self.__main_hero_horizontal_speed = IDLE_SPEED
        self.__main_hero_vertical_speed = IDLE_SPEED
        self.__map = Map(self.__game)

    def loop(self):
        self.__handle_events()
        self.__transform()
        self.__draw()

    def __handle_events(self):
        for event in self.__game.get_events():
            self.__handle_keydown_events(event)
            self.__handle_keyup_events(event)

    def __handle_keydown_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            self.__main_hero_vertical_speed = -self.__hero_move_converter(self.__main_hero)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            self.__main_hero_vertical_speed = self.__hero_move_converter(self.__main_hero)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            self.__main_hero_horizontal_speed = -self.__hero_move_converter(self.__main_hero)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            self.__main_hero_horizontal_speed = self.__hero_move_converter(self.__main_hero)

    def __handle_keyup_events(self, event):
        if event.type == pygame.KEYUP and (event.key == pygame.K_w or event.key == pygame.K_s):
            self.__main_hero_vertical_speed = IDLE_SPEED
        elif event.type == pygame.KEYUP and (event.key == pygame.K_a or event.key == pygame.K_d):
            self.__main_hero_horizontal_speed = IDLE_SPEED

    def __hero_move_converter(self, hero):
        return hero.get_move_speed() * self.__game.get_delta_time()

    def __transform(self):
        self.__map.change_bias_x(self.__main_hero_horizontal_speed)
        self.__map.change_bias_y(self.__main_hero_vertical_speed)
        self.__main_hero.update_position(self.__main_hero_horizontal_speed, self.__main_hero_vertical_speed)

    def __draw(self):
        self.__map.fill_screen_with_grass()
        self.__screen.blit(self.__main_hero.get_character(), self.__main_hero_pos)

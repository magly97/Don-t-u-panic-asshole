import pygame
from lib.game.heroes.main_hero import MainHero
from lib.game.map import Map
from lib.game.object_generator import ObjectGenerator

IDLE_SPEED = 0


class GameRunner:

    def __init__(self, game_object):
        self.__game = game_object
        self.__main_hero_pos = tuple(map(lambda x: x/2, self.__game.get_screen().get_size()))
        self.__screen = self.__game.get_screen()
        self.__map = Map(self.__game)
        self.__objects = ObjectGenerator.generate_objects()
        self.__objects.sort(key=lambda y: y.get_y())
        self.__main_hero = MainHero(self, game_object)
        self.__main_hero_horizontal_speed = IDLE_SPEED
        self.__main_hero_vertical_speed = IDLE_SPEED

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
            self.__main_hero.set_movement_up()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            self.__main_hero_vertical_speed = self.__hero_move_converter(self.__main_hero)
            self.__main_hero.set_movement_down()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            self.__main_hero_horizontal_speed = -self.__hero_move_converter(self.__main_hero)
            self.__main_hero.set_movement_left()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            self.__main_hero_horizontal_speed = self.__hero_move_converter(self.__main_hero)
            self.__main_hero.set_movement_right()

    def __handle_keyup_events(self, event):
        if event.type == pygame.KEYUP and (event.key == pygame.K_w or event.key == pygame.K_s):
            self.__main_hero_vertical_speed = IDLE_SPEED
            self.__main_hero.reset_direction(event.key)
        elif event.type == pygame.KEYUP and (event.key == pygame.K_a or event.key == pygame.K_d):
            self.__main_hero_horizontal_speed = IDLE_SPEED
            self.__main_hero.reset_direction(event.key)

    def __hero_move_converter(self, hero):
        return hero.get_move_speed() * self.__game.get_delta_time()

    def __transform(self):
        if not self.__main_hero.get_col_flag():
            self.__map.change_bias_x(self.__main_hero_horizontal_speed)
            self.__map.change_bias_y(self.__main_hero_vertical_speed)
        self.__main_hero.update_position(self.__main_hero_horizontal_speed, self.__main_hero_vertical_speed)

    def __draw(self):
        self.__map.fill_screen_with_grass()
        self.__screen.blit(self.__main_hero.get_sprite(), self.__main_hero_pos)
        for world_object in self.__objects:
            self.__screen.blit(world_object.get_sprite(), (world_object.get_x() - self.__main_hero.get_x(),
                                                           world_object.get_y() - self.__main_hero.get_y()))
            # draw collision rect only for testing
            # world_object.draw_collision_rect(self.__game.get_screen(), self.__main_hero.get_x(), self.__main_hero.get_y(),
            #                                  self.__main_hero.get_width(), self.__main_hero.get_height(),
            #                                  self.__main_hero.get_center_x(), self.__main_hero.get_center_y())

    def get_objects(self):
        return self.__objects


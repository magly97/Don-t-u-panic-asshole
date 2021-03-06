import pygame
from lib import gamestates
from lib.game.heroes.main_hero import MainHero
from lib.game.map import Map
from lib.game.object_generator import ObjectGenerator
from lib.config.controllers.controller import Controller
from lib.game.heroes.hero_movement import HeroMovement

IDLE_SPEED = 0
CROSS_SPEED = 0.7071


class GameRunner:

    def __init__(self, game_object):
        self.__game = game_object
        self.__main_hero_pos = tuple(map(lambda x: x / 2, self.__game.get_screen().get_size()))
        self.__screen = self.__game.get_screen()
        self.__screen_size = self.__screen.get_size()
        self.__map = Map(self.__game)
        self.__objects = ObjectGenerator.generate_objects()
        self.__objects.sort(key=lambda y: y.get_y())
        self.__main_hero = MainHero(self, game_object)
        self.__main_hero_horizontal_speed = IDLE_SPEED
        self.__main_hero_vertical_speed = IDLE_SPEED
        self.__eq_slot_sprite = self.__main_hero.get_equipment().get_background()
        self.__eq_slot_width = 64
        self.__marked_slot_sprite = self.__main_hero.get_equipment().get_marked_background()
        self.__1_key_value = 49
        self.__lower_margin = 84
        self.__shift_from_middle = 160
        self.__x_index = 0
        self.__y_index = 1
        self.__movement_events = []

    def loop(self):
        self.__handle_events()
        self.__transform()
        self.__draw()

    def __handle_events(self):
        for event in self.__game.get_events():
            self.__handle_keydown_events(event)
            self.__handle_keyup_events(event)
            self.__handle_number_key_event(event)

    def __handle_keydown_events(self, event):
        if event.type == pygame.KEYDOWN and self.__check_event_type(event) == 'movement':
            self.__movement_events.append(event.key)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.__game.set_state(gamestates.GAME_MENU)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            HeroMovement.movement_up(self.__main_hero, self.__game)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            HeroMovement.movement_down(self.__main_hero, self.__game)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            HeroMovement.movement_left(self.__main_hero, self.__game)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            HeroMovement.movement_right(self.__main_hero, self.__game)

        if self.__movement_events.count(Controller.D.value) > 0\
                and self.__movement_events.count(Controller.W.value) > 0:
            HeroMovement.movement_up_right(self.__main_hero, self.__game)
        elif self.__movement_events.count(Controller.S.value) > 0\
                and self.__movement_events.count(Controller.D.value) > 0:
            HeroMovement.movement_down_right(self.__main_hero, self.__game)
        elif self.__movement_events.count(Controller.A.value) > 0\
                and self.__movement_events.count(Controller.S.value) > 0:
            HeroMovement.movement_down_left(self.__main_hero, self.__game)
        elif self.__movement_events.count(Controller.A.value) > 0\
                and self.__movement_events.count(Controller.W.value) > 0:
            HeroMovement.movement_up_left(self.__main_hero, self.__game)

    def __handle_keyup_events(self, event):
        if event.type == pygame.KEYUP and self.__check_event_type(event) == 'movement':
            self.__movement_events.remove(event.key)
        if event.type == pygame.KEYUP and (event.key == pygame.K_w or event.key == pygame.K_s):
            self.__main_hero.set_vertical_speed(IDLE_SPEED)
            self.__main_hero.reset_direction(event.key)
        elif event.type == pygame.KEYUP and (event.key == pygame.K_a or event.key == pygame.K_d):
            self.__main_hero.set_horizontal_speed(IDLE_SPEED)
            self.__main_hero.reset_direction(event.key)
        if self.__movement_events.count(Controller.W.value) > 0:
            self.__main_hero.set_vertical_speed(-HeroMovement.hero_move_converter(self.__main_hero, self.__game))
        elif self.__movement_events.count(Controller.S.value) > 0:
            self.__main_hero.set_vertical_speed(HeroMovement.hero_move_converter(self.__main_hero, self.__game))
        elif self.__movement_events.count(Controller.A.value) > 0:
            self.__main_hero.set_horizontal_speed(-HeroMovement.hero_move_converter(self.__main_hero, self.__game))
        elif self.__movement_events.count(Controller.D.value) > 0:
            self.__main_hero.set_horizontal_speed(HeroMovement.hero_move_converter(self.__main_hero, self.__game))

    def __hero_move_converter(self, hero):
        return hero.get_move_speed() * self.__game.get_delta_time()

    def __handle_number_key_event(self, event):
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_1 or event.key == pygame.K_2 or
                                             event.key == pygame.K_3 or event.key == pygame.K_4 or
                                             event.key == pygame.K_5):
            value = event.key - self.__1_key_value
            self.__main_hero.get_equipment().mark_item(value)

    def __transform(self):
        if not self.__main_hero.get_col_flag():
            self.__map.change_bias_x(self.__main_hero.get_horizontal_speed())
            self.__map.change_bias_y(self.__main_hero.get_vertical_speed())
        self.__main_hero.update_position(self.__main_hero.get_horizontal_speed(), self.__main_hero.get_vertical_speed())

    def __draw(self):
        self.__map.fill_screen_with_grass()
        self.__screen.blit(self.__main_hero.get_sprite(), self.__main_hero_pos)
        for world_object in self.__objects:
            self.__screen.blit(world_object.get_sprite(),
                               (
                                   world_object.get_x() - self.__main_hero.get_x() + self.__screen_size[
                                       self.__x_index] / 2,
                                   world_object.get_y() - self.__main_hero.get_y()
                                   + self.__screen_size[self.__y_index] / 2))
        marked_index = self.__main_hero.get_equipment().get_marked_index()
        for y in range(0, 5):
            if y == marked_index:
                self.__screen.blit(self.__marked_slot_sprite,
                                   ((self.__screen_size[self.__x_index] / 2) + y * self.__eq_slot_width
                                    - self.__shift_from_middle,
                                    self.__screen_size[self.__y_index] - self.__lower_margin))

            else:
                self.__screen.blit(self.__eq_slot_sprite,
                                   ((self.__screen_size[self.__x_index] / 2) + y * self.__eq_slot_width
                                    - self.__shift_from_middle,
                                    self.__screen_size[self.__y_index] - self.__lower_margin))
            if self.__main_hero.get_equipment().get_item_by_index(y) is not None:
                item_sprite = self.__main_hero.get_equipment()
                item_sprite = item_sprite.get_item_by_index(y)
                item_sprite = item_sprite.get_sprite()
                self.__screen.blit(item_sprite,
                                   ((self.__screen_size[self.__x_index] / 2) + y * self.__eq_slot_width
                                    - self.__shift_from_middle,
                                    self.__screen_size[self.__y_index] - self.__lower_margin))

    def get_objects(self):
        return self.__objects

    def __check_event_type(self, event):
        if event.key == pygame.K_w or event.key == pygame.K_a or event.key == pygame.K_s or event.key == pygame.K_d:
            return 'movement'

    def get_main_hero(self):
        return self.__main_hero

    def get_game(self):
        return self.__game

import pygame
from lib.game.heroes.main_hero import MainHero
from lib.game.map import Map
from lib.game.object_generator import ObjectGenerator
from lib.game.weapons.sword import Sword
from lib.game.weapons.bullet import Bullet

IDLE_SPEED = 0


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
        self.__weapons = []
        self.__sword = None

    def loop(self):
        self.__handle_events()
        self.__transform()
        self.__draw()
        self.__bullets_refresh()

    def __bullets_refresh(self):
        for weapon in self.__weapons:
            if weapon.get_life() != 0:
                weapon.update_x()
                weapon.update_y()
                weapon.update_life()
            else:
                print("puf")
                self.__weapons.pop(self.__weapons.index(weapon))
            for object in self.__objects:
                if object.check_collision_bullet(weapon.get_x(), weapon.get_y(),
                                                 weapon.get_col_width(), weapon.get_col_height()):
                    print("łubudu")
                    if self.__weapons.count(weapon) > 0:
                        self.__weapons.pop(self.__weapons.index(weapon))

    def __handle_events(self):
        for event in self.__game.get_events():
            self.__handle_keydown_events(event)
            self.__handle_keyup_events(event)
            self.__handle_number_key_event(event)

    def __handle_keydown_events(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.selected_weapon(mouse_x, mouse_y)
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
        #     self.selected_weapon(-1, 0)
        # elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
        #     self.selected_weapon(1, 0)
        # elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
        #     self.selected_weapon(0, -1)
        # elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
        #     self.selected_weapon(0, 1)

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

    def __handle_number_key_event(self, event):
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_1 or event.key == pygame.K_2 or
                                             event.key == pygame.K_3 or event.key == pygame.K_4 or
                                             event.key == pygame.K_5):
            value = event.key - self.__1_key_value
            self.__main_hero.get_equipment().mark_item(value)

    def __transform(self):
        if not self.__main_hero.get_col_flag():
            self.__map.change_bias_x(self.__main_hero_horizontal_speed)
            self.__map.change_bias_y(self.__main_hero_vertical_speed)
        self.__main_hero.update_position(self.__main_hero_horizontal_speed, self.__main_hero_vertical_speed)

    def __draw(self):
        self.__map.fill_screen_with_grass()
        self.__screen.blit(self.__main_hero.get_sprite(), self.__main_hero_pos)
        for world_object in self.__objects:
            self.__screen.blit(world_object.get_sprite(),
                               (world_object.get_x() - self.__main_hero.get_x() + self.__screen_size[0] / 2,
                                world_object.get_y() - self.__main_hero.get_y() + self.__screen_size[1] / 2))
            # DON'T REMOVE THAT! NEEDED FOR TEST
            # world_object.draw_collision_rect(self.__screen, self.__main_hero.get_x() - self.__screen_size[0] / 2,
            #                                  self.__main_hero.get_y() - self.__screen_size[1] / 2,
            #                                  self.__main_hero.get_width(), self.__main_hero.get_height(),
            #                                  self.__main_hero.get_center_x(), self.__main_hero.get_center_y())
        for weapon in self.__weapons:
            self.__screen.blit(weapon.get_sprite(), (weapon.get_x() - self.__main_hero.get_x(),
                                                     weapon.get_y() - self.__main_hero.get_y()))

        marked_index = self.__main_hero.get_equipment().get_marked_index()
        for y in range(0, 5):
            if y == marked_index:
                self.__screen.blit(self.__marked_slot_sprite,
                                   ((self.__screen_size[0] / 2) + y * self.__eq_slot_width - self.__shift_from_middle,
                                    self.__screen_size[1] - self.__lower_margin))

            else:
                self.__screen.blit(self.__eq_slot_sprite,
                                   ((self.__screen_size[0] / 2) + y * self.__eq_slot_width - self.__shift_from_middle,
                                    self.__screen_size[1] - self.__lower_margin))
            if self.__main_hero.get_equipment().get_item_by_index(y) is not None:
                item_sprite = self.__main_hero.get_equipment()
                item_sprite = item_sprite.get_item_by_index(y)
                item_sprite = item_sprite.get_sprite()
                self.__screen.blit(item_sprite,
                                   ((self.__screen_size[0] / 2) + y * self.__eq_slot_width - self.__shift_from_middle,
                                    self.__screen_size[1] - self.__lower_margin))

    def get_objects(self):
        return self.__objects

    def selected_weapon(self, horizontal, vertical):
        marked_index = self.__main_hero.get_equipment().get_marked_index()
        marked_item = self.__main_hero.get_equipment().get_item_by_index(marked_index)
        distance = 1
        melee = 0
        if marked_item is not None:
            action = self.__main_hero.get_equipment().get_item_by_index(marked_index).get_action()
        else:
            action = None
        if action == melee:
            self.__weapons.append(
                Sword(self.__main_hero.get_x() + self.__screen_size[0] / 2 + self.__main_hero.get_center_x(),
                      self.__main_hero.get_y() + self.__screen_size[1] / 2 + self.__main_hero.get_center_x(),
                      horizontal, vertical, self.__main_hero.get_center_x(), self.__main_hero.get_center_y(),
                      self.__screen_size))
        elif action == distance:
            self.__weapons.append(
                Bullet(self.__main_hero.get_x() + self.__screen_size[0] / 2 + self.__main_hero.get_center_x(),
                       self.__main_hero.get_y() + self.__screen_size[1] / 2 + self.__main_hero.get_center_x(),
                       horizontal, vertical, self.__main_hero.get_center_x(), self.__main_hero.get_center_y(),
                       self.__screen_size))

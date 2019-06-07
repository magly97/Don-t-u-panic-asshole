import pygame
import math

from game.lib.game.weapons.weapon import Weapon


class Sword(Weapon):
    def __init__(self, x, y, horizontal, vertical, center_x, center_y, screen_size):
        self.__angle = math.atan2(vertical - center_y - screen_size[1] / 2, horizontal - center_x - screen_size[0] / 2)
        self._vel_horizontal = math.cos(self.__angle) * 10
        self._vel_vertical = math.sin(self.__angle) * 10
        self._pos_x = x + 1 * self._vel_horizontal
        self._pos_y = y + 1 * self._vel_vertical
        self._sprite = pygame.transform.scale(pygame.image.load('config/assets/objects/rock1.png'), (50, 50))
        self._time_of_life = 2
        self._collision_width = 50
        self._collision_height = 50


import pygame
import math
from game.lib.game.weapons.weapon import Weapon


class Bullet(Weapon):
    def __init__(self, x, y, horizontal, vertical, center_x, center_y, screen_size):

        self._pos_x = x
        self._pos_y = y
        self.__angle = math.atan2(vertical - center_y - screen_size[1] / 2, horizontal - center_x - screen_size[0] / 2)
        self._vel_horizontal = math.cos(self.__angle) * 10
        self._vel_vertical = math.sin(self.__angle) * 10
        self._sprite = pygame.transform.scale(pygame.image.load('config/assets/objects/rock1.png'), (30, 30))
        self._time_of_life = 100
        self._collision_width = 20
        self._collision_height = 20

import pygame

from game.lib.game.weapons.weapon import Weapon


class Sword(Weapon):
    def __init__(self, x, y, horizontal, vertical):
        self._pos_x = x + 20 * horizontal
        self._pos_y = y + 20 * vertical
        self._vel_horizontal = 5 * horizontal
        self._vel_vertical = 5 * vertical
        self._sprite = pygame.transform.scale(pygame.image.load('config/assets/objects/rock1.png'), (50, 50))
        self._time_of_life = 2
        self._collision_width = 50
        self._collision_height = 50


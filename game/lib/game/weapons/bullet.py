import pygame

from game.lib.game.weapons.weapon import Weapon


class Bullet(Weapon):
    def __init__(self, x, y, horizontal, vertical):
        self._pos_x = x
        self._pos_y = y
        self._vel_horizontal = 8 * horizontal
        self._vel_vertical = 8 * vertical
        self._sprite = pygame.transform.scale(pygame.image.load('config/assets/objects/rock1.png'), (30, 30))
        self._time_of_life = 100
        self._collision_width = 20
        self._collision_height = 20

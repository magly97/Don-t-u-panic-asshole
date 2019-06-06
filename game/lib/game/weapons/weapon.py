class Weapon:
    _pos_x = None
    _pos_y = None
    _vel_horizontal = None
    _vel_vertical = None
    _sprite = None
    _time_of_life = None
    _collision_width = None
    _collision_height = None

    def __init__(self, x, y, horizontal, vertical):
        self._pos_x = x
        self._pos_y = y
        self._vel_horizontal = 20 * horizontal
        self._vel_vertical = 20 * vertical
        self._time_of_life = 100
        self._collision_width = 20
        self._collision_height = 20

    def update_x(self):
        self._pos_x += self._vel_horizontal

    def update_y(self):
        self._pos_y += self._vel_vertical

    def update_life(self):
        self._time_of_life -= 1

    def get_x(self):
        return self._pos_x

    def get_y(self):
        return self._pos_y

    def get_life(self):
        return self._time_of_life

    def get_sprite(self):
        return self._sprite

    def get_col_height(self):
        return self._collision_height

    def get_col_width(self):
        return self._collision_width

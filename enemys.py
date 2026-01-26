import random
import math
import arcade


ANIMATION_SPEED = 0.2


class Enemy(arcade.Sprite):
    def __init__(self, x, y, angle, speed):
        super().__init__()

        self.animation_frame = 0
        self.animation_time = 0
        self.turn = False
        self.textures = []

        self.ran_textures = random.randint(1, 2)
        if self.ran_textures == 1:
            self.textures = [arcade.load_texture("bat.png"),  # вправо, крылья вверх
                             arcade.load_texture("bat_hang.png"),  # вправо, крылья вверх
                             arcade.load_texture("bat.png").flip_horizontally(),  # влево, крылья вверх
                             arcade.load_texture("bat_hang.png").flip_horizontally()]  # влево, крылья вверх
        else:
            self.textures = [arcade.load_texture("ghost.png"),  # вправо, открытый рот
                             arcade.load_texture("ghost_normal.png"),  # вправо, открытый рот
                             arcade.load_texture("ghost.png").flip_horizontally(),  # влево, закрытый рот
                             arcade.load_texture("ghost_normal.png").flip_horizontally()]  # влево, закрытый рот

        self.set_texture(self.animation_frame)
        self.center_x = x
        self.center_y = y
        self.scale = 0.5
        self.speed_enemy = speed
        self.angle_en = angle

    def update(self, delta_time):
        dx = self.speed_enemy * delta_time * math.cos(math.radians(self.angle_en))
        dy = self.speed_enemy * delta_time * math.sin(math.radians(self.angle_en))
        if self.turn:
            dx = dx * -1
            dy = dy * -1
        self.center_x += dx
        self.center_y += dy

        self.animation_time += ANIMATION_SPEED * ANIMATION_SPEED * ANIMATION_SPEED
        if self.animation_time > ANIMATION_SPEED:
            self.animation_time = 0
            if self.turn:
                if self.animation_frame == 0:
                    self.animation_frame = 1
                else:
                    self.animation_frame = 0
            else:
                if self.animation_frame == 2:
                    self.animation_frame = 3
                else:
                    self.animation_frame = 2
        self.set_texture(self.animation_frame)

    def changing_the_direction(self):
        self.turn = not(self.turn)
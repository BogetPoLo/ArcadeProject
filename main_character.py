import arcade
ANIMATION_SPEED = 0.2

class MainCharacter(arcade.Sprite):
    """класс главного игрока"""
    def init(self, keys_pr):
        super().init()
        self.keys_pr = keys_pr

        self.animation_frame = 0
        self.animation_time = 0

        self.textures = [arcade.load_texture("alienGreen.png"),  # стоит
                         arcade.load_texture("alienGreen_walk1.png"),  # бежит влево 1
                         arcade.load_texture("alienGreen_walk2.png"),  # бежит влево 2
                         arcade.load_texture("alienGreen_walk1.png").flip_horizontally(),  # бежит вправо 1
                         arcade.load_texture("alienGreen_walk2.png").flip_horizontally(),  # бежит вправо 2
                         arcade.load_texture("alienGreen_climb1.png"),  # идёт на верх 1
                         arcade.load_texture("alienGreen_climb2.png")]  # идёт на верх 2
        self.set_texture(self.animation_frame)
        self.center_x = 200
        self.center_y = 200
        self.scale = 0.5
        self.speed_player = 250

    def update(self, delta_time):
        dx = 0
        dy = 0
        if arcade.key.A in self.keys_pr:
            dx -= self.speed_player * delta_time
        if arcade.key.D in self.keys_pr:
            dx += self.speed_player * delta_time
        if arcade.key.W in self.keys_pr:
            dy += self.speed_player * delta_time
        if arcade.key.S in self.keys_pr:
            dy -= self.speed_player * delta_time

        if dx != 0 and dy != 0:
            factor = 0.7071  # ≈ 1/√2
            dx *= factor
            dy *= factor

        self.center_x += dx
        self.center_y += dy

        if arcade.key.W in self.keys_pr and self.animation_frame != 6:
            self.animation_frame = 5
        if arcade.key.S in self.keys_pr:
          self.animation_frame = 0
        if arcade.key.A in self.keys_pr and self.animation_frame != 4:
          self.animation_frame = 3
        if arcade.key.D in self.keys_pr and self.animation_frame != 2:
            self.animation_frame = 1
        elif all([True if key not in self.keys_pr else False for key in [arcade.key.A, arcade.key.D, arcade.key.W, arcade.key.S]]):
            self.animation_frame = 0

        self.animation_time += ANIMATION_SPEED * ANIMATION_SPEED * ANIMATION_SPEED
        if self.animation_time > ANIMATION_SPEED:
            self.animation_time = 0
            if self.animation_frame == 5:
                self.animation_frame += 1
            elif self.animation_frame == 6:
                self.animation_frame -= 1

            if self.animation_frame == 1:
                self.animation_frame += 1
            elif self.animation_frame == 2:
                self.animation_frame -= 1

            if self.animation_frame == 3:
                self.animation_frame += 1
            elif self.animation_frame == 4:
                self.animation_frame -= 1
        self.set_texture(self.animation_frame)

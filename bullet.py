import arcade
import math


class Bullet(arcade.Sprite):
    def __init__(self, start_x, start_y, target_x, target_y, speed=800, damage=10):
        super().__init__()
        self.texture = arcade.load_texture("worm_hit.png")
        self.center_x = start_x
        self.center_y = start_y
        self.speed = speed
        self.damage = damage

        x_diff = target_x - start_x
        y_diff = target_y - start_y
        angle = math.atan2(y_diff, x_diff)

        self.change_x = math.cos(angle) * speed
        self.change_y = math.sin(angle) * speed

        self.angle = math.degrees(-angle)

    def update(self, delta_time):
        # Удаляем пулю, если она ушла за экран
        if (self.center_x < 0 or self.center_x > 1620 or
                self.center_y < 0 or self.center_y > 980):
            self.remove_from_sprite_lists()
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time

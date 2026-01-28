import arcade
import random


class DustParticleFromWalking(arcade.SpriteCircle):
    """Частица пыли для эффекта приземления"""
    def __init__(self, x, y):
        color = random.choice([
            (220, 220, 220, 255),  # Очень легкий налет пыли
            (200, 200, 200, 255),  # Едва заметный слой пыли
            (180, 180, 180, 255),  # Светлый след пыли
            (160, 160, 160, 255)  # Легко различимый слой пыли
        ])
        size = random.randint(3, 8)
        super().__init__(size, color)
        self.center_x = x
        self.center_y = y
        self.change_x = random.uniform(-1.5, 1.5)
        self.change_y = random.uniform(0, 2)
        self.scale = 1.0
        self.alpha = 200
        self.lifetime = random.uniform(0.5, 1.2)
        self.time_alive = 0

    def update(self, delta_time):
        # Движение частицы
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Замедление
        self.change_x *= 0.95
        self.change_y *= 0.95

        # Изменение масштаба
        self.scale_x *= 1.02
        self.scale_y *= 1.005

        # Уменьшение прозрачности
        self.alpha -= 2

        # Увеличение времени жизни
        self.time_alive += delta_time

        # Проверка на окончание времени жизни
        if self.time_alive >= self.lifetime:
            return True
        return False
# ! - означает, что эта часть кода не доделана
import math

import arcade
from pyglet.graphics import Batch
from main_character import MainCharacter
from bullet import Bullet


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640

ANIMATION_SPEED = 0.2
CAMERA_LERP = 0.12
DEAD_ZONE_W = int(SCREEN_WIDTH * 0.15)
DEAD_ZONE_H = int(SCREEN_HEIGHT * 0.25)

PRICE_PER_CHEST = {"chest_one_tex": 1, "chest_two_tex": 2, "chest_tree_tex": 3}
SCREEN_TITLE = "Очень крутой рогалик"
KEYS_PRESSED = []


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        "Размер карты: 1620, 980"
        self.name_map = arcade.load_tilemap("arc_map.tmx", scaling=0.5)  # загружаем карту
        self.scene = arcade.Scene.from_tilemap(self.name_map)  # делаем из карты сцены

        "Текстуры"
        self.f_t = self.scene["floor_tex"]
        self.g_t = self.scene["grass_tex"]
        self.w_t = self.scene["wall_tex"]
        self.a_t = self.scene["all_tex"]
        self.ch_o_t = self.scene["chest_one_tex"]
        self.ch_tw_t = self.scene["chest_two_tex"]
        self.ch_tr_t = self.scene["chest_tree_tex"]

        "Коллизии"
        self.w_c = self.scene["wall_coll"]
        self.ch_o_c = self.scene["chest_one_coll"]
        self.ch_tw_c = self.scene["chest_two_coll"]
        self.ch_tr_c = self.scene["chest_tree_coll"]

    def setup(self):
        """обнуляем всё для нового забега"""
        "персонаж"
        self.player = MainCharacter(KEYS_PRESSED)
        self.pl_sp = arcade.SpriteList()
        self.pl_sp.append(self.player)
        "пули"
        self.bullet_list = arcade.SpriteList()
        "камера для игрока"
        self.world_camera = arcade.Camera2D()
        self.world_camera.position = (200, 200)
        "камера для gui"
        self.gui_camera = arcade.Camera2D()

        "физика"
        self.ph_wall = arcade.PhysicsEngineSimple(
            self.player, self.w_c
        )

        "иные переменные"
        self.result_score = 0
        self.life_time = 0.0
        self.result_kill = 0
        self.batch = Batch()

    def on_draw(self):
        """Рисует картинку"""
        self.clear()
        self.world_camera.use()

        self.f_t.draw()
        self.g_t.draw()
        self.w_t.draw()
        self.a_t.draw()
        self.ch_o_t.draw()
        self.ch_tw_t.draw()
        self.ch_tr_t.draw()
        self.pl_sp.draw()

        self.bullet_list.draw()

        self.gui_camera.use()
        text_lifetime = arcade.Text(f"Время жизни: {self.life_time:.2f}", 5, SCREEN_HEIGHT - 30, arcade.color.BLACK, 20, batch=self.batch)
        text_score = arcade.Text(f"Собрано монет: {self.result_score}", 5, SCREEN_HEIGHT - 60, arcade.color.BLACK, 20, batch=self.batch)
        text_kill = arcade.Text(f"Убито врагов: {self.result_kill}", 5, SCREEN_HEIGHT - 90, arcade.color.BLACK, 20, 20, batch=self.batch)
        self.batch.draw()

    def on_update(self, delta_time):
        """Обновляем все элементы"""
        print(self.player.center_x, self.player.center_y)
        "время"
        self.life_time += delta_time
        "Физический движок"
        #  self.ph_wall.update()
        "Позиция игрока"
        self.player.update(delta_time)
        "Позиция пули"
        self.bullet_list.update()

        "проверка на столкновения игрока с бочками"
        for name in PRICE_PER_CHEST:
            for chest in self.scene[name]:
                if arcade.check_for_collision_with_list(chest, self.pl_sp):
                    chest.remove_from_sprite_lists()
                    self.result_score += PRICE_PER_CHEST[name]

        "Камера"
        cam_x, cam_y = self.world_camera.position
        dz_left = cam_x - DEAD_ZONE_W // 2
        dz_right = cam_x + DEAD_ZONE_W // 2
        dz_bottom = cam_y - DEAD_ZONE_H // 2
        dz_top = cam_y + DEAD_ZONE_H // 2

        px, py = self.player.center_x, self.player.center_y
        target_x, target_y = cam_x, cam_y

        if px < dz_left:
            target_x = px + DEAD_ZONE_W // 2
        elif px > dz_right:
            target_x = px - DEAD_ZONE_W // 2
        if py < dz_bottom:
            target_y = py + DEAD_ZONE_H // 2
        elif py > dz_top:
            target_y = py - DEAD_ZONE_H // 2

        half_w = self.world_camera.viewport_width / 2
        half_h = self.world_camera.viewport_height / 2
        target_x = max(half_w, min(1600 - half_w, target_x))
        target_y = max(half_h, min(960 - half_h, target_y))

        smooth_x = (1 - CAMERA_LERP) * cam_x + CAMERA_LERP * target_x
        smooth_y = (1 - CAMERA_LERP) * cam_y + CAMERA_LERP * target_y
        self.cam_target = (smooth_x, smooth_y)

        self.world_camera.position = (self.cam_target[0], self.cam_target[1])

    def on_key_press(self, key, modifiers):
        """Управление (добавляем нажатые клавиши в список)"""
        KEYS_PRESSED.append(key)

    def on_key_release(self, key, modifiers):
        """Управление (удаление клавиш из списка если их отпустили)"""
        KEYS_PRESSED.remove(key)

    def on_mouse_press(self, x, y, button, modifiers):
        "Создаём пулю при нажатии на левую кнопку мыши"
        if button == arcade.MOUSE_BUTTON_LEFT:
            world_x, world_y = (self.world_camera.position[0] + (x - SCREEN_WIDTH // 2),
                                self.world_camera.position[1] + (y - SCREEN_HEIGHT // 2))  # преобразовываем координаты для пули
            bullet = Bullet(
                self.player.center_x,
                self.player.center_y,
                world_x,
                world_y)
            self.bullet_list.append(bullet)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = GameView()
    start_view.setup()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
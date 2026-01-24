# ! - означает, что эта часть кода не доделана
import arcade


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
ANIMATION_SPEED = 0.2
# DEAD_ZONE_W = 10
# DEAD_ZONE_H = 10
CAMERA_LERP = 0.12
DEAD_ZONE_W = int(SCREEN_WIDTH * 0.35)
DEAD_ZONE_H = int(SCREEN_HEIGHT * 0.45)
SCREEN_TITLE = "Очень крутой рогалик"
KEYS_PRESSED = []

class MainCharacter(arcade.Sprite):
    """класс главного игрока"""
    def __init__(self):
        super().__init__()
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
        if arcade.key.A in KEYS_PRESSED:
            dx -= self.speed_player * delta_time
        if arcade.key.D in KEYS_PRESSED:
            dx += self.speed_player * delta_time
        if arcade.key.W in KEYS_PRESSED:
            dy += self.speed_player * delta_time
        if arcade.key.S in KEYS_PRESSED:
            dy -= self.speed_player * delta_time

        if dx != 0 and dy != 0:
            factor = 0.7071  # ≈ 1/√2
            dx *= factor
            dy *= factor

        self.center_x += dx
        self.center_y += dy

        if arcade.key.W in KEYS_PRESSED and self.animation_frame != 6:
            self.animation_frame = 5
        if arcade.key.S in KEYS_PRESSED:
          self.animation_frame = 0
        if arcade.key.A in KEYS_PRESSED and self.animation_frame != 4:
          self.animation_frame = 3
        if arcade.key.D in KEYS_PRESSED and self.animation_frame != 2:
            self.animation_frame = 1
        elif all([True if key not in KEYS_PRESSED else False for key in [arcade.key.A, arcade.key.D, arcade.key.W, arcade.key.S]]):
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

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        "Размер карты: 3_200, 1920"
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

    def setup(self):
        self.player = MainCharacter()
        self.pl_sp = arcade.SpriteList()
        self.pl_sp.append(self.player)

        "камера для игрока"
        self.world_camera = arcade.Camera2D()
        self.world_camera.position = (200, 200)

        # ! надо поменять: начало
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player, self.scene["wall_coll"]
        )
        # ! надо поменять: конец
        "!нарежь сцены правильно"

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

    def on_update(self, delta_time):
        """Обновляем все элементы"""
        "Физический движок"
        self.physics_engine.update()
        "Обновляем позицию игрока"
        self.player.update(delta_time)

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


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = GameView()
    start_view.setup()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
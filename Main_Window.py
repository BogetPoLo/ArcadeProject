# ! - означает, что эта часть кода не доделана
import math
from random import randint, choice

import arcade
from pyglet.graphics import Batch
from main_character import MainCharacter
from enemys import Enemy
from bullet import Bullet
from particles_walking import DustParticleFromWalking

SCREEN_WIDTH = 800  # Ширина
SCREEN_HEIGHT = 640  # Высота

CAMERA_LERP = 0.12
DEAD_ZONE_W = int(SCREEN_WIDTH * 0.15)  # Мёртвая зона по ширине
DEAD_ZONE_H = int(SCREEN_HEIGHT * 0.25)  # Мёртвая зона по высоте
DAMAGE_TIMER_CONST = 1.5  # Промежуток между уроном, который может пройти по игроку
DUST_FROM_WALKING_TIMER = 0.5  # Промежуток появления частиц от ходьбы

PRICE_PER_CHEST = {"chest_one_tex": 1, "chest_two_tex": 2, "chest_tree_tex": 3}  # Цена за каждую бочку
SCREEN_TITLE = "Очень крутой рогалик"  # Название игры
KEYS_PRESSED = []  # Список нажатых кнопок


class GameView(arcade.View):
    """
    Класс реализует саму игру
    Создание персонажей, обновление всего и т.п.
    """
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
        self.p_f_e = self.scene["protection_from_enemies"]
        self.l_f_e = self.scene["limitations for enemies"]

        self.lv_start_on = self.scene["level_start_one"]
        self.lv_start_tw = self.scene["level_start_two"]
        self.lv_start_tr = self.scene["level_start_tree"]
        self.lv_start_fo = self.scene["level_start_four"]

        "Двери для комнат с бочками"
        self.red_d = self.scene["red_door"]
        self.purple_d = self.scene["purple door"]

        "уровни поделённые на блоки"
        self.start = self.scene["start"]
        self.finish = self.scene["finish"]
        self.corridor = self.scene["corridor"]
        self.le_on = self.scene["level_one"]
        self.le_tw = self.scene["level_two"]
        self.le_tr = self.scene["level_tree"]
        self.le_fo = self.scene["level_four"]
        self.TYPES_OF_LOCATIONS = {self.start: ["Вы на стартовой локации"],
                                   self.le_on: ["Вы на первом уровне"],
                                   self.le_tw: ["Вы на втором уровне"],
                                   self.le_tr: ["Вы на третьем уровне"],
                                   self.le_fo: ["Вы на четвёртом уровне"],
                                   self.finish: ["Конец забега"],
                                   self.corridor: ["Вы в коридоре"]}
        self.DOOR = {self.lv_start_on: self.le_on,
                     self.lv_start_tw: self.le_tw,
                     self.lv_start_tr: self.le_tr,
                     self.lv_start_fo: self.le_fo}

        "двери уровней"
        self.lv_on_cl = self.scene["level_one_close"]
        self.lv_tw_cl = self.scene["level_two_close"]
        self.lv_tr_cl = self.scene["level_tree_close"]
        self.lv_fo_cl = self.scene["level_four_close"]

        "ключи"
        self.r_k = self.scene["red_key"]
        self.p_k = self.scene["purple_key"]

    def setup(self):
        """обнуляем всё для нового забега"""
        "персонаж"
        self.player = MainCharacter(KEYS_PRESSED)
        self.pl_sp = arcade.SpriteList()
        self.pl_sp.append(self.player)

        "пули"
        self.bullet_list = arcade.SpriteList()

        "частицы"
        self.particles_w = arcade.SpriteList()

        "камера для игрока"
        self.world_camera = arcade.Camera2D()
        self.world_camera.position = (200, 200)

        "камера для gui"
        self.gui_camera = arcade.Camera2D()

        "физика"
        self.ph_wall = arcade.PhysicsEngineSimple(  # Игрок и стены
            self.player, self.w_c
        )
        "Двери для комнат с бочками"
        self.ph_r_door = arcade.PhysicsEngineSimple(
            self.player, self.red_d
        )
        self.ph_p_door = arcade.PhysicsEngineSimple(
            self.player, self.purple_d
        )

        "Двери для каждого уровня"
        self.ph_lv_one = arcade.PhysicsEngineSimple(
            self.player, self.lv_on_cl
        )
        self.ph_lv_two = arcade.PhysicsEngineSimple(
            self.player, self.lv_tw_cl
        )
        self.ph_lv_tree = arcade.PhysicsEngineSimple(
            self.player, self.lv_tr_cl
        )
        self.ph_lv_four = arcade.PhysicsEngineSimple(
            self.player, self.lv_fo_cl
        )

        "враги"
        self.enemy_sp = arcade.SpriteList()
        for data in [[randint(400, 575), randint(190, 260)],
                     [randint(180, 270), randint(460, 595)],
                     [randint(400, 470), randint(460, 660)],
                     [randint(180, 460), randint(765, 820)],
                     [randint(750, 920), randint(565, 730)],
                     [randint(1030, 1270), randint(715, 735)],
                     [randint(1340, 1460), randint(560, 705)]]:
            for _ in range(randint(5, 7)):
                rx = data[0]
                ry = data[1]
                angle = choice((0, 30, 45, 60, 90))
                rspeed = randint(150, 250)
                self.enemy_sp.append(Enemy(rx, ry, angle, rspeed))

        "иные переменные"
        self.result_score = 0
        self.life_time = 0.0
        self.result_kill = 0
        self.batch = Batch()
        self.magazine = 10
        self.xp = 100
        self.damage_timer = 0
        self.dust_w = 0
        self.name_level = 0
        self.close_door = None
        self.current_level = None
        self.location = None
        self.room_text_one = False
        self.room_text_two = False
        self.open_room_one = False
        self.open_room_two = False
        self.purple_keys = 0
        self.red_keys = 0

        self.sound_closed_door = arcade.load_sound("closed-door-381852.wav")
        self.sound_laser = arcade.load_sound("laser-shot-ingame-230500.wav")
        self.sound_smash = arcade.load_sound("wood-smash-5-170421.wav")
        self.sound_game = arcade.load_sound("game.mp3")

        arcade.play_sound(self.sound_game, volume=0.2, loop=True)

    def on_draw(self):
        """Рисует картинку"""
        self.clear()
        self.world_camera.use()

        self.f_t.draw()
        self.g_t.draw()
        self.w_t.draw()
        self.a_t.draw()
        self.r_k.draw()
        self.p_k.draw()
        self.ch_o_t.draw()
        self.ch_tw_t.draw()
        self.ch_tr_t.draw()
        self.particles_w.draw()
        self.pl_sp.draw()
        self.enemy_sp.draw()

        if not(self.open_room_one):
            self.purple_d.draw()
        if not(self.open_room_two):
            self.red_d.draw()

        if self.current_level == self.le_on:
            self.lv_on_cl.draw()
        elif self.current_level == self.le_tw:
            self.lv_tw_cl.draw()
        elif self.current_level == self.le_tr:
            self.lv_tr_cl.draw()
        elif self.current_level == self.le_fo:
            self.lv_fo_cl.draw()

        self.bullet_list.draw()

        self.gui_camera.use()
        text_lifetime = arcade.Text(f"Время жизни: {self.life_time:.2f}", 5, SCREEN_HEIGHT - 30, arcade.color.BLACK, 20, batch=self.batch)
        text_score = arcade.Text(f"Собрано монет: {self.result_score}", 5, SCREEN_HEIGHT - 60, arcade.color.BLACK, 20, batch=self.batch)
        text_kill = arcade.Text(f"Убито врагов: {self.result_kill}", 5, SCREEN_HEIGHT - 90, arcade.color.BLACK, 20, batch=self.batch)
        text_magazine = arcade.Text(f"Патронов в магазине: {self.magazine}", 5, SCREEN_HEIGHT - 120, arcade.color.BLACK, 20, batch=self.batch)
        text_xp = arcade.Text(f"XP: {self.xp}", 5, SCREEN_HEIGHT - 150, arcade.color.BLACK,20, batch=self.batch)
        text_num_level = arcade.Text(str(self.name_level), 5, SCREEN_HEIGHT - 180, arcade.color.BLACK,20, batch=self.batch)
        p_keys = arcade.Text(f"Фиолетовыx ключей: {self.purple_keys}", 5, SCREEN_HEIGHT - 210, arcade.color.BLACK,20, batch=self.batch)
        r_keys = arcade.Text(f"Красных ключей: {self.red_keys}", 5, SCREEN_HEIGHT - 240, arcade.color.BLACK, 20, batch=self.batch)

        if self.room_text_one:
            color = [arcade.color.RED, arcade.color.RED]
            arcade.draw_rect_filled(arcade.rect.XYWH(SCREEN_WIDTH // 1.35, SCREEN_HEIGHT // 4.6, 400, 100), arcade.color.WHITE)
            arcade.draw_rect_outline(arcade.rect.XYWH(SCREEN_WIDTH // 1.35, SCREEN_HEIGHT // 4.6, 400, 100), arcade.color.BLACK)
            text_door_one = arcade.Text("Чтобы открыть эту комнату нужно:", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, arcade.color.BLACK,20, batch=self.batch)
            if self.purple_keys == 4:
                color[0] = arcade.color.GREEN
            text_door_two = arcade.Text(f"Найдите фиолетовые ключи {self.purple_keys}/4", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 - 30, color[0], 20, batch=self.batch)
            if self.xp > 70:
                color[1] = arcade.color.GREEN
            text_door_tree = arcade.Text("XP должно быть больше 70.", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 - 60, color[1], 20, batch=self.batch)

        if self.room_text_two:
            color = [arcade.color.RED, arcade.color.RED]
            arcade.draw_rect_filled(arcade.rect.XYWH(SCREEN_WIDTH // 3.5, SCREEN_HEIGHT // 3.5, 400, 100), arcade.color.WHITE)
            arcade.draw_rect_outline(arcade.rect.XYWH(SCREEN_WIDTH // 3.5, SCREEN_HEIGHT // 3.5, 400, 100), arcade.color.BLACK)
            text_door_one = arcade.Text("Чтобы открыть эту комнату нужно:", SCREEN_WIDTH // 24, SCREEN_HEIGHT // 3.2, arcade.color.BLACK, 20, batch=self.batch)
            if self.red_keys == 2:
                color[0] = arcade.color.GREEN
            text_door_two = arcade.Text(f"Найдите красные ключи {self.red_keys}/2", SCREEN_WIDTH // 24, SCREEN_HEIGHT // 3.2 - 30, color[0], 20, batch=self.batch)
            if self.xp > 40:
                color[1] = arcade.color.GREEN
            text_door_tree = arcade.Text("XP должно быть больше 40.", SCREEN_WIDTH // 24, SCREEN_HEIGHT // 3.2 - 60, color[1],20, batch=self.batch)
        self.batch.draw()

    def on_update(self, delta_time):
        """Обновляем все элементы"""
        "время"
        self.life_time += delta_time

        "Физический движок"
        self.ph_wall.update()
        if not (self.open_room_one):
            self.ph_p_door.update()
        if not (self.open_room_two):
            self.ph_r_door.update()

        if self.xp > 70 and self.purple_keys == 4 and arcade.key.Q in KEYS_PRESSED and self.room_text_one and not(self.open_room_one):
            self.open_room_one = True
            arcade.play_sound(self.sound_closed_door)

        if self.xp > 40 and self.purple_keys == 2 and arcade.key.Q in KEYS_PRESSED and self.room_text_two and not(self.open_room_two):
            self.open_room_two = True
            arcade.play_sound(self.sound_closed_door)

        "Проверяем есть ли на одном уровне с игроком враги. Если да, то локация закрывается и надо убить всех врагов."
        if self.close_door is None:
            for door, location in self.DOOR.items():
                if arcade.check_for_collision_with_list(self.player, door):
                    self.close_door = door
                    self.location = location

        if self.location is not None:
            if any([True if arcade.check_for_collision_with_list(enemy, self.location) else False for enemy in self.enemy_sp]):
                self.current_level = self.location
            else:
                self.close_door = None
                self.current_level = None
                self.location = None

        if self.location is not None:
            if self.current_level == self.le_on:
                self.ph_lv_one.update()
            elif self.current_level == self.le_tw:
                self.ph_lv_two.update()
            elif self.current_level == self.le_tr:
                self.ph_lv_tree.update()
            elif self.current_level == self.le_fo:
                self.ph_lv_four.update()

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
                    arcade.play_sound(self.sound_smash, volume=0.1)

        "проверка столкновения врага и стены"
        for enemy in self.enemy_sp:
            if arcade.check_for_collision_with_list(enemy, self.l_f_e):
                enemy.changing_the_direction()
            if arcade.check_for_collision_with_list(enemy, self.bullet_list):
                enemy.remove_from_sprite_lists()
                self.result_kill += 1
            if arcade.check_for_collision_with_list(enemy, self.p_f_e):
                enemy.remove_from_sprite_lists()
            if arcade.check_for_collision_with_list(enemy, self.pl_sp) and self.damage_timer > DAMAGE_TIMER_CONST:
                self.xp -= 15
                self.damage_timer = 0
                if self.xp <= 0:
                    exit()
        self.damage_timer += delta_time

        "позиция врага"
        self.enemy_sp.update(delta_time)

        "удаляем пулю если она столкнулась со стеной"
        for bullet in self.bullet_list:
            if arcade.check_for_collision_with_list(bullet, self.w_c):
                bullet.remove_from_sprite_lists()

        "обновляем частицы"
        for dust in self.particles_w:
            if dust.update(delta_time):
                dust.remove_from_sprite_lists()

        "Создаём частицу от положения игрока"
        if self.dust_w >= DUST_FROM_WALKING_TIMER:
            self.dust_w = 0
            x, y = self.player.center_x, self.player.center_y
            if arcade.key.W in KEYS_PRESSED:
                self.create_dust_effect(x, y - 10)
            elif arcade.key.S in KEYS_PRESSED:
                self.create_dust_effect(x, y + 20)
            elif arcade.key.A in KEYS_PRESSED:
                self.create_dust_effect(x + 20, y - 20)
            elif arcade.key.D in KEYS_PRESSED:
                self.create_dust_effect(x - 20, y - 20)
        self.dust_w += delta_time

        "Обновляем камеры"
        self.update_camera()

        "обновление переменных"
        if  arcade.key.R in KEYS_PRESSED:
            self.magazine = 10

        "проверяем на каком уровне игрок и обновляем"
        for location, text_loc in self.TYPES_OF_LOCATIONS.items():
            if arcade.check_for_collision_with_list(self.player, location):
                self.name_level = text_loc[0]

        "Проверяем на срабатывания текста около комнат с бочками"
        if 771 <= self.player.center_x <= 831 and 740 <= self.player.center_y <= 773:
            self.room_text_one = True
        else:
            self.room_text_one = False

        if 1400 <= self.player.center_x <= 1475 and 534 <= self.player.center_y <= 551:
            self.room_text_two = True
        else:
            self.room_text_two = False

        "проверка на нахождения ключа"
        for key in self.r_k:
            if arcade.check_for_collision(self.player, key):
                self.red_keys += 1
                key.remove_from_sprite_lists()

        for key in self.p_k:
            if arcade.check_for_collision(self.player, key):
                self.purple_keys += 1
                key.remove_from_sprite_lists()


    def update_camera(self):
        "Обновляем камеру для персонажа и gui"
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

    def create_dust_effect(self, x, y):
        "создаём частицы"
        for _ in range(randint(1, 2)):
            self.dust = DustParticleFromWalking(x, y)
            self.particles_w.append(self.dust)

    def on_key_press(self, key, modifiers):
        """Управление (добавляем нажатые клавиши в список)"""
        KEYS_PRESSED.append(key)

    def on_key_release(self, key, modifiers):
        """Управление (удаление клавиш из списка если их отпустили)"""
        KEYS_PRESSED.remove(key)

    def on_mouse_press(self, x, y, button, modifiers):
        "Создаём пулю при нажатии на левую кнопку мыши"
        if button == arcade.MOUSE_BUTTON_LEFT and self.magazine > 0:
            self.magazine -= 1
            world_x, world_y = (self.world_camera.position[0] + (x - SCREEN_WIDTH // 2),
                                self.world_camera.position[1] + (y - SCREEN_HEIGHT // 2))  # преобразовываем координаты для пули
            bullet = Bullet(
                self.player.center_x,
                self.player.center_y,
                world_x,
                world_y)
            self.bullet_list.append(bullet)
            arcade.play_sound(self.sound_laser, volume=0.1)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = GameView()
    start_view.setup()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
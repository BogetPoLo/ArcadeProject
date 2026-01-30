import arcade
ANIMATION_SPEED = 0.2  # Интервал смены текстуры


class MainCharacter(arcade.Sprite):
    """
    Класс главного героя.
    Отвечает за движение персонажа, смену анимации
    """
    def __init__(self, keys_pr):
        super().__init__()
        self.keys_pr = keys_pr  # Список кнопок, на которые нажал человек
        "Анимационная информация об игроке"
        self.animation_frame = 0
        self.animation_time = 0

        "загружаем текстуры"
        self.textures = [arcade.load_texture("alienGreen.png"),  # Стоит
                         arcade.load_texture("alienGreen_walk1.png"),  # Бежит влево 1
                         arcade.load_texture("alienGreen_walk2.png"),  # Бежит влево 2
                         arcade.load_texture("alienGreen_walk1.png").flip_horizontally(),  # Бежит вправо 1
                         arcade.load_texture("alienGreen_walk2.png").flip_horizontally(),  # Бежит вправо 2
                         arcade.load_texture("alienGreen_climb1.png"),  # Идёт на верх 1
                         arcade.load_texture("alienGreen_climb2.png")]  # Идёт на верх 2
        self.set_texture(self.animation_frame)  # Устанавливаем начальную текстуру
        "Стартовая информация об игроке"
        self.center_x = 200
        self.center_y = 200
        self.scale = 0.5
        self.speed_player = 250

    def update(self, delta_time):
        dx = 0
        dy = 0

        "Направление игрока"
        THE_DIRECTION_OF_MOVEMENT = {arcade.key.A: (-self.speed_player * delta_time, 0),
                                     arcade.key.D: (self.speed_player * delta_time, 0),
                                     arcade.key.W: (0, self.speed_player * delta_time),
                                     arcade.key.S: (0, -self.speed_player * delta_time)}

        "Определяем направление игрока"
        for direction in THE_DIRECTION_OF_MOVEMENT:
            if direction in self.keys_pr:
                change_dx, change_dy = THE_DIRECTION_OF_MOVEMENT[direction]
                dx += change_dx
                dy += change_dy

        "Угловое движение"
        if dx != 0 and dy != 0:
            factor = 0.7071  # ≈ 1/√2
            dx *= factor
            dy *= factor

        self.center_x += dx
        self.center_y += dy

        # Проверяем какое направление у игрока и сменяем текстуру
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

        # Меняем текстуры текстуру
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
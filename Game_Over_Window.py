# ! - означает, что эта часть кода не доделана

import arcade
from arcade.gui import UIManager, UIAnchorLayout, UIBoxLayout, UILabel, UITextArea, UITextureButton, UIInputText

class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.final_score = 0
        self.life_time = 0.0

        self.background_color = arcade.color.BLUE_GRAY  #! Поменяй цвет на нормальный

        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout()  # Центрирует виджеты
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)  # !Вертикальный стек

        self.setup_widgets()

        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):
        "Создаём виджеты"
        "!"
        label = UILabel(text="ИГРА ОКОНЧЕНА",
                        font_size=50,
                        text_color=arcade.color.WHITE,
                        width=300,
                        align="center")
        self.box_layout.add(label)

        text_output_score = UILabel(text=f"Всего очков: {self.final_score}",
                        font_size=20,
                        text_color=arcade.color.WHITE,
                        width=300,
                        align="center")
        self.box_layout.add(text_output_score)

        text_output_life_time = UILabel(text=f"Ваше время жизни: {self.life_time}",
                        font_size=20,
                        text_color=arcade.color.WHITE,
                        width=300,
                        align="center")
        self.box_layout.add(text_output_life_time)

        new_game = UILabel(text="Нажмите на пробел чтобы начать новую игру",
                        font_size=20,
                        text_color=arcade.color.WHITE,
                        width=300,
                        align="center")
        self.box_layout.add(new_game)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            exit()  #! для тестов

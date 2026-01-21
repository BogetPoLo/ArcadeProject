# ! - означает, что эта часть кода не доделана

import arcade
from arcade.gui import UIManager, UIAnchorLayout, UIBoxLayout, UILabel, UITextArea, UITextureButton, UIInputText

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Очень крутой рогалик"


class Menu_View(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.BLUE_GRAY

        self.manager = UIManager()
        self.manager.enable()

        # Layout
        self.anchor_layout = UIAnchorLayout()  # Центрирует виджеты
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)  # !Вертикальный стек
        self.rules_and_management = UIBoxLayout(vertical=False, space_between=10)  # !Горизонтальный layout для правил и управления

        self.setup_widgets()

        self.box_layout.add(self.rules_and_management)

        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):
        "Создаём виджеты"
        "!Название игры"
        label = UILabel(text="ОЧЕНЬ КРУТОЙ РОГАЛИК",
                        font_size=50,
                        text_color=arcade.color.WHITE,
                        width=300,
                        align="center")
        self.box_layout.add(label)

        "!Управление"
        text_area = UITextArea(text="Управление\nПеремещение: WASD\nУклонение: Q\nПерезарядка: R",
                               width=200,
                               height=200,
                               font_size=20)
        self.rules_and_management.add(text_area)

        "!Правила"
        text_area_two = UITextArea(text="Правила игры\nНужно пройти 5 уровней,\n убивая противников и собирая монеты,\n которые будут в сундуках.",
                               width=500,
                               height=200,
                               font_size=20)
        self.rules_and_management.add(text_area_two)

        "!Кнопка для запуска игры"
        texture_normal = arcade.load_texture(":resources:/gui_basic_assets/button/red_normal.png")  # Нужно добавить свои текстуры
        texture_hovered = arcade.load_texture(":resources:/gui_basic_assets/button/red_hover.png")  # Нужно добавить свои текстуры
        texture_pressed = arcade.load_texture(":resources:/gui_basic_assets/button/red_press.png")  # Нужно добавить свои текстуры
        texture_button = UITextureButton(texture=texture_normal,
                                         texture_hovered=texture_hovered,
                                         texture_pressed=texture_pressed,
                                         scale=1.0)
        self.box_layout.add(texture_button)

        "!Поле для ввода ника, если ника нет, то в игру не запускает"
        input_text = UIInputText(x=0, y=0, width=200, height=30, text="Введи имя")
        self.box_layout.add(input_text)

    def on_draw(self):
        self.clear()
        self.manager.draw()


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = Menu_View()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
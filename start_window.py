import arcade
from arcade.gui import (
    UIManager, UIAnchorLayout, UIBoxLayout,
    UILabel, UITextArea, UITextureButton, UIInputText
)

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 650
SCREEN_TITLE = "ОЧЕНЬ КРУТОЙ РОГАЛИК"


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.ALMOND

        self.manager = UIManager()
        self.manager.enable()

        self.anchor = UIAnchorLayout()
        self.main_box = UIBoxLayout(vertical=True, space_between=20)

        self.info_box = UIBoxLayout(vertical=False, space_between=30)

        self.setup_ui()

        self.main_box.add(self.info_box)
        self.anchor.add(self.main_box, anchor_x="center_x", anchor_y="center_y")
        self.manager.add(self.anchor)

    def setup_ui(self):
        # Заголовок
        title = UILabel(
            text="🔥 ОЧЕНЬ КРУТОЙ РОГАЛИК 🔥",
            font_size=48,
            bold=True,
            text_color=arcade.color.BLACK,
            align="center"
        )
        self.main_box.add(title)

        # Управление
        controls_text = (
            "🎮 УПРАВЛЕНИЕ\n\n"
            "W A S D — ходьба\n"
            "ПКМ — выстрел\n"
            "R — перезарядка\n"
            "Q — открыть дверь\n"
        )

        controls = UITextArea(
            text=controls_text,
            width=300,
            height=220,
            font_size=18,
            text_color=arcade.color.BLACK
        )

        # ===== Правила =====
        rules_text = (
            "📜 ПРАВИЛА ИГРЫ\n\n"
            "• Пройди 5 уровней\n"
            "• Уничтожай врагов\n"
            "• Исследуй комнаты\n\n"
            "🔑 КЛЮЧИ:\n"
            "Фиолетовый\n"
            "Красный "
        )

        rules = UITextArea(
            text=rules_text,
            width=380,
            height=250,
            font_size=18,
            text_color=arcade.color.BLACK
        )

        self.info_box.add(controls)
        self.info_box.add(rules)

        # Ввод ника
        self.name_input = UIInputText(
            text="Введите имя",
            width=250,
            height=35,
            text_color=arcade.color.BLACK
        )
        self.main_box.add(self.name_input)

        start_button = UITextureButton(
            texture=arcade.load_texture(":resources:/gui_basic_assets/button/red_normal.png"),
            texture_hovered=arcade.load_texture(":resources:/gui_basic_assets/button/red_hover.png"),
            texture_pressed=arcade.load_texture(":resources:/gui_basic_assets/button/red_press.png"),
            scale=1.1
        )

        self.main_box.add(start_button)

    def on_draw(self):
        self.clear()
        self.manager.draw()


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.show_view(MenuView())
    arcade.run()


if __name__ == "__main__":
    main()

import arcade
from arcade.gui import (
    UIManager, UIAnchorLayout, UIBoxLayout, UILabel
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Pause Menu — тест"


class PauseView(arcade.View):
    def __init__(self):
        super().__init__()

        self.background_color = arcade.color.DARK_SLATE_GRAY

        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=20)

        self.setup_widgets()

        self.anchor_layout.add(
            self.box_layout,
            anchor_x="center_x",
            anchor_y="center_y"
        )
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):
        # PAUSE
        title = UILabel(
            text="⏸ ПАУЗА",
            font_size=52,
            bold=True,
            text_color=arcade.color.YELLOW,
            align="center"
        )
        self.box_layout.add(title)

        # Подсказки
        resume = UILabel(
            text="ESC — продолжить игру",
            font_size=24,
            text_color=arcade.color.WHITE,
            align="center"
        )
        self.box_layout.add(resume)

        restart = UILabel(
            text="R — начать заново",
            font_size=22,
            text_color=arcade.color.LIGHT_GRAY,
            align="center"
        )
        self.box_layout.add(restart)

        quit_game = UILabel(
            text="Q — выйти из игры",
            font_size=22,
            text_color=arcade.color.LIGHT_GRAY,
            align="center"
        )
        self.box_layout.add(quit_game)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_key_press(self, key, modifiers):
        # Продолжить игру
        if key == arcade.key.ESCAPE:
            print("Продолжить игру (заглушка)")

        # Рестарт
        elif key == arcade.key.R:
            print("Рестарт игры (заглушка)")

        # Выход
        elif key == arcade.key.Q:
            arcade.close_window()


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    pause_view = PauseView()
    window.show_view(pause_view)
    arcade.run()


if __name__ == "__main__":
    main()

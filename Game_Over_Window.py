import arcade
from arcade.gui import (
    UIManager, UIAnchorLayout, UIBoxLayout, UILabel
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Game Over — тест"


class GameOverView(arcade.View):
    def __init__(self, final_score=1234, life_time=87.6):
        super().__init__()

        self.final_score = final_score
        self.life_time = life_time

        # Нормальный тёмный фон
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
        # GAME OVER
        title = UILabel(
            text="💀 GAME OVER 💀",
            font_size=52,
            bold=True,
            text_color=arcade.color.RED,
            align="center"
        )
        self.box_layout.add(title)

        # Очки
        score_label = UILabel(
            text=f"⭐ Очки: {self.final_score}",
            font_size=26,
            text_color=arcade.color.WHITE,
            align="center"
        )
        self.box_layout.add(score_label)

        # Время жизни
        time_label = UILabel(
            text=f"⏱ Время жизни: {self.life_time:.1f} сек",
            font_size=24,
            text_color=arcade.color.WHITE,
            align="center"
        )
        self.box_layout.add(time_label)

        # Подсказка
        hint = UILabel(
            text=(
                "SPACE — начать заново \n"
                "ESC — выход"
            ),
            font_size=20,
            text_color=arcade.color.LIGHT_GRAY,
            align="center"
        )
        self.box_layout.add(hint)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            print("Новая игра (заглушка)")
        elif key == arcade.key.ESCAPE:
            arcade.close_window()


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game_over_view = GameOverView()
    window.show_view(game_over_view)
    arcade.run()


if __name__ == "__main__":
    main()

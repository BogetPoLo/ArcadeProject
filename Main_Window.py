# ! - означает, что эта часть кода не доделана

import arcade


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
SCREEN_TITLE = "Очень крутой рогалик"


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        "Размер карты: 3_200, 1920"
        self.name_map = arcade.load_tilemap("arc_map.tmx", scaling=0.5)  # загружаем карту
        self.scene = arcade.Scene.from_tilemap(self.name_map)  # делаем из карты сцены
        "!нарежь сцены правильно"

    def on_draw(self):
        self.clear()
        self.scene.draw()


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = GameView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
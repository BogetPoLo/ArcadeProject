import arcade
from arcade.gui import UIManager, UIAnchorLayout, UIBoxLayout, UILabel

FILE_RECORDS = "final.txt"  # файл с результатами
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class GameOverView(arcade.View):
    def __init__(self, name_player, win, coin, time_val, kill, xp):
        super().__init__()

        # Данные игрока
        self.name_player = name_player
        self.win = win
        self.coin = coin
        self.time = time_val
        self.kill = kill
        self.xp = xp

        # Обновляем базу и получаем лучшую статистику
        self.best_stats, self.message = self.update_player_record()

        # Настройка интерфейса
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

    def update_player_record(self):
        """Сравнивает игрока с базой и обновляет файл final.txt"""
        records = {}
        # Читаем существующие записи
        try:
            with open(FILE_RECORDS, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split(",")
                    if len(parts) != 6:
                        continue  # некорректная строка
                    name, win, coin, time_val, kill, xp = parts
                    records[name] = {
                        "win": int(win),
                        "coin": int(coin),
                        "time": float(time_val),
                        "kill": int(kill),
                        "xp": int(xp)
                    }
        except FileNotFoundError:
            pass  # Файл ещё не создан

        message = "Новый рекорд!"
        # Если игрок уже есть, сравниваем результаты
        if self.name_player in records:
            old = records[self.name_player]
            updated = False

            # Обновляем только лучшие показатели
            if self.coin > old["coin"]:
                old["coin"] = self.coin
                updated = True
            if self.kill > old["kill"]:
                old["kill"] = self.kill
                updated = True
            if self.xp > old["xp"]:
                old["xp"] = self.xp
                updated = True
            if self.win and not old["win"]:
                old["win"] = int(self.win)
                updated = True
            # Время лучше меньше
            if self.time < old["time"]:
                old["time"] = self.time
                updated = True

            if updated:
                message = "Обновлён лучший результат!"
        else:
            # Новый игрок
            records[self.name_player] = {
                "win": int(self.win),
                "coin": self.coin,
                "time": self.time,
                "kill": self.kill,
                "xp": self.xp
            }

        # Перезаписываем файл
        with open(FILE_RECORDS, "w", encoding="utf-8") as f:
            for name, data in records.items():
                f.write(f"{name},{data['win']},{data['coin']},{data['time']},{data['kill']},{data['xp']}\n")

        return records[self.name_player], message

    def setup_widgets(self):
        # Основной горизонтальный контейнер для статуса и статистики
        main_hbox = UIBoxLayout(vertical=False, space_between=50)

        # Левая колонка — статус
        left_vbox = UIBoxLayout(vertical=True, space_between=20)
        status_text = "WIN! 🎉" if self.win else "GAME OVER 💀"
        status_label = UILabel(
            text=status_text,
            font_size=48,
            bold=True,
            text_color=arcade.color.RED if not self.win else arcade.color.GREEN,
            align="center"
        )
        left_vbox.add(status_label)

        # Правая колонка — статистика
        right_vbox = UIBoxLayout(vertical=True, space_between=10)
        stats = self.best_stats
        right_vbox.add(UILabel(text=f"Игрок: {self.name_player}", font_size=22, text_color=arcade.color.WHITE))
        right_vbox.add(
            UILabel(text=f"Победа: {'Да' if stats['win'] else 'Нет'}", font_size=22, text_color=arcade.color.WHITE))
        right_vbox.add(UILabel(text=f"Монеты: {stats['coin']}", font_size=22, text_color=arcade.color.WHITE))
        right_vbox.add(UILabel(text=f"Убийства: {stats['kill']}", font_size=22, text_color=arcade.color.WHITE))
        right_vbox.add(UILabel(text=f"Время: {stats['time']:.1f} сек", font_size=22, text_color=arcade.color.WHITE))
        right_vbox.add(UILabel(text=f"XP: {stats['xp']}", font_size=22, text_color=arcade.color.WHITE))

        # Сообщение о рекорде
        message_label = UILabel(
            text=self.message,
            font_size=20,
            text_color=arcade.color.YELLOW,
            align="center"
        )
        right_vbox.add(message_label)

        # Подсказка
        hint_label = UILabel(
            text="ESC — выход",
            font_size=18,
            text_color=arcade.color.LIGHT_GRAY,
            align="center"
        )
        right_vbox.add(hint_label)

        # Добавляем колонки в горизонтальный контейнер
        main_hbox.add(left_vbox)
        main_hbox.add(right_vbox)

        # Добавляем горизонтальный контейнер в основной вертикальный layout
        self.box_layout.add(main_hbox)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window()

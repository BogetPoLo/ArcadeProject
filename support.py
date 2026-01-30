"комната 1"
"размеры - (400, 180) (590, 260)"
"кол. врагов: 2 - 3"

"комната 2"
"размеры: 1((180, 460) (270,595)) 2((400, 460) (470, 660)) 3((175, 765) (460, 820)"
"кол. врагов: 1(1), 2(2) 3(2)"

"комната 3"
"размеры - 1((750, 565) (920, 730)) 2((1030, 715) (1270, 735)) 3((1340, 560) (1460, 705))"
"кол. врагов: 1(2 - 3) 2(2 очень маленьких) 3(2 - 3)"

"комната 4"
"размеры - () ()"

"комната 5"
"размеры - () ()"

"комната бочек №1"
"точка срабатывания текста - (771, 744) (831, 773)"

"комната бочек №2"
"точка срабатывания текста - (1400, 534) (1475, 551)"


"комната 1 - старт"
"размер - (144, 152) (303, 296)"

"комната 2"
"размер - (368, 153) (620, 297)"

"комната 3"
"размер - (144, 439) (495, 841)"

"комната 4"
"размеры - (723, 535) (1487, 744)"

"комната 5"
"размеры - (816, 424) (978, 119) (1007, 119) (1359, 293)"

"комната 6"
"размер - (1424, 296) (1487, 119)"


"""x, y = self.player.center_x, self.player.center_y
        if 144 <= x <= 303 and 152 <= y <= 296:
            self.num_level = 1
            print(1)
        elif 368 <= x <= 620 and 153 <= y <= 297:
            self.num_level = 2
            print(2)
        elif 144 <= x <= 495 and 439 <= y <= 841:
            self.num_level = 3
            print(3)
        elif 723 <= x <= 1487 and 535 <= y <= 744:
            self.num_level = 4
            print(4)
        elif (816 <= x <= 978 and 424 <= y <= 119):
            self.num_level = 5
            print(5)
        elif 1424 <= x <= 1487 and 296 <= y <= 120:
            self.num_level = 6
            print(6)"""




# self.animation_time += ANIMATION_SPEED * ANIMATION_SPEED * ANIMATION_SPEED
        # if self.animation_time > ANIMATION_SPEED:
        #     self.animation_time = 0
        #     if self.animation_frame == 5:
        #         self.animation_frame += 1
        #     elif self.animation_frame == 6:
        #         self.animation_frame -= 1
        #
        #     if self.animation_frame == 1:
        #         self.animation_frame += 1
        #     elif self.animation_frame == 2:
        #         self.animation_frame -= 1
        #
        #     if self.animation_frame == 3:
        #         self.animation_frame += 1
        #     elif self.animation_frame == 4:
        #         self.animation_frame -= 1


self.TYPES_OF_LOCATIONS = {self.start: ["Вы на стартовой локации", None],
                                   self.le_on: ["Вы на первом уровне", False],
                                   self.le_tw: ["Вы на втором уровне", False],
                                   self.le_tr: ["Вы на третьем уровне", False],
                                   self.le_fo: ["Вы на четвёртом уровне", False],
                                   self.finish: ["Конец забега", None],
                                   self.corridor: ["Вы в коридоре", None]}


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

if self.close_door is None:
    for door in self.DOOR:
        if arcade.check_for_collision_with_list(self.player, door):
            self.close_door = door
            break

if self.close_door is not None and self.current_level is None:
    for location in self.TYPES_OF_LOCATIONS:
        for enemy in self.enemy_sp:
            if arcade.check_for_collision_with_list(enemy, location):
                self.current_level = location

if self.current_level == self.le_on:
    self.ph_lv_one.update()
elif self.current_level == self.le_tw:
    self.ph_lv_two.update()
elif self.current_level == self.le_tr:
    self.ph_lv_tree.update()
elif self.current_level == self.le_fo:
    self.ph_lv_four.update()
else:
    self.close_door = None
    self.current_level = None

self.DOOR = {self.lv_start_on: self.le_on,
                     self.lv_start_tw: self.le_tw,
                     self.lv_start_tr: self.le_tr,
                     self.lv_start_fo: self.le_fo}


text_lifetime = arcade.Text(f"Время жизни: {self.life_time:.2f}", 5, SCREEN_HEIGHT - 30, arcade.color.BLACK, 20, batch=self.batch)
        text_score = arcade.Text(f"Собрано монет: {self.result_score}", 5, SCREEN_HEIGHT - 60, arcade.color.BLACK, 20, batch=self.batch)
        text_kill = arcade.Text(f"Убито врагов: {self.result_kill}", 5, SCREEN_HEIGHT - 90, arcade.color.BLACK, 20, batch=self.batch)
        text_magazine = arcade.Text(f"Патронов в магазине: {self.magazine}", 5, SCREEN_HEIGHT - 120, arcade.color.BLACK, 20, batch=self.batch)
        text_xp = arcade.Text(f"XP: {self.xp}", 5, SCREEN_HEIGHT - 150, arcade.color.BLACK,20, batch=self.batch)
        text_num_level = arcade.Text(str(self.name_level), 5, SCREEN_HEIGHT - 180, arcade.color.BLACK,20, batch=self.batch)
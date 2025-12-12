import arcade

WIDTH = 1350
HEIGHT = 800
TITLE = "Стартовое окно"


class Start_Window(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.w = width
        self.h = height
        self.texture = arcade.load_texture("images/start_forest.jpg")
        self.button_width = 200
        self.button_height = 60
        self.button_x = WIDTH // 2
        self.button_y = HEIGHT // 2
        self.button_color = arcade.color.BLUE
        self.hover_color = arcade.color.LIGHT_BLUE
        self.text_color = arcade.color.WHITE
        self.is_hovered = False
        self.game_window = None

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(self.w // 2, self.h // 2, self.w, self.h, self.texture)
        button_color = self.hover_color if self.is_hovered else self.button_color
        arcade.draw_rectangle_filled(self.button_x, self.button_y, self.button_width, self.button_height, button_color)
        arcade.draw_rectangle_outline(self.button_x, self.button_y, self.button_width, self.button_height,
                                      arcade.color.BLACK, 2)
        arcade.draw_text("Начать игру", self.button_x, self.button_y, self.text_color,
                         font_size=20, anchor_x="center", anchor_y="center")

    def on_mouse_motion(self, x, y, dx, dy):
        if (self.button_x - self.button_width // 2 < x < self.button_x + self.button_width // 2 and
                self.button_y - self.button_height // 2 < y < self.button_y + self.button_height // 2):
            self.is_hovered = True
        else:
            self.is_hovered = False

    def on_mouse_press(self, x, y, button, mods):
        if (self.button_x - self.button_width // 2 < x < self.button_x + self.button_width // 2 and
                self.button_y - self.button_height // 2 < y < self.button_y + self.button_height // 2):
            print("Кнопка начать игру нажата!")
            self.game_window = Game_Window()
            self.close()


class Game_Window(arcade.Window):

    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "Игра")
        arcade.set_background_color(arcade.color.GRAY)
        self.scale_person = 0.3
        self.speed = 250
        self.health = 100
        self.idle_texture = arcade.load_texture("images/spp.png")
        self.texture = self.idle_texture
        self.cent_x = self.width // 2
        self.cent_y = self.height // 2
        self.is_walking = False
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False

    def update(self, delta_time):
        old_x = self.cent_x
        old_y = self.cent_y
        if self.up_pressed:
            self.cent_y += self.speed * delta_time
        if self.down_pressed:
            self.cent_y -= self.speed * delta_time
        if self.left_pressed:
            self.cent_x -= self.speed * delta_time
        if self.right_pressed:
            self.cent_x += self.speed * delta_time
        half_width = (self.texture.width * self.scale_person) / 2
        half_height = (self.texture.height * self.scale_person) / 2

        self.cent_x = max(half_width, min(WIDTH - half_width, self.cent_x))
        self.cent_y = max(half_height, min(HEIGHT - half_height, self.cent_y))
        self.is_walking = self.cent_x != old_x or self.cent_y != old_y

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(
            self.cent_x,
            self.cent_y,
            self.texture.width * self.scale_person,
            self.texture.height * self.scale_person,
            self.texture
        )

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.W:
            self.up_pressed = True
        elif symbol == arcade.key.S:
            self.down_pressed = True
        elif symbol == arcade.key.A:
            self.left_pressed = True
        elif symbol == arcade.key.D:
            self.right_pressed = True

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.W:
            self.up_pressed = False
        elif symbol == arcade.key.S:
            self.down_pressed = False
        elif symbol == arcade.key.A:
            self.left_pressed = False
        elif symbol == arcade.key.D:
            self.right_pressed = False


def main():
    start_window = Start_Window(WIDTH, HEIGHT, TITLE)
    arcade.run()


if __name__ == "__main__":
    main()

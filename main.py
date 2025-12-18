import arcade
import random
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Limbo - World's Hardest Maze Game"


class Wall:
    """Простой класс для стены"""

    def __init__(self, x1, y1, x2, y2, thickness=10):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.thickness = thickness

    def check_collision(self, px, py, radius):
        """Проверка столкновения с кругом"""
        if self.x1 == self.x2:
            dist_x = abs(px - self.x1)
            min_y = min(self.y1, self.y2)
            max_y = max(self.y1, self.y2)
            if min_y - radius <= py <= max_y + radius:
                return (self.x1, py, dist_x)
        elif self.y1 == self.y2:
            dist_y = abs(py - self.y1)
            min_x = min(self.x1, self.x2)
            max_x = max(self.x1, self.x2)
            if min_x - radius <= px <= max_x + radius:
                return (px, self.y1, dist_y)
        return None

    def draw(self):
        """Рисование стены"""
        arcade.draw_line(self.x1, self.y1, self.x2, self.y2,
                         arcade.color.BLACK, self.thickness)


class MazeGenerator:

    def __init__(self):
        self.levels = []
        self.create_levels()

    def create_levels(self):
        """Создание уровней лабиринта"""
        level1 = [
            Wall(50, 50, SCREEN_WIDTH - 50, 50, 20),
            Wall(50, SCREEN_HEIGHT - 50, SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50, 20),
            Wall(50, 50, 50, SCREEN_HEIGHT - 50, 20),
            Wall(SCREEN_WIDTH - 50, 50, SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50, 20),

            Wall(200, 100, 200, 400, 15),
            Wall(400, 200, 400, 500, 15),
            Wall(600, 100, 600, 300, 15),
        ]

        level2 = [
            Wall(50, 50, SCREEN_WIDTH - 50, 50, 20),
            Wall(50, SCREEN_HEIGHT - 50, SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50, 20),
            Wall(50, 50, 50, SCREEN_HEIGHT - 50, 20),
            Wall(SCREEN_WIDTH - 50, 50, SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50, 20),

            Wall(200, 100, 500, 100, 12),
            Wall(500, 100, 500, 300, 12),
            Wall(300, 300, 600, 300, 12),
            Wall(300, 300, 300, 500, 12),
            Wall(100, 400, 400, 400, 12),
        ]
        level3 = [
            Wall(50, 50, SCREEN_WIDTH - 50, 50, 20),
            Wall(50, SCREEN_HEIGHT - 50, SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50, 20),
            Wall(50, 50, 50, SCREEN_HEIGHT - 50, 20),
            Wall(SCREEN_WIDTH - 50, 50, SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50, 20),

            Wall(150, 100, 150, 500, 10),
            Wall(150, 500, 650, 500, 10),
            Wall(300, 150, 300, 350, 10),
            Wall(450, 250, 450, 450, 10),
            Wall(600, 150, 600, 400, 10),
            Wall(150, 100, 400, 100, 10),
            Wall(500, 200, 700, 200, 10),
        ]

        level4 = [
            Wall(50, 50, SCREEN_WIDTH - 50, 50, 20),
            Wall(50, SCREEN_HEIGHT - 50, SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50, 20),
            Wall(50, 50, 50, SCREEN_HEIGHT - 50, 20),
            Wall(SCREEN_WIDTH - 50, 50, SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50, 20),
            Wall(100, 100, 700, 100, 8),
            Wall(700, 100, 700, 500, 8),
            Wall(100, 500, 700, 500, 8),
            Wall(100, 100, 100, 500, 8),
            Wall(200, 200, 600, 200, 8),
            Wall(200, 300, 600, 300, 8),
            Wall(200, 400, 600, 400, 8),
            Wall(200, 200, 200, 400, 8),
            Wall(400, 200, 400, 400, 8),
            Wall(600, 200, 600, 400, 8),
        ]

        self.levels = [level1, level2, level3, level4]

    def get_level(self, level_index):
        """Получить уровень по индексу"""
        if 0 <= level_index < len(self.levels):
            return self.levels[level_index]
        return self.levels[0]


class Limbo(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.LIGHT_GRAY)
        self.player = None
        self.walls = []
        self.keys_pressed = set()
        self.wall_generator = MazeGenerator()
        self.current_level = 0
        self.total_levels = len(self.wall_generator.levels)
        self.targets = []
        self.score = 0
        self.target_count = 8
        self.level_score = 0

    def setup(self, level=0):
        self.current_level = level
        self.level_score = 0
        if level == 0:
            self.player = {'x': 100, 'y': 100}
        elif level % 2 == 0:
            self.player = {'x': 100, 'y': 100}
        else:
            self.player = {'x': SCREEN_WIDTH - 100, 'y': SCREEN_HEIGHT - 100}

        self.player.update({
            'radius': 15,
            'color': arcade.color.BLUE,
            'speed': 250 + (level * 10)
        })
        self.walls = self.wall_generator.get_level(level)
        self.targets = []
        attempts = 0
        while len(self.targets) < self.target_count and attempts < 1000:
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            valid_position = True
            for wall in self.walls:
                collision = wall.check_collision(x, y, 10)
                if collision and collision[2] < 10 + wall.thickness / 2:
                    valid_position = False
                    break
            if valid_position:
                dist_to_player = math.sqrt((x - self.player['x']) ** 2 +
                                           (y - self.player['y']) ** 2)
                if dist_to_player > 100:
                    self.targets.append({
                        'x': x,
                        'y': y,
                        'radius': 8,
                        'color': arcade.color.RED
                    })

            attempts += 1

    def check_wall_collision(self, new_x, new_y):
        """Проверяем столкновение с любой стеной"""
        for wall in self.walls:
            collision = wall.check_collision(new_x, new_y, self.player['radius'])
            if collision and collision[2] < self.player['radius'] + wall.thickness / 2:
                return True
        return False

    def check_target_collision(self):
        """Проверяем столкновение с целями"""
        collected = []
        for i, target in enumerate(self.targets):
            distance = math.sqrt((self.player['x'] - target['x']) ** 2 +
                                 (self.player['y'] - target['y']) ** 2)
            if distance < self.player['radius'] + target['radius']:
                collected.append(i)
                self.score += 1
                self.level_score += 1
        for i in sorted(collected, reverse=True):
            self.targets.pop(i)
        if not self.targets:
            if self.current_level < self.total_levels - 1:
                self.current_level += 1
                self.setup(self.current_level)
            else:
                self.score = 0
                self.setup(0)

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)
        if arcade.key.KEY_1 <= key <= arcade.key.KEY_9:
            level = key - arcade.key.KEY_1
            if level < self.total_levels:
                self.setup(level)
        elif key == arcade.key.N:
            if self.current_level < self.total_levels - 1:
                self.setup(self.current_level + 1)
        elif key == arcade.key.P:
            if self.current_level > 0:
                self.setup(self.current_level - 1)
        elif key == arcade.key.R:
            self.setup(self.current_level)

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)

    def on_update(self, delta_time):
        old_x, old_y = self.player['x'], self.player['y']
        dx, dy = 0, 0
        if arcade.key.LEFT in self.keys_pressed or arcade.key.A in self.keys_pressed:
            dx -= self.player['speed'] * delta_time
        if arcade.key.RIGHT in self.keys_pressed or arcade.key.D in self.keys_pressed:
            dx += self.player['speed'] * delta_time
        if arcade.key.UP in self.keys_pressed or arcade.key.W in self.keys_pressed:
            dy += self.player['speed'] * delta_time
        if arcade.key.DOWN in self.keys_pressed or arcade.key.S in self.keys_pressed:
            dy -= self.player['speed'] * delta_time

        if dx != 0 and dy != 0:
            factor = 0.7071
            dx *= factor
            dy *= factor
        new_x = old_x + dx
        if not self.check_wall_collision(new_x, old_y):
            self.player['x'] = new_x
        else:
            small_step = dx / 10
            for _ in range(10):
                test_x = old_x + small_step
                if not self.check_wall_collision(test_x, old_y):
                    self.player['x'] = test_x
                    old_x = test_x

        new_y = old_y + dy
        if not self.check_wall_collision(self.player['x'], new_y):
            self.player['y'] = new_y
        else:
            small_step = dy / 10
            for _ in range(10):
                test_y = old_y + small_step
                if not self.check_wall_collision(self.player['x'], test_y):
                    self.player['y'] = test_y
                    old_y = test_y
        self.check_target_collision()

    def on_draw(self):
        self.clear()

        # Рисуем стены
        for wall in self.walls:
            wall.draw()

        # Рисуем цели
        for target in self.targets:
            arcade.draw_circle_filled(target['x'], target['y'],
                                      target['radius'], target['color'])

        # Рисуем игрока
        arcade.draw_circle_filled(self.player['x'], self.player['y'],
                                  self.player['radius'], self.player['color'])

        arcade.draw_text(f"Уровень: {self.current_level + 1}/{self.total_levels}",
                         10, SCREEN_HEIGHT - 30, arcade.color.BLACK, 20)
        arcade.draw_text(f"Общий счет: {self.score}",
                         10, SCREEN_HEIGHT - 60, arcade.color.BLACK, 18)
        arcade.draw_text(f"Целей на уровне: {self.level_score}/{self.target_count}",
                         10, SCREEN_HEIGHT - 90, arcade.color.BLACK, 18)
        arcade.draw_text(f"Скорость: {self.player['speed']:.0f}",
                         10, SCREEN_HEIGHT - 120, arcade.color.BLACK, 16)
        arcade.draw_text("Управление: WASD/Стрелки",
                         10, 40, arcade.color.DARK_GRAY, 16)
        arcade.draw_text("1-9: Выбор уровня | N: Следующий | P: Предыдущий | R: Перезапуск",
                         10, 15, arcade.color.DARK_GRAY, 14)


def main():
    window = Limbo()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()

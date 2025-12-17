import arcade
import random
import math
import maze_generator
from pyglet.graphics import Batch

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Limbo - World's Hardest Maze Game"





class Limbo(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.LIGHT_GRAY)
        self.player = None
        self.walls = []
        self.keys_pressed = set()
        self.batch = Batch()
        
        # Генератор уровней
        self.wall_generator = maze_generator.WallGenerator()
        self.current_level = 0
        self.total_levels = len(self.wall_generator.levels)
        
        # Цели (шарики), которые нужно собрать
        self.targets = []
        self.score = 0
        self.target_count = 10  # Количество целей на уровень
        self.level_score = 0  # Счет на текущем уровне

    def setup(self, level=0):
        """Настройка уровня"""
        self.current_level = level
        self.level_score = 0
        
        # Игрок - начальная позиция зависит от уровня
        if level == 0:
            self.player = {'x': 100, 'y': 100}
        elif level % 2 == 0:
            self.player = {'x': 100, 'y': 100}
        else:
            self.player = {'x': SCREEN_WIDTH - 100, 'y': SCREEN_HEIGHT - 100}
            
        self.player.update({
            'radius': 15,
            'color': arcade.color.BLUE,
            'speed': 250 + (level * 10)  # Скорость увеличивается с уровнем
        })
        
        # Загружаем стены уровня
        self.walls = self.wall_generator.get_level(level)
        
        # Создаем цели (шарики)
        self.targets = []
        
        # Генерируем цели в свободных местах
        attempts = 0
        while len(self.targets) < self.target_count and attempts < 1000:
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            
            # Проверяем, чтобы цель не пересекалась со стенами
            valid_position = True
            for wall in self.walls:
                collision = wall.check_collision(x, y, 10)
                if collision and collision[2] < 10 + wall.thickness / 2:
                    valid_position = False
                    break
            
            # Проверяем, чтобы цель не была слишком близко к игроку
            if valid_position:
                dist_to_player = math.sqrt((x - self.player['x'])**2 + 
                                          (y - self.player['y'])**2)
                if dist_to_player > 100:
                    self.targets.append({
                        'x': x,
                        'y': y,
                        'radius': 10,
                        'color': arcade.color.RED
                    })
            
            attempts += 1

    def check_wall_collision(self, new_x, new_y):
        """Проверяем столкновение с любой стеной"""
        for wall in self.walls:
            collision = wall.check_collision(new_x, new_y, self.player['radius'])
            if collision:
                return True
        return False

    def check_target_collision(self):
        """Проверяем столкновение с целями"""
        collected = []
        for i, target in enumerate(self.targets):
            distance = math.sqrt((self.player['x'] - target['x'])**2 + 
                                (self.player['y'] - target['y'])**2)
            if distance < self.player['radius'] + target['radius']:
                collected.append(i)
                self.score += 1
                self.level_score += 1
        
        # Удаляем собранные цели
        for i in sorted(collected, reverse=True):
            self.targets.pop(i)
        
        # Если все цели собраны, переходим на следующий уровень
        if not self.targets:
            if self.current_level < self.total_levels - 1:
                self.current_level += 1
                self.setup(self.current_level)
            else:
                # Игра пройдена
                self.current_level = 0
                self.setup(0)

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)
        
        # Переключение уровней клавишами 1-9
        if arcade.key.KEY_1 <= key <= arcade.key.KEY_9:
            level = key - arcade.key.KEY_1
            if level < self.total_levels:
                self.setup(level)
        
        # Следующий/предыдущий уровень
        elif key == arcade.key.N:
            if self.current_level < self.total_levels - 1:
                self.setup(self.current_level + 1)
        elif key == arcade.key.P:
            if self.current_level > 0:
                self.setup(self.current_level - 1)
        
        # Сброс уровня
        elif key == arcade.key.R:
            self.setup(self.current_level)

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)

    def on_update(self, delta_time):
        # Сохраняем старую позицию
        old_x, old_y = self.player['x'], self.player['y']
        
        # Вычисляем новую позицию
        dx, dy = 0, 0
        if arcade.key.LEFT in self.keys_pressed or arcade.key.A in self.keys_pressed:
            dx -= self.player['speed'] * delta_time
        if arcade.key.RIGHT in self.keys_pressed or arcade.key.D in self.keys_pressed:
            dx += self.player['speed'] * delta_time
        if arcade.key.UP in self.keys_pressed or arcade.key.W in self.keys_pressed:
            dy += self.player['speed'] * delta_time
        if arcade.key.DOWN in self.keys_pressed or arcade.key.S in self.keys_pressed:
            dy -= self.player['speed'] * delta_time

        # Корректировка диагонального движения
        if dx != 0 and dy != 0:
            factor = 0.7071
            dx *= factor
            dy *= factor

        # Пробуем переместиться по X
        new_x = old_x + dx
        if not self.check_wall_collision(new_x, old_y):
            self.player['x'] = new_x
        else:
            # Если столкнулись, пробуем скользить вдоль стены
            small_step = dx / 10
            for _ in range(10):
                test_x = old_x + small_step
                if not self.check_wall_collision(test_x, old_y):
                    self.player['x'] = test_x
                    old_x = test_x

        # Пробуем переместиться по Y
        new_y = old_y + dy
        if not self.check_wall_collision(self.player['x'], new_y):
            self.player['y'] = new_y
        else:
            # Если столкнулись, пробуем скользить вдоль стены
            small_step = dy / 10
            for _ in range(10):
                test_y = old_y + small_step
                if not self.check_wall_collision(self.player['x'], test_y):
                    self.player['y'] = test_y
                    old_y = test_y

        # Проверяем столкновения с целями
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
        
        # Отображаем информацию
        arcade.draw_text(f"Уровень: {self.current_level + 1}/{self.total_levels}", 
                        10, SCREEN_HEIGHT - 30, arcade.color.BLACK, 20)
        arcade.draw_text(f"Общий счет: {self.score}", 
                        10, SCREEN_HEIGHT - 60, arcade.color.BLACK, 18)
        arcade.draw_text(f"Целей на уровне: {self.level_score}/{self.target_count}", 
                        10, SCREEN_HEIGHT - 90, arcade.color.BLACK, 18)
        
        # Отображаем инструкции
        arcade.draw_text("Управление: WASD/Стрелки", 
                        10, 40, arcade.color.DARK_GRAY, 16)
        arcade.draw_text("1-9: Выбор уровня | N: Следующий | P: Предыдущий | R: Перезапуск", 
                        10, 15, arcade.color.DARK_GRAY, 14)


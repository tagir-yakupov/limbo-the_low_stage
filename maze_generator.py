import math
import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Wall:
    def __init__(self, x1, y1, x2, y2, thickness, color=arcade.color.DARK_BROWN):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.thickness = thickness
    
    def draw(self):
        arcade.draw_line(self.x1, self.y1, self.x2, self.y2, 
                        self.color, self.thickness)
    
    def get_normal(self, point_x, point_y):
        """Получаем нормаль к стене для определения столкновения"""
        # Вектор стены
        wall_vec = (self.x2 - self.x1, self.y2 - self.y1)
        wall_length = math.sqrt(wall_vec[0]**2 + wall_vec[1]**2)
        
        if wall_length == 0:
            return (0, 0)
        
        # Нормализованный вектор стены
        wall_vec = (wall_vec[0] / wall_length, wall_vec[1] / wall_length)
        
        # Вектор от точки до начала стены
        to_point = (point_x - self.x1, point_y - self.y1)
        
        # Проекция на стену
        projection = to_point[0] * wall_vec[0] + to_point[1] * wall_vec[1]
        
        if projection < 0:
            # Ближе к началу стены
            return self._point_to_segment_distance(point_x, point_y, self.x1, self.y1)
        elif projection > wall_length:
            # Ближе к концу стены
            return self._point_to_segment_distance(point_x, point_y, self.x2, self.y2)
        else:
            # Проекция на саму стену
            closest_x = self.x1 + wall_vec[0] * projection
            closest_y = self.y1 + wall_vec[1] * projection
            dx = point_x - closest_x
            dy = point_y - closest_y
            distance = math.sqrt(dx**2 + dy**2)
            return (dx, dy, distance)
    
    def _point_to_segment_distance(self, px, py, sx, sy):
        dx = px - sx
        dy = py - sy
        distance = math.sqrt(dx**2 + dy**2)
        return (dx, dy, distance)
    
    def check_collision(self, x, y, radius):
        """Проверяем столкновение круга со стеной"""
        # Получаем вектор до ближайшей точки на стене
        result = self.get_normal(x, y)
        
        if len(result) == 3:
            dx, dy, distance = result
            if distance < radius + self.thickness / 2:
                return (dx, dy, distance)
        return None


class WallGenerator:
    def __init__(self):
        self.levels = []
        self.generate_levels()
    
    def generate_levels(self):
        # Уровень 1: Простой лабиринт для обучения
        self.levels.append([
            Wall(0, 0, 0, SCREEN_HEIGHT, 100),
            Wall(0, 0, SCREEN_WIDTH, 0, 100),
            Wall(0, SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, 100),
            Wall(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, 0, 100),
            Wall(200, 100, 200, 400, 30),
            Wall(600, 200, 600, 500, 30),
        ])
        
        # Уровень 2: Worlds Hardest Game стиль - узкие коридоры
        self.levels.append([
            Wall(0, 0, 0, SCREEN_HEIGHT, 100),
            Wall(0, 0, SCREEN_WIDTH, 0, 100),
            Wall(0, SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, 100),
            Wall(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, 0, 100),
            Wall(150, 100, 150, 500, 20),
            Wall(650, 100, 650, 500, 20),
            Wall(150, 100, 650, 100, 20),
            Wall(200, 500, 650, 500, 20),
        ])
        
        # Уровень 3: Крестообразная структура
        self.levels.append([
            Wall(0, 0, 0, SCREEN_HEIGHT, 100),
            Wall(0, 0, SCREEN_WIDTH, 0, 100),
            Wall(0, SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, 100),
            Wall(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, 0, 100),
            Wall(300, 100, 300, 500, 30),
            Wall(100, 300, 500, 300, 30),
        ])
        
        # Уровень 4: Worlds Hardest Game - узкие ворота
        self.levels.append([
            Wall(0, 0, 0, SCREEN_HEIGHT, 100),
            Wall(0, 0, SCREEN_WIDTH, 0, 100),
            Wall(0, SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, 100),
            Wall(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, 0, 100),
            Wall(200, 100, 200, 500, 40),
            Wall(400, 100, 400, 500, 40),
            Wall(600, 100, 600, 500, 40),
            Wall(200, 200, 400, 200, 40),
            Wall(400, 300, 600, 300, 40),
            Wall(200, 400, 600, 400, 40),
        ])
        
        # Уровень 5: Зигзагообразный путь
        self.levels.append([
            Wall(0, 0, 0, SCREEN_HEIGHT, 100),
            Wall(0, 0, SCREEN_WIDTH, 0, 100),
            Wall(0, SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, 100),
            Wall(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, 0, 100),
            Wall(100, 150, 700, 150, 25),
            Wall(100, 150, 100, 450, 25),
            Wall(100, 450, 700, 450, 25),
            Wall(700, 450, 700, 250, 25),
            Wall(700, 250, 300, 250, 25),
        ])
        
        # Уровень 6: Worlds Hardest Game - лабиринт с тупиками
        self.levels.append([
            Wall(0, 0, 0, SCREEN_HEIGHT, 100),
            Wall(0, 0, SCREEN_WIDTH, 0, 100),
            Wall(0, SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, 100),
            Wall(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, 0, 100),
            Wall(150, 100, 150, 500, 35),
            Wall(300, 100, 300, 500, 35),
            Wall(450, 100, 450, 500, 35),
            Wall(600, 100, 600, 500, 35),
            Wall(150, 100, 650, 100, 35),
            Wall(150, 200, 650, 200, 35),
            Wall(150, 300, 650, 300, 35),
            Wall(150, 400, 650, 400, 35),
            Wall(150, 500, 650, 500, 35),
            Wall(300, 100, 300, 150, 35),
            Wall(450, 200, 450, 250, 35),
            Wall(600, 300, 600, 350, 35),
        ])
        
        # Уровень 7: Спираль
        self.levels.append([
            Wall(0, 0, 0, SCREEN_HEIGHT, 100),
            Wall(0, 0, SCREEN_WIDTH, 0, 100),
            Wall(0, SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, 100),
            Wall(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, 0, 100),
            Wall(100, 100, 700, 100, 30),
            Wall(700, 100, 700, 500, 30),
            Wall(700, 500, 200, 500, 30),
            Wall(200, 500, 200, 200, 30),
            Wall(200, 200, 600, 200, 30),
            Wall(600, 200, 600, 400, 30),
            Wall(600, 400, 300, 400, 30),
            Wall(300, 400, 300, 300, 30),
        ])
        
        # Уровень 8: Worlds Hardest Game - движущиеся стены (имитация)
        self.levels.append([
            Wall(0, 0, 0, SCREEN_HEIGHT, 100),
            Wall(0, 0, SCREEN_WIDTH, 0, 100),
            Wall(0, SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, 100),
            Wall(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, 0, 100),
            Wall(100, 100, 100, 500, 30),
            Wall(250, 100, 250, 500, 30),
            Wall(400, 100, 400, 500, 30),
            Wall(550, 100, 550, 500, 30),
            Wall(700, 100, 700, 500, 30),
            Wall(100, 200, 250, 200, 30),
            Wall(400, 300, 550, 300, 30),
            Wall(250, 400, 400, 400, 30),
            Wall(550, 150, 700, 150, 30),
        ])
        
        # Уровень 9: Решетка
        self.levels.append([
            Wall(0, 0, 0, SCREEN_HEIGHT, 100),
            Wall(0, 0, SCREEN_WIDTH, 0, 100),
            Wall(0, SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, 100),
            Wall(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, 0, 100),
            Wall(133, 100, 133, 500, 25),
            Wall(266, 100, 266, 500, 25),
            Wall(399, 100, 399, 500, 25),
            Wall(532, 100, 532, 500, 25),
            Wall(665, 100, 665, 500, 25),
            Wall(100, 133, 700, 133, 25),
            Wall(100, 266, 700, 266, 25),
            Wall(100, 399, 700, 399, 25),
            Wall(100, 532, 700, 532, 25),
        ])
        
        # Уровень 10: Worlds Hardest Game - финальный лабиринт
        self.levels.append([
            Wall(0, 0, 0, SCREEN_HEIGHT, 100),
            Wall(0, 0, SCREEN_WIDTH, 0, 100),
            Wall(0, SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, 100),
            Wall(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, 0, 100),
            Wall(100, 100, 100, 500, 40),
            Wall(700, 100, 700, 500, 40),
            Wall(100, 100, 300, 100, 40),
            Wall(500, 100, 700, 100, 40),
            Wall(100, 300, 250, 300, 40),
            Wall(350, 300, 700, 300, 40),
            Wall(100, 500, 700, 500, 40),
            Wall(300, 100, 300, 250, 40),
            Wall(500, 100, 500, 250, 40),
            Wall(250, 300, 250, 450, 40),
            Wall(550, 300, 550, 450, 40),
            Wall(150, 450, 400, 450, 40),
            Wall(450, 450, 650, 450, 40),
        ])
        
        # Уровень 11: Восьмерка
        self.levels.append([
            Wall(0, 0, 0, SCREEN_HEIGHT, 100),
            Wall(0, 0, SCREEN_WIDTH, 0, 100),
            Wall(0, SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, 100),
            Wall(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, 0, 100),
            Wall(200, 150, 600, 150, 30),
            Wall(200, 450, 600, 450, 30),
            Wall(200, 150, 200, 450, 30),
            Wall(600, 150, 600, 450, 30),
            Wall(400, 150, 400, 300, 30),
            Wall(400, 300, 600, 300, 30),
        ])
        
        # Уровень 12: Worlds Hardest Game - миниигры
        self.levels.append([
            Wall(0, 0, 0, SCREEN_HEIGHT, 100),
            Wall(0, 0, SCREEN_WIDTH, 0, 100),
            Wall(0, SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, 100),
            Wall(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, 0, 100),
            Wall(400, 0, 400, SCREEN_HEIGHT, 40),
            Wall(0, 300, SCREEN_WIDTH, 300, 40),
            Wall(100, 50, 100, 250, 25),
            Wall(300, 50, 300, 250, 25),
            Wall(500, 350, 500, 550, 25),
            Wall(700, 350, 700, 550, 25),
            Wall(100, 350, 100, 550, 25),
            Wall(300, 350, 300, 550, 25),
        ])
        
        # Уровень 13: Треугольный лабиринт
        self.levels.append([
            Wall(0, 0, 0, SCREEN_HEIGHT, 100),
            Wall(0, 0, SCREEN_WIDTH, 0, 100),
            Wall(0, SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, 100),
            Wall(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, 0, 100),
            Wall(200, 100, 600, 100, 30),
            Wall(200, 100, 400, 400, 30),
            Wall(400, 400, 600, 100, 30),
            Wall(200, 500, 600, 500, 30),
            Wall(200, 500, 400, 200, 30),
            Wall(400, 200, 600, 500, 30),
        ])
        
        # Уровень 14: Worlds Hardest Game - точное движение
        self.levels.append([
            Wall(0, 0, 0, SCREEN_HEIGHT, 100),
            Wall(0, 0, SCREEN_WIDTH, 0, 100),
            Wall(0, SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, 100),
            Wall(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, 0, 100),
            Wall(150, 100, 150, 500, 50),
            Wall(300, 100, 300, 500, 50),
            Wall(450, 100, 450, 500, 50),
            Wall(600, 100, 600, 500, 50),
            Wall(150, 100, 650, 100, 50),
            Wall(150, 500, 650, 500, 50),
            Wall(150, 200, 210, 200, 50),
            Wall(390, 200, 450, 200, 50),
            Wall(540, 200, 600, 200, 50),
            Wall(300, 300, 360, 300, 50),
            Wall(450, 300, 510, 300, 50),
        ])
        
        # Уровень 15: Шахматная доска
        self.levels.append([
            Wall(0, 0, 0, SCREEN_HEIGHT, 100),
            Wall(0, 0, SCREEN_WIDTH, 0, 100),
            Wall(0, SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, 100),
            Wall(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, 0, 100),
            Wall(160, 120, 160, 480, 40),
            Wall(320, 120, 320, 480, 40),
            Wall(480, 120, 480, 480, 40),
            Wall(640, 120, 640, 480, 40),
            Wall(80, 160, 720, 160, 40),
            Wall(80, 320, 720, 320, 40),
            Wall(80, 480, 720, 480, 40),
        ])
        
        # Уровень 16: Worlds Hardest Game - скрытые пути
        self.levels.append([
            Wall(0, 0, 0, SCREEN_HEIGHT, 100),
            Wall(0, 0, SCREEN_WIDTH, 0, 100),
            Wall(0, SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, 100),
            Wall(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, 0, 100),
            Wall(100, 100, 700, 100, 35),
            Wall(100, 100, 100, 500, 35),
            Wall(100, 500, 700, 500, 35),
            Wall(700, 500, 700, 100, 35),
            Wall(250, 100, 250, 300, 35),
            Wall(400, 300, 400, 500, 35),
            Wall(550, 100, 550, 300, 35),
            Wall(100, 250, 250, 250, 35),
            Wall(400, 250, 550, 250, 35),
            Wall(250, 400, 400, 400, 35),
            Wall(550, 400, 700, 400, 35),
        ])
        
        # Уровень 17: Кольца
        self.levels.append([
            Wall(0, 0, 0, SCREEN_HEIGHT, 100),
            Wall(0, 0, SCREEN_WIDTH, 0, 100),
            Wall(0, SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, 100),
            Wall(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, 0, 100),
            Wall(150, 150, 650, 150, 25),
            Wall(650, 150, 650, 450, 25),
            Wall(650, 450, 150, 450, 25),
            Wall(150, 450, 150, 150, 25),
            Wall(250, 250, 550, 250, 25),
            Wall(550, 250, 550, 350, 25),
            Wall(550, 350, 250, 350, 25),
            Wall(250, 350, 250, 250, 25),
        ])
        
        # Уровень 18: Worlds Hardest Game - финальный вызов
        self.levels.append([
            Wall(0, 0, 0, SCREEN_HEIGHT, 100),
            Wall(0, 0, SCREEN_WIDTH, 0, 100),
            Wall(0, SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, 100),
            Wall(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, 0, 100),
            Wall(100, 100, 100, 500, 40),
            Wall(700, 100, 700, 500, 40),
            Wall(100, 100, 700, 100, 40),
            Wall(100, 500, 700, 500, 40),
            Wall(200, 100, 200, 500, 30),
            Wall(300, 100, 300, 500, 30),
            Wall(400, 100, 400, 500, 30),
            Wall(500, 100, 500, 500, 30),
            Wall(600, 100, 600, 500, 30),
            Wall(100, 200, 700, 200, 30),
            Wall(100, 300, 700, 300, 30),
            Wall(100, 400, 700, 400, 30),
            Wall(200, 200, 300, 200, 30),
            Wall(400, 300, 500, 300, 30),
            Wall(300, 400, 400, 400, 30),
            Wall(500, 200, 600, 200, 30),
        ])
        
        # Уровень 19: Симметричный лабиринт
        self.levels.append([
            Wall(0, 0, 0, SCREEN_HEIGHT, 100),
            Wall(0, 0, SCREEN_WIDTH, 0, 100),
            Wall(0, SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, 100),
            Wall(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, 0, 100),
            Wall(400, 100, 400, 500, 40),
            Wall(200, 150, 600, 150, 30),
            Wall(200, 450, 600, 450, 30),
            Wall(200, 150, 200, 300, 30),
            Wall(600, 150, 600, 300, 30),
            Wall(200, 450, 200, 300, 30),
            Wall(600, 450, 600, 300, 30),
        ])
        
        # Уровень 20: Итоговый Worlds Hardest Game
        self.levels.append([
            Wall(0, 0, 0, SCREEN_HEIGHT, 100),
            Wall(0, 0, SCREEN_WIDTH, 0, 100),
            Wall(0, SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, 100),
            Wall(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, 0, 100),
            Wall(50, 50, 750, 50, 40),
            Wall(750, 50, 750, 550, 40),
            Wall(750, 550, 50, 550, 40),
            Wall(50, 550, 50, 50, 40),
            Wall(150, 150, 650, 150, 35),
            Wall(650, 150, 650, 450, 35),
            Wall(650, 450, 150, 450, 35),
            Wall(150, 450, 150, 150, 35),
            Wall(150, 150, 400, 400, 30),
            Wall(650, 150, 400, 400, 30),
            Wall(150, 450, 400, 200, 30),
            Wall(650, 450, 400, 200, 30),
            Wall(350, 275, 450, 275, 25),
            Wall(400, 225, 400, 325, 25),
            Wall(275, 275, 325, 275, 25),
            Wall(475, 275, 525, 275, 25),
            Wall(400, 175, 400, 225, 25),
            Wall(400, 325, 400, 375, 25),
        ])
    
    def get_level(self, level_number):
        """Возвращает стены для указанного уровня"""
        if 0 <= level_number < len(self.levels):
            return self.levels[level_number]
        return self.levels[0]
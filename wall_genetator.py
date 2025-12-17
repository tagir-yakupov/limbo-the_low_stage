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

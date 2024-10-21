import numpy as np
import matplotlib.pyplot as plt


class Shape:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

    def draw(self, field):
        """Абстрактный метод для отрисовки объекта на поле"""
        raise NotImplementedError


class Rectangle(Shape):
    def __init__(self, x, y, width, height, value):
        super().__init__(x, y, value)
        self.width = width
        self.height = height

    def draw(self, field):
        grid_x = int(self.x * field.resolution)
        grid_y = int(self.y * field.resolution)
        width_in_grid = int(self.width * field.resolution)
        height_in_grid = int(self.height * field.resolution)

        for i in range(grid_y, grid_y + height_in_grid):
            for j in range(grid_x, grid_x + width_in_grid):
                if 0 <= i < field.grid.shape[0] and 0 <= j < field.grid.shape[1]:
                    field.grid[i, j] = self.value


class Circle(Shape):
    def __init__(self, x, y, radius, value):
        super().__init__(x, y, value)
        self.radius = radius

    def draw(self, field):
        grid_x = int(self.x * field.resolution)
        grid_y = int(self.y * field.resolution)
        radius_in_grid = int(self.radius * field.resolution)

        for i in range(grid_y - radius_in_grid, grid_y + radius_in_grid):
            for j in range(grid_x - radius_in_grid, grid_x + radius_in_grid):
                if 0 <= i < field.grid.shape[0] and 0 <= j < field.grid.shape[1] and (i - grid_y) ** 2 + (
                        j - grid_x) ** 2 <= radius_in_grid ** 2:
                    field.grid[i, j] = self.value


class Field:
    def __init__(self, width=4, height=3.1, resolution=1000, case=0):
        self.width = width  # Ширина поля (4 м)
        self.height = height  # Высота поля (3.1 м)
        self.resolution = resolution  # Дискретизация (точек на метр)
        self.grid = np.zeros((int(height * resolution), int(width * resolution)))  # Карта поля
        self.case = case
        self.shapes = []

    def add_shape(self, shape):
        """Добавляет объект на поле"""
        self.shapes.append(shape)

    def draw(self):
        """Отрисовка всех объектов на поле"""
        for shape in self.shapes:
            shape.draw(self)

    def plot(self):
        """Визуализация карты"""
        plt.imshow(self.grid, cmap='tab20', origin='lower', extent=[0, self.width, 0, self.height])
        plt.grid(True)
        plt.show()


def create_field_with_case(case, resolution):
    field = Field(4, 3.1, resolution, case)

    # Общие объекты для всех кейсов
    common_objects = [
        Rectangle(0.05 + 1 + 0.05, 0.05 + 0.45, 0.55, 0.05, 1),  # горизонтальная средняя правая стенка
        Rectangle(0.05 + 1 + 0.05 + 0.55 + 0.7, 0.05 + 0.45, 0.55, 0.05, 1),
        Rectangle(0.05 + 1 + 0.05, 0.05 + 0.45 + 0.7 + 0.7 + 0.65, 0.55, 0.05, 3),
        Rectangle(0.05 + 1 + 0.05 + 0.55 + 0.7, 0.05 + 0.45 + 0.7 + 0.7 + 0.65, 0.55, 0.05, 1),
        Rectangle(0.05 + 1, 0.05 + 0.45, 0.05, 0.7, 1),  # горизонтальная средняя правая стенка
        Rectangle(0.05 + 1 + 0.05 + 0.55 + 0.7 + 0.55, 0.05 + 0.45, 0.05, 0.7, 1),
        Rectangle(0.05 + 1, 0.05 + 0.45 + 0.7 + 0.7, 0.05, 0.7, 1),  # горизонтальная средняя правая стенка
        Rectangle(0.05 + 1 + 0.05 + 0.55 + 0.7 + 0.55, 0.05 + 0.45 + 0.7 + 0.7, 0.05, 0.7, 1),
        Rectangle(0.05, 0, 3.9, 0.05, 2),  # нижняя граница
        Rectangle(0.05, 3.1 - 0.05, 3.9, 0.05, 2),  # верхняя граница
        Rectangle(0, 0, 0.05, 3.1, 2),  # левая граница
        Rectangle(4 - 0.05, 0, 0.05, 3.1, 2),  # правая граница
        Rectangle(0.05 + 1 + 0.05 + 0.55 + 0.2, 0.05, 0.3, 0.42, 4),  # левый прямоугольник
        Rectangle(0.05 + 1 + 0.05 + 0.55 + 0.2, 3.1 - 0.05 - 0.42, 0.3, 0.42, 4),  # правый прямоугольник
        Circle(2, 3.1 / 2, 0.05, 5)  # центральный круг
    ]

    # Добавляем общие объекты на поле
    for obj in common_objects:
        field.add_shape(obj)

    # Специфические объекты для каждого случая
    specific_objects = []
    if case == 0:
        specific_objects = [
            Rectangle(0.05 + 1 + 0.05 + 0.55, 0.05 + 0.45, 0.7, 0.05, 1),
            Rectangle(0.05 + 1 + 0.05 + 0.55, 0.05 + 0.45 + 0.7 + 0.7 + 0.65, 0.7, 0.05, 1),# верхняя средняя стенка
            Rectangle(0.05 + 1 + 0.05 + 0.55, 0.05 + 0.45 + 0.62 + 0.05, 0.7, 0.05, 3)
        ]
    elif case == 1:
        specific_objects = [
            Rectangle(0.05 + 1, 0.05 + 0.45 + 0.7, 0.05, 0.7, 1),
        ]
    elif case == 2:
        specific_objects = []
    elif case == 3:
        specific_objects = []
    elif case == 4:
        specific_objects = []
    else:
        print("Incorrect value")

    # Добавляем специфические объекты на поле
    for obj in specific_objects:
        field.add_shape(obj)

    return field




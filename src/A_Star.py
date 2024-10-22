import cv2
import numpy as np
import matplotlib.pyplot as plt
import time

A_STAR_SPACE = 0xFFFFFFFF
A_STAR_WALL = 0xFFFFFFFE


def mass_center(c):
    contour_size = len(c)
    x = 0
    y = 0
    for i in range(contour_size):
        x = x + c[0, 0, 0]
        y = x + c[0, 0, 1]
    x = x / contour_size
    y = y / contour_size
    return np.array([x, y])


class astar:
    def __init__(self):
        self.map = None  # 2D list for map
        self.xs = 0
        self.ys = 0
        self.px = None  # list of x-coordinates of the path
        self.py = None  # list of y-coordinates of the path
        self.ps = 0  # path length

    def _freemap(self):
        """Release the memory of the map."""
        self.map = None
        self.xs = 0
        self.ys = 0

    def _freepnt(self):
        """Release the memory of the path points."""
        self.px = None
        self.py = None
        self.ps = 0

    def resize(self, _xs, _ys):
        """Resize the map to new dimensions."""
        if self.xs == _xs and self.ys == _ys:
            return
        self._freemap()
        self.xs = _xs
        self.ys = _ys
        self.map = [[A_STAR_SPACE for _ in range(self.xs)] for _ in range(self.ys)]

    def set(self, bitmap, col_wall):
        """Set the map using a bitmap (2D list) with a specific wall color."""
        self.resize(len(bitmap[0]), len(bitmap))
        for y in range(self.ys):
            for x in range(self.xs):
                self.map[y][x] = A_STAR_WALL if bitmap[y][x] == col_wall else A_STAR_SPACE

    def get(self):
        """Return the map for debugging purposes."""
        return [[self.map[y][x] for x in range(self.xs)] for y in range(self.ys)]

    def compute(self, x0, y0, x1, y1):
        start = time.time()
        """Compute the path from (x0, y0) to (x1, y1) using the A* algorithm."""
        # Clear previous paths
        for y in range(self.ys):
            for x in range(self.xs):
                if self.map[y][x] != A_STAR_WALL:
                    self.map[y][x] = A_STAR_SPACE

        self._freepnt()

        # Init points lists for BFS-like exploration
        i0 = 0
        i1 = self.xs * self.ys
        n0 = 0
        n1 = 0
        px = [0] * (i1 * 2)
        py = [0] * (i1 * 2)

        if self.map[y0][x0] == A_STAR_SPACE:
            px[i0 + n0] = x0
            py[i0 + n0] = y0
            n0 += 1
            self.map[y0][x0] = 0

            for j in range(1, self.xs * self.ys):
                if self.map[y1][x1] != A_STAR_SPACE:
                    break

                e = False
                for ii in range(i0, i0 + n0):
                    x, y = px[ii], py[ii]

                    # Test neighbors
                    for yy, xx in [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]:
                        if 0 <= yy < self.ys and 0 <= xx < self.xs and self.map[yy][xx] == A_STAR_SPACE:
                            self.map[yy][xx] = j
                            px[i1 + n1] = xx
                            py[i1 + n1] = yy
                            n1 += 1
                            e = True

                if not e:
                    break

                # Swap the lists
                i0, i1 = i1, i0
                n0, n1 = n1, 0

        # Reconstruct path if found
        if self.map[y1][x1] == A_STAR_SPACE or self.map[y1][x1] == A_STAR_WALL:
            return  # No path found

        self.ps = self.map[y1][x1] + 1
        self.px = [0] * self.ps
        self.py = [0] * self.ps

        x, y = x1, y1
        for i in range(self.ps - 1, -1, -1):
            self.px[i] = x
            self.py[i] = y

            if y > 0 and self.map[y - 1][x] == i - 1:
                y -= 1
            elif y < self.ys - 1 and self.map[y + 1][x] == i - 1:
                y += 1
            elif x > 0 and self.map[y][x - 1] == i - 1:
                x -= 1
            elif x < self.xs - 1 and self.map[y][x + 1] == i - 1:
                x += 1
        end = time.time()
        print("Время работы алгоритма", end - start)

    @staticmethod
    def contours(image):

        # Преобразуем изображение в градации серого
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        edges = cv2.Canny(gray, 200, 700)
        # Найдем контуры
        contours, _ = cv2.findContours(edges, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        largest_contour = max(contours, key=cv2.contourArea)
        largest_contour_area = cv2.contourArea(largest_contour)

        new_contours = []
        for c in contours:
            epsilon = 0.0005 * cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, epsilon, True)
            if cv2.contourArea(approx) / largest_contour_area > 0.01 and cv2.contourArea(
                    approx) / largest_contour_area < 0.2:
                new_contours.append(approx)

        x, y, w, h = cv2.boundingRect(largest_contour)

        rect = cv2.minAreaRect(largest_contour)
        box = cv2.boxPoints(rect)
        box = np.intp(box)

        k = 400 / w

        step_coeff = 50
        not_contours = []
        for c in new_contours:
            contour_size = len(c)
            for i in range(contour_size - 1):
                x0, y0 = c[i, 0, 1], c[i, 0, 0]
                x1, y1 = c[i + 1, 0, 1], c[i + 1, 0, 0]
                if x0 != x1:
                    a = (y1 - y0) / (x1 - x0)
                    b = y0 - a * x0
                    for x_t in range(x0 * step_coeff, (x1) * step_coeff + 1):
                        y_t = a * x_t / step_coeff + b
                        not_contours.append([np.int32(k * (x_t / step_coeff - x)), np.int32(k * (y_t - y))])
                else:
                    a = (x1 - x0) / (y1 - y0)
                    b = x0 - a * y0
                    for y_t in range(y0 * step_coeff, (y1 * step_coeff) + 1):
                        x_t = a * y_t / step_coeff + b
                        not_contours.append([np.int32(k * (x_t - x)), np.int32(k * (y_t / step_coeff - y))])
        return not_contours

    @staticmethod
    def mass_center(c):
        contour_size = len(c)
        x = 0
        y = 0
        for i in range(contour_size):
            x = x + c[0, 0, 0]
            y = x + c[0, 0, 1]
        x = x / contour_size
        y = y / contour_size
        return np.array([x, y])

    @staticmethod
    def get_matrix(not_contours):
        size_x = 400
        size_y = 310
        bitmap = [[0 for _ in range(size_x)] for _ in range(size_y)]
        for c in not_contours:
            if 1 <= c[0] < 310 and 1 <= c[1] < 399:
                # Выставляем единицу в клетке (x, y)
                bitmap[310 - c[0]][c[1]] = 1

                # Выставляем единицы во всех клетках (a, b), где a <= c[0] + 15 и b <= c[1] + 15
                for a in range(c[0], min(c[0] + 20, 310)):  # Ограничение по высоте
                    for b in range(c[1], min(c[1] + 20, 399)):  # Ограничение по ширине
                        bitmap[310 - a][b] = 1
            else:
                print(c)
                break
        return bitmap

    def calculate_segment_info(self, segments):
        info = []  # Список для хранения информации о сегментах

        directions = {
            (1, 0): 'right',  # Движение по X+
            (-1, 0): 'left',  # Движение по X-
            (0, 1): 'вверх',  # Движение по Y+
            (0, -1): 'вниз'  # Движение по Y-
        }

        previous_direction = None
        i = 0
        for segment in segments:
            # Длина отрезка
            start = segment[0]
            end = segment[-1]
            length = abs(end[0] - start[0]) + abs(end[1] - start[1])

            # Определение направления
            if start[0] == end[0]:  # Вертикальный сегмент
                direction = (0, 1 if end[1] > start[1] else -1)
            else:  # Горизонтальный сегмент
                direction = (1 if end[0] > start[0] else -1, 0)

            if i == 0:
                info.append(('null', length))
            # Определение поворота
            if previous_direction:
                if (previous_direction[0] == 0 and direction[0] != 0) or (
                        previous_direction[1] == 0 and direction[1] != 0):
                    # Определяем, был ли поворот вправо или влево
                    if previous_direction[0] == 0:  # Вертикальный
                        turn = 'right' if direction[0] == 1 else 'left'
                    else:  # Горизонтальный
                        turn = 'right' if direction[1] == -1 else 'left'
                    info.append((turn, length))
            i += 1
            previous_direction = direction

        return info

    def path_segments(self, coords):
        if len(coords) < 2:
            return []

        segments = []  # Список для хранения отрезков
        current_segment = [coords[0]]
        X_flag = False
        Y_flag = False
        counter = 0
        i = 1
        while i < len(coords):
            c = coords[i]
            k = current_segment
            a = coords[i][0]
            b = current_segment[-1][0]
            # Проверяем, является ли следующая точка продолжением текущего отрезка
            if coords[i][0] == current_segment[-1][0] and counter == 0:
                X_flag = True
                current_segment.append(coords[i])
                counter += 1
                i += 1
            elif coords[i][1] == current_segment[-1][1] and counter == 0:
                Y_flag = True
                current_segment.append(coords[i])
                counter += 1
                i += 1
            elif coords[i][0] == current_segment[-1][0] and counter != 0:
                if Y_flag == True:
                    Y_flag = False
                    segments.append(current_segment)
                    current_segment = [coords[i - 1]]
                    counter = 0

                else:
                    current_segment.append(coords[i])
                    counter += 1
                    i += 1
            elif coords[i][1] == current_segment[-1][1] and counter != 0:
                if X_flag == True:
                    X_flag = False
                    segments.append(current_segment)
                    current_segment = [coords[i - 1]]
                    counter = 0

                else:
                    current_segment.append(coords[i])
                    counter += 1
                    i += 1

        # Не забудьте добавить последний сегмент
        segments.append(current_segment)
        info = self.calculate_segment_info(segments)

        return info

    def get_trajectory(self, bitmap, start_x, start_y, end_x, end_y):
        size_x = 400
        size_y = 310
        # a = astar()
        self.resize(size_x, size_y)
        self.set(bitmap, 1)
        X_border = []
        Y_border = []
        self.compute(start_x, start_y, end_x, end_y)
        for i in range(size_y):
            for j in range(size_x):
                if self.map[i][j] == 0xFFFFFFFE:
                    X_border.append(j)
                    Y_border.append(i)
        X = self.px
        Y = self.py
        coord = list(zip(X, Y))
        return coord, X, Y, X_border, Y_border

    @staticmethod
    def draw_trajectory(coord, image, start_x, start_y, end_x, end_y, X, Y, X_border, Y_border):
        size_x = 400
        size_y = 310
        L = len(coord)
        new_coord = []
        new_coord.append(coord[0])
        if coord[1][0] == coord[0][0]:
            axes_path = "X"
        else:
            axes_path = "Y"
        X_path = []
        Y_path = []
        X_path.append(coord[0][0])
        Y_path.append(coord[0][1])

        for i in range(1, L - 1):
            if coord[i - 1][0] == coord[i][0]:
                if axes_path == "Y":
                    X_path.append(coord[i - 1][0])
                    Y_path.append(coord[i - 1][1])
                    axes_path = "X"
            if coord[i - 1][1] == coord[i][1]:
                if axes_path == "X":
                    X_path.append(coord[i - 1][0])
                    Y_path.append(coord[i - 1][1])
                    axes_path = "Y"
        X_path.append(coord[L - 1][0])
        Y_path.append(coord[L - 1][1])

        fig, ax = plt.subplots()
        ax.set_xlim([0, size_x])
        ax.set_ylim([0, size_y])
        image = cv2.resize(image, (400, 310))
        image = cv2.flip(image, 0)

        ax.plot(start_x, start_y, "r*")
        ax.plot(end_x, end_y, "r*")
        ax.plot(X, Y)
        ax.plot(X_path, Y_path, '.r')
        ax.plot(X_border, Y_border, "k.")
        ax.imshow(image)
        ax.grid()
        plt.show()

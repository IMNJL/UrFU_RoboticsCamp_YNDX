import cv2
import numpy as np
import matplotlib.pyplot as plt
A_STAR_SPACE = 0xFFFFFFFF
A_STAR_WALL = 0xFFFFFFFE
class astar:
    def __init__(self):
        self.map = None  # 2D list for map
        self.xs = 0
        self.ys = 0
        self.px = None  # list of x-coordinates of the path
        self.py = None  # list of y-coordinates of the path
        self.ps = 0     # path length

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
                    for yy, xx in [(y-1, x), (y+1, x), (y, x-1), (y, x+1)]:
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

            if y > 0 and self.map[y-1][x] == i - 1:
                y -= 1
            elif y < self.ys - 1 and self.map[y+1][x] == i - 1:
                y += 1
            elif x > 0 and self.map[y][x-1] == i - 1:
                x -= 1
            elif x < self.xs - 1 and self.map[y][x+1] == i - 1:
                x += 1





image = cv2.imread('maze.png')
# print(image.shape)
################### unnecessary
# hMin = 0
# sMin = 0
# vMin = 50
# hMax = 255
# sMax = 255
# vMax = 255
# lower = np.array([hMin, sMin, vMin])
# upper = np.array([hMax, sMax, vMax])
# # Create HSV Image and threshold into a range.
# hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
# mask = cv2.inRange(hsv, lower, upper)
# output = cv2.bitwise_and(image,image, mask= mask)
# image = output
# # image = np.maximum(image, 20)
#########################################



# Преобразуем изображение в градации серого

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


################### unnecessary
# Применим размытие для устранения шумов
# gray= cv2.GaussianBlur(gray, (5, 5), 0)
# kernel = np.ones((5, 5), 'uint8')
# gray = cv2.erode(gray, kernel, iterations=1) 
# gray = cv2.dilate(gray, kernel, iterations=1)
#################################



cv2.namedWindow('canny', cv2.WINDOW_NORMAL)
edges = cv2.Canny(gray, 200, 700)
cv2.imshow('canny',edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
# Найдем контуры
contours, _ = cv2.findContours(edges, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

# Отобразим контуры на изображении
contour_image = image.copy()
contour_image_test = image.copy()
contour_image_test_test = image.copy()
contour_image_test_3= image.copy()

cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)

# Отобразим результат
cv2.namedWindow('Contours', cv2.WINDOW_NORMAL)
cv2.imshow('Contours', contour_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Определим границы лабиринта
# Мы предполагаем, что самые большие контуры соответствуют границам лабиринта
# Отбираем контур с наибольшей площадью

largest_contour = max(contours, key=cv2.contourArea)
largest_contour_area = cv2.contourArea(largest_contour)
# print(largest_contour_area)



cv2.drawContours(contour_image_test_3, [largest_contour], -1, (0, 255, 0), 2)
cv2.namedWindow('largest', cv2.WINDOW_NORMAL)
cv2.imshow('largest',contour_image_test_3)
cv2.waitKey(0)
cv2.destroyAllWindows()

areas = [cv2.contourArea(c) for c in contours]
areas.sort()
# print(areas)
# Подбираем объекты примерно нужного размера
new_contours = []
for c in contours:
        epsilon = 0.0005*cv2.arcLength(c,True)
        approx = cv2.approxPolyDP(c,epsilon,True)
        new_contours.append(approx)


cv2.namedWindow('Contours', cv2.WINDOW_NORMAL)
cv2.drawContours(contour_image_test_3,new_contours ,-1,(0,0,255),2)
cv2.imshow('Contours', contour_image_test_3)
cv2.waitKey(0)
cv2.destroyAllWindows()


def mass_center(c):
        contour_size = len(c)
        x = 0
        y = 0
        for i in range(contour_size):
                x = x + c[0,0,0]
                y = x + c[0,0,1]
        x = x/contour_size
        y = y/contour_size
        return np.array([x,y])     

# Исключение лишних контуров по критерию площади
new_new_contours = []
for c in new_contours:
    if cv2.contourArea(c)/largest_contour_area> 0.01 and cv2.contourArea(c)/largest_contour_area < 0.2:
#       if cv2.contourArea(c)> and cv2.contourArea(c)/largest_contour_area < 0.5:
        new_new_contours.append(c)
new_contours = new_new_contours
# print(new_contours[0][0,:,:])

# Исключение дубликатов конутров



# print([cv2.contourArea(c) for c in new_contours])
areas = [(cv2.contourArea(c), cv2.contourArea(c)/largest_contour_area, mass_center(c)) for c in new_contours]
areas.sort()
# print(areas)


cv2.namedWindow('filtered_contours', cv2.WINDOW_NORMAL)
cv2.drawContours(contour_image_test_test,new_contours ,-1,(0,0,255),2)
cv2.imshow('filtered_contours', contour_image_test_test)
cv2.waitKey(0)
cv2.destroyAllWindows()


# Вычисляем координаты ограничивающего прямоугольника (границы лабиринта)
x, y, w, h = cv2.boundingRect(largest_contour)
# print(f"Границы лабиринта: верхний левый угол ({x}, {y}), ширина {w}, высота {h}")



epsilon = 0.01*cv2.arcLength(largest_contour,True)
approx = cv2.approxPolyDP(largest_contour,epsilon,True)
rect = cv2.minAreaRect(largest_contour)
box = cv2.boxPoints(rect)
box = np.intp(box)

# print(approx)

# cv2.namedWindow('minimum_points_contour', cv2.WINDOW_NORMAL)
# cv2.drawContours(contour_image_test,[approx],-1,(0,0,255),2)
# cv2.imshow('minimum_points_contour', contour_image_test)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
cv2.drawContours(contour_image_test,[box],-1,(0,0,255),2)
cv2.namedWindow('bounding_box', cv2.WINDOW_NORMAL)
cv2.imshow('bounding_box', contour_image_test)
cv2.waitKey(0)
cv2.destroyAllWindows()




# print(len(new_contours))

# print("box",x,y,w,h)

# Масштабирование:
N = 400
M = 310
# Выбираем, что больше - высота или ширина прямоугольника и масштабируем под нее
k = N / w
# box_shifted = approx -approx[0][0][:] + [5,5]  # И небольшой сдвиг, чтобы не выходить в отрицательную область. 
# box_scaled = np.intc(approx_shifted * k)       # Это и строчку выше проделать для всех точек

step_coeff = 50 
not_contours = []
for c in new_contours:
        contour_size = len(c)
        for i in range(contour_size-1):
                x0,y0 = c[i,0,1], c[i,0,0]
                x1,y1 = c[i+1,0,1], c[i+1,0,0]
                # print(x0,x1)
                if x0 != x1:
                        a = (y1-y0)/(x1-x0)
                        b = y0-a*x0
                        for x_t in range(x0*step_coeff,(x1)*step_coeff+1):
                                y_t = a*x_t/step_coeff+b
                                not_contours.append([ np.int32(k*(x_t/step_coeff - x)), np.int32(k*(y_t - y))])
                else:
                        a = (x1-x0)/(y1-y0)
                        b = x0-a*y0
                        for y_t in range(y0*step_coeff,(y1*step_coeff)+1):
                                x_t = a*y_t/step_coeff+b
                                not_contours.append([ np.int32(k*(x_t - x)), np.int32(k*(y_t/step_coeff - y))])             


 
new_contours_shifted = [c - [x,y] for c in new_contours]
new_contours_scaled = [np.intc(c * k) for c in new_contours_shifted]

##### КОНЕЦ
# cv2.drawContours(contour_image_test,new_contours_scaled,-1,(0,0,255),2)
cv2.drawContours(contour_image_test,new_contours_scaled,-1,(0,0,255),2)
cv2.imshow('Contours', contour_image_test)
cv2.waitKey(0)
cv2.destroyAllWindows()
######### A*

size_x = 400
size_y = 310
bitmap  = [[0 for _ in range(size_x)] for _ in range(size_y)]
for c in not_contours:
        if 0 <= c[0] < 310 and 0 <= c[1] < 399:
                bitmap[310-c[0]][c[1]] = 1
        else:
             print(c)
             break
        # print(c[0,0,:])



# for i in range(10):
#     for j in range(10):
#         bitmap[i+15][j+15] = 1
# for i in range(10):
#     for j in range(10):
#         bitmap[i+20][j+40] = 1




a = astar()
a.resize(size_x ,size_y )
a.set(bitmap, 1)
start_x = 5
start_y = 15
end_x = 268
end_y = 221
X_border = []
Y_border = []
a.compute(start_x, start_y, end_x, end_y) 
for i in range(size_y):
    for j in range(size_x):
        if a.map[i][j] == 0xFFFFFFFE:
            X_border.append(j)
            Y_border.append(i)
X = a.px
Y = a.py
coord = list(zip(X,Y))
# print(coord)
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

for i in range(1,L-1):
    if coord[i-1][0] == coord[i][0]:
        if axes_path == "Y":
            X_path.append(coord[i-1][0])
            Y_path.append(coord[i-1][1])
            axes_path = "X"
    if coord[i-1][1] == coord[i][1]:
        if axes_path == "X":
            X_path.append(coord[i-1][0])
            Y_path.append(coord[i-1][1])
            axes_path = "Y" 
X_path.append(coord[L-1][0])
Y_path.append(coord[L-1][1])           
# print(list(zip(X_path,Y_path)))


# X_path, Y_path = list(zip(*new_coord))

fig, ax = plt.subplots()
ax.set_xlim([0, size_x])
ax.set_ylim([0, size_y])
image = cv2.resize(image, (400, 310)) 
image = cv2.flip(image, 0) 

ax.plot(start_x, start_y, "r*")
ax.plot(end_x, end_y, "r*")
ax.plot(X,Y)
ax.plot(X_path,Y_path,'.r')
ax.plot(X_border,Y_border,"k.")
ax.imshow(image)
ax.grid()
plt.show()




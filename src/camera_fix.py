import cv2 as cv
import numpy as np

def fisheye_fix(frame):

    # Определение матрицы камеры и коэффициентов искажений
    camera_matrix = np.array([[1200, 0, 960],
                              [0, 1200, 540],
                              [0, 0, 1]], dtype=np.float64)

    dist_coeffs = np.array([-0.1, 0.05, 0.001, 0.0], dtype=np.float64)

    height, width = frame.shape[:2]
    new_camera_matrix = cv.fisheye.estimateNewCameraMatrixForUndistortRectify(
        camera_matrix, dist_coeffs, (width, height), np.eye(3), balance=1)
    corrected_frame = cv.fisheye.undistortImage(frame, camera_matrix, dist_coeffs, None, new_camera_matrix)

    # Если необходимо, можно дополнительно обрезать изображение вручную или масштабировать его
    corrected_frame = cv.resize(corrected_frame, (width, height))
    return corrected_frame



def find_homography(frame, scale_map=2):
    # (X1, Y1), (X2, Y2), (X3, Y3), (X4, Y4) = map_config.border_corners

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray = cv.medianBlur(gray, 5)
    _, thresh = cv.threshold(gray, 127, 255, cv.THRESH_BINARY_INV)
    contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    rect = max(contours, key=cv.contourArea)
    cv.drawContours(frame, [rect], -1, 255, 5)
    hull = cv.convexHull(rect)
    epsilon = 0.02 * cv.arcLength(hull, True)
    approx = cv.approxPolyDP(hull, epsilon, True)
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = sorted([x[0] for x in approx], key=lambda c: c[1])
    #print('fdfdf', approx[0])
    get_corners(approx)
    # (x,y,w,h) = cv.boundingRect(approx)

    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = get_corners(approx)
    (X1, Y1), (X2, Y2), (X3, Y3), (X4, Y4) = [(0, 0), (400, 0), (0, 310), (400, 310)]
    X1, Y1, X2, Y2, X3, Y3, X4, Y4 = [i * scale_map for i in [X1, Y1, X2, Y2, X3, Y3, X4, Y4]]
    # Опорные точки на изображении и соответствующие точки на карте
    image_points = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]], dtype="float32")
    map_points = np.array([[X1, Y1], [X2, Y2], [X3, Y3], [X4, Y4]], dtype="float32")

    # Вычисляем матрицу гомографии для проецирования изображения на карту
    H, status = cv.findHomography(image_points, map_points)
    angle_coordinates = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
    return H
    # Применяем матрицу гомографии, чтобы преобразовать откалиброванное изображение
    # aligned_frame = cv.warpPerspective(frame, H, (map_width, map_height))
    #
    # return aligned_frame


def get_corners(cnt):
    corners = sorted([x[0] for x in cnt], key=lambda c: c[1])
    up = corners[:2]
    down = corners[2:]
    left_up,right_up = sorted(up, key=lambda c: c[0])
    left_down,right_down = sorted(down, key=lambda c: c[0])
    return [left_up, right_up, left_down, right_down]


def warp_frame(frame, H = 0, scale_map=2):
    w, h = (400, 310)
    map_width, map_height = [i * scale_map for i in [w, h]]
    #H = H or find_homography(frame, scale_map)
    if (type(H) == int):
        H = find_homography(frame, scale_map)
    #return frame
    aligned_frame = cv.warpPerspective(frame, H, (map_width, map_height))
    cv.imshow('test', aligned_frame)
    cv.waitKey(0)
    return aligned_frame, H



import cv2 as cv
import time
import threading
from queue import Queue
import camera_fix as ff

# Максимальное количество кадров в очереди
MAX_QUEUE_SIZE = 10
VIDEO_CAM = "rtsp://Admin:rtf123@192.168.2.250/251:554/1/1"
TEST_VIDEO = "output_video4.avi"

def capture_frames(video_source="rtsp://Admin:rtf123@192.168.2.250/251:554/1/1", frame_queue=None):
    """
    Функция захвата кадров с камеры каждые 2 секунды.
    """
    cap = cv.VideoCapture(video_source)

    if not cap.isOpened():
        print("Ошибка: не удалось открыть видеопоток.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Ошибка: не удалось захватить кадр.")
            break

        # Добавление нового кадра
        if frame_queue.qsize() >= MAX_QUEUE_SIZE:
            frame_queue.get()  # Удаляем последний кадр (самый старый)

        frame_queue.put(frame)
        time.sleep(2)  # Захватываем кадры каждые 2 секунды

    cap.release()

def initial_processing(frame):
    fixed_fisheye_frame = ff.fisheye_fix(frame)
    processed_frame, H = ff.warp_frame(fixed_fisheye_frame)
    return H


def process_frames(frame_queue):
    first_frame_processed = False
    processing_params = None
    # while True:
    #     if not frame_queue.empty():
    #         frame = frame_queue.get()
    #
    #         # Обработка кадра
    #         handle_frame(frame)
    while True:
        if not frame_queue.empty():
            frame = frame_queue.get()

            if not first_frame_processed:
                # Обрабатывать первый кадр иначе
                processing_params = initial_processing(frame)
                first_frame_processed = True
                print(f"Параметры для обработки: {processing_params}")
            else:
                # Дальнейшая обработка остальных кадров с использованием параметров
                handle_frame(frame, processing_params)


def handle_frame(frame, H):
    fixed_fisheye_frame = ff.fisheye_fix(frame)
    # Если warp_frame возвращает изображение, используем его
    processed_frame, angles_coordinates = ff.warp_frame(fixed_fisheye_frame, H)

    if processed_frame is not None:
        cv.imshow('Обработанный Кадр', processed_frame)
        cv.waitKey(2000)  # Показываем кадр в течение 2 секунд

    # Закрываем окно, если кадр был обработан
    if cv.waitKey(1) & 0xFF == ord('q'):
        cv.destroyAllWindows()
    return processed_frame



# coding:utf8

import cv2
import time
import threading
import pyzbar.pyzbar as pyzbar

from xr_motor import RobotDirection
go = RobotDirection()

import xr_config as cfg

def decodeDisplay(image):
    barcodes = pyzbar.decode(image)
    if barcodes ==[]:
        cfg.barcodeData = None
        cfg.barcodeType = None
    else:
        for barcode in barcodes:
            # 提取条形码的边界框的位置
            # 画出图像中条形码的边界框
            (x, y, w, h) = barcode.rect
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # 条形码数据为字节对象，所以如果我们想在输出图像上
            # 画出来，就需要先将它转换成字符串
            cfg.barcodeData = barcode.data.decode("utf-8")
            cfg.barcodeType = barcode.type

            # 绘出图像上条形码的数据和条形码类型
            text = "{} ({})".format(cfg.barcodeData, cfg.barcodeType)
            cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        .5, (0, 0, 125), 2)

            # 向终端打印条形码数据和条形码类型
            print("[INFO] Found {} barcode: {}".format(cfg.barcodeType, cfg.barcodeData))
    return image

def car():
    cfg.LEFT_SPEED = 40
    cfg.RIGHT_SPEED = 40
    while True:
        if cfg.barcodeData == 'start':
            STATUS = 1
        elif cfg.barcodeData == 'stop':
            STATUS = 0
        if STATUS:
            if cfg.barcodeData == 'forward':
                go.forward()
                time.sleep(0.5)
            elif cfg.barcodeData == 'back':
                go.left()
                time.sleep(1.5)
            elif cfg.barcodeData == 'left':
                go.left()
                time.sleep(0.5)
            elif cfg.barcodeData == 'right':
                go.right()
                time.sleep(0.5)
            else:
                go.forward()
        else:
            go.stop()
    go.stop()


def detect():
    camera = cv2.VideoCapture(0)

    while True:
        # 读取当前帧
        ret, frame = camera.read()
        # 转为灰度图像
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img = decodeDisplay(gray)
        #car()
        #cv2.waitKey(5)
        cv2.imshow("qrcode", img)

        if cv2.waitKey(1)&0XFF == ord('q'):#检测到按键q退出
            go.stop()
            break
    go.stop()
    camera.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    t1 = threading.Thread(target=car,args=())
    t1.setDaemon(True)
    t1.start()
    detect()

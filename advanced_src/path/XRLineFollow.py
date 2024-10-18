#! /usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Author: Ceoifung
Date: 2022-08-23 11:40:49
LastEditTime: 2022-09-27 15:30:11
LastEditors: Ceoifung
Description: 摄像头巡线工具类
XiaoRGEEK All Rights Reserved, Powered by Ceoifung
'''
import cv2
import numpy as np
import time
import threading
from xr_motor import RobotDirection
go = RobotDirection()

class XRLineFollow():
    def __init__(self):
        self.orgFrame = None
        self.cvOk = False
        self.angleFactor = 0.125
        self.lineOut = False
        self.weight = [0, 0.5, 0.5]
        self.weightSum = 0
        for w in range(len(self.weight)):
            self.weightSum += self.weight[w]
        self.deflectionAngle = 0
        self.lastTurn = None
        self.isRunning = False
        # 要识别的颜色字典
        self.colorDist = {'Lower': np.array([0, 0, 0]), 'Upper': np.array([180, 255, 95])}
        # self.colorDist = {'red': {'Lower': np.array([0, 50, 50]), 'Upper': np.array([6, 255, 255])},
        #             'blue': {'Lower': np.array([100, 80, 46]), 'Upper': np.array([124, 255, 255])},
        #             'cyan': {'Lower': np.array([35, 43, 46]), 'Upper': np.array([77, 255, 255])},
        #             'black': {'Lower': np.array([0, 0, 0]), 'Upper': np.array([180, 255, 95])},
        #             }

    def getX(self, img):
        """获取图像的中心坐标X值

        Args:
            img ([type]): 图像

        Returns:
            [type]: X坐标
        """
        x = 0
        # 高斯模糊
        gsFrame = cv2.GaussianBlur(img, (5, 5), 0)
        # 转换颜色空间
        hsv = cv2.cvtColor(gsFrame, cv2.COLOR_BGR2HSV)
        # 查找颜色
        mask = cv2.inRange(hsv, self.colorDist['Lower'], self.colorDist['Upper'])
        # 腐蚀
        mask = cv2.erode(mask, None, iterations=2)
        # 膨胀
        mask = cv2.dilate(mask, None, iterations=2)
        # 查找轮廓
        # cv2.imshow('mask', mask)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(cnts):
            c = max(cnts, key=cv2.contourArea)  # 找出最大的区域
            area = cv2.contourArea(c)
            # 获取最小外接矩形
            rect = cv2.minAreaRect(c)
            if area >= 500:
                xy = rect[0]
                xy = int(xy[0]), int(xy[1])
                cv2.circle(img, (xy[0], xy[1]), 3, (0, 255, 0), -1)
                x = xy[0]
                # box = cv2.cv.BoxPoints(rect)
                box = cv2.boxPoints(rect)
                # 数据类型转换
                box = np.int0(box)
                # 绘制轮廓
                cv2.drawContours(img, [box], 0, (0, 255, 255), 1)
        return x

    def setRunning(self, running):
        """设置是否开始检测线条

        Args:
            running ([type]): 是否开始巡线
        """
        self.isRunning = running

    def line(self):
        while True:
            if self.isRunning:
                if self.cvOk:
                    if -20 <= self.deflectionAngle <=20:
                        print("ST")
                        go.forward()
                    else:
                        if (self.deflectionAngle/15)<0:
                            print("turn left")
                            go.left()
                        else:
                            print("turn right")
                            go.right()
                        # 休眠0.15s，保证向左或向右的范围不要过大
                        time.sleep(0.15)
                    self.cvOk = False
                else:
                    if self.lineOut:
                        if self.lastTurn == "R":
                            print("last turn right")
                            go.right()
                            time.sleep(0.05)
                        elif self.lastTurn == "L":
                            print("last turn left")
                            go.left()
                            time.sleep(0.05)
                        self.lineOut = False
                    else:
                        time.sleep(0.05)
            else:
                print("waitting run")
                time.sleep(0.05)

    def backgroundTask(self, orgFrame, colorDist={'Lower': np.array([0, 0, 0]), 'Upper': np.array([180, 255, 95])}):
        """后台处理巡线任务

        Args:
            orgFrame ([type]): 原始图像
            colorDist ([type]): 要识别的颜色字典，默认是黑色

        Returns:
            [type]: 处理过后的图像
        """
        self.colorDist = colorDist
        lineCenter = 0.0
        f = orgFrame
        h, w = f.shape[:2]
        # 获取黑线的顶部，底部以及中部区间
        upFrame = f[0:65, 0:480]
        centerFrame = f[145:210, 0:480]
        downFrame = f[290:355, 0:480]

        upX = self.getX(upFrame)
        centerX = self.getX(centerFrame)
        downX = self.getX(downFrame)
        
        if downX != 0:
            lineCenter = downX
            if lineCenter >= 360:
                self.lastTurn = "R"
            elif lineCenter <= 120:
                self.lastTurn = 'L'
            self.deflectionAngle = (lineCenter - w/2)*self.angleFactor
            self.cvOk = True
        elif centerX != 0:
            lineCenter = centerX
            if lineCenter >= 360:
                self.lastTurn = "R"
            elif lineCenter <= 120:
                self.lastTurn = 'L'
            self.deflectionAngle = (lineCenter - w/2)*self.angleFactor
            self.cvOk = True
        elif upX != 0 and downX != 0:
            lineCenter = (upX + downX) /2
            self.deflectionAngle = (lineCenter - w/2)*self.angleFactor
            self.cvOk = True
        elif upX != 0:
            lineCenter = upX
            if lineCenter >= 360:
                self.lastTurn = "R"
            elif lineCenter <= 120:
                self.lastTurn = 'L'
            self.deflectionAngle = (lineCenter - w/2)*self.angleFactor
            self.cvOk = True
        elif upX == 0 and downX == 0 and centerX == 0:
            self.lineOut = True
        # 画屏幕中心十字
        cv2.line(f, (220, 180), (260, 180), (255, 255, 0), 1)
        cv2.line(f, (240, 160), (240, 200), (255, 255, 0), 1)
        # cv2.waitKey(1)
        return f

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    lineFollow = XRLineFollow()
    th2 = threading.Thread(target=lineFollow.line)
    th2.setDaemon(True)     # 设置为后台线程，这里默认是False，设置为True之后则主线程不用等待子线程
    th2.start()
    # color = {'Lower': np.array([26, 43, 46]), 'Upper': np.array([34, 255, 255])}
    while True:
        success, img = cap.read()
        if success:
            lineFollow.setRunning(True)
            img = lineFollow.backgroundTask(img)
            time.sleep(0.01)
            #cv2.imshow("Image", img)
            #cv2.waitKey(1)
        else:
            break
    lineFollow.setRunning(False)
    th2.join()
    cap.release()
    # cv2.destoryAllWindows()

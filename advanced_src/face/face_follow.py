#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    * @par Copyright (C): 2010-2020 Shenzhen XiaoRGEEK Tech
    * @file         face_tracking
    * @version      V1.0
    * @details
    * @par History
    
    @author: Ylstart
"""


from __future__ import division
import cv2

import math                                     #提供了许多对浮点数的数学运算函数
from xr_servo import Servo                      #引入舵机类
servo = Servo()                                 #实例化舵机

from xr_pid import PID
X_pid = PID(0.03, 0.09, 0.0005)                 #实例化一个X轴坐标的PID算法PID参数：第一个代表pid的P值，二代表I值,三代表D值
X_pid.setSampleTime(0.005)                      #设置PID算法的周期
X_pid.setPoint(160)                             #设置PID算法的预值点，即目标值，这里160指的是屏幕框的x轴中心点，x轴的像素是320，一半是160

Y_pid = PID(0.035, 0.08, 0.002)             #实例化一个X轴坐标的PID算法PID参数：第一个代表pid的P值，二代表I值,三代表D值
Y_pid.setSampleTime(0.005)                      #设置PID算法的周期
Y_pid.setPoint(160)                             #设置PID算法的预值点，即目标值，这里160指的是屏幕框的y轴中心点，y轴的像素是320，一半是160

x_middle = 0                                    #人脸框中心x轴的坐标
y_middle = 0                                    #人脸框中心y轴的坐标

angle_X = 80                                    #x轴舵机初始角度
angle_Y = 20                                    #y轴舵机初始角度

servo_X = 7                                     #设置x轴舵机号
servo_Y = 8                                     #设置y轴舵机号

cap = cv2.VideoCapture(0)                       #使用opencv获取摄像头
cap.set(3, 320)                                 #设置图像的宽为320像素
cap.set(4, 320)                                 #设置图像的高为320像素

#face.xml的位置要和本程序位于同一文件夹下
face_cascade = cv2.CascadeClassifier( 'face.xml' )

#死循环
while True:
    ret,frame = cap.read()      #获取摄像头视频流
    if ret == 1:                #判断摄像头是否工作
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)   #要先将每一帧先转换成灰度图，在灰度图中进行查找
        faces = face_cascade.detectMultiScale(gray)     #查找人脸
        if len(faces)>0:        #当视频中有人脸轮廓时
            #print('face found!')
            for (x,y,w,h) in faces:
                #参数分别是“目标帧”，“矩形”，“矩形大小”，“线条颜色”，“宽度”
                cv2.rectangle(frame,(x,y),(x+h,y+w),(0,255,0),2)
                result = (x,y,w,h)
                x_middle = result[0] + w/2      #x轴中心
                y_middle = result[1] + h / 2    #y轴中心

                X_pid.update(x_middle)      #将X轴数据放入pid中计算输出值
                Y_pid.update(y_middle)      #将Y轴数据放入pid中计算输出值
                #print("X_pid.output==%d"%X_pid.output)     #打印X输出
                #print("Y_pid.output==%d"%Y_pid.output)     #打印Y输出
                angle_X = math.ceil(angle_X + 1 * X_pid.output)     #更新X轴的舵机角度，用上一次的舵机角度加上一定比例的增量值取整更新舵机角度
                angle_Y = math.ceil(angle_Y + 0.8 * Y_pid.output)   #更新Y轴的舵机角度，用上一次的舵机角度加上一定比例的增量值取整更新舵机角度
                #print("angle_X-----%d" % angle_X)  #打印X轴舵机角度
                #print("angle_Y-----%d" % angle_Y)  #打印Y轴舵机角度
                if angle_X > 180:       #限制X轴最大角度
                    angle_X = 180
                if angle_X < 0:         #限制X轴最小角度
                    angle_X = 0
                if angle_Y > 180:       #限制Y轴最大角度
                    angle_Y = 180
                if angle_Y < 0:         #限制Y轴最小角度
                    angle_Y = 0
                servo.set(servo_X, angle_X)         #设置X轴舵机
                servo.set(servo_Y, angle_Y)     #设置Y轴舵机

        cv2.imshow("capture", frame)    # 显示图像
        if cv2.waitKey(1) == ord('q'):  # 当按键按下q键时退出
            break
cap.release()
cv2.destroyAllWindows()
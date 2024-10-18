# coding=utf-8
import cv2
import numpy as np #导入库
COLOR_LOWER = [
    # 红色
    np.array([0,43,46]),
    # 绿色
    np.array([35,43,46]),
    # 蓝色
    np.array([100,43,46]),
    # 紫色
    np.array([125,43,46]),
    # 橙色
    np.array([11,43,46])
]
# 颜色区间高阀值
COLOR_UPPER = [
    # 红色
    np.array([10, 255, 255]),
    # 绿色
    np.array([77, 255, 255]),
    # 蓝色
    np.array([124, 255, 255]),
    # 紫色
    np.array([155, 255, 255]),
    # 橙色
    np.array([25, 255, 255])
]

COLOR = 0

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

x = 0                                   #人脸框中心x轴的坐标
y = 0                                   #人脸框中心y轴的坐标

angle_X = 80                                    #x轴舵机初始角度
angle_Y = 20                                    #y轴舵机初始角度

servo_X = 7                                     #设置x轴舵机号
servo_Y = 8                                     #设置y轴舵机号

cap = cv2.VideoCapture(0)                       #使用opencv获取摄像头
cap.set(3, 320)                                 #设置图像的宽为320像素
cap.set(4, 320)                                 #设置图像的高为320像素

while 1: #进入无线循环
    ret,frame = cap.read() #将摄像头拍摄到的画面作为frame的值
    if ret == 1:  # 判断摄像头是否工作
        frame = cv2.GaussianBlur(frame,(5,5),0) #高斯滤波GaussianBlur() 让图片模糊
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) #将图片的色域转换为HSV的样式 以便检测
        mask = cv2.inRange(hsv,COLOR_LOWER[COLOR],COLOR_UPPER[COLOR])  #设置阈值，去除背景 保留所设置的颜色

        mask = cv2.erode(mask,None,iterations=2) #显示腐蚀后的图像
        mask = cv2.GaussianBlur(mask,(3,3),0) #高斯模糊
        res = cv2.bitwise_and(frame,frame,mask=mask) #图像合并

        cnts = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2] #边缘检测

        if len(cnts) >0 : #通过边缘检测来确定所识别物体的位置信息得到相对坐标
            cnt = max(cnts,key=cv2.contourArea)
            (x,y),radius = cv2.minEnclosingCircle(cnt)
            cv2.circle(frame,(int(x),int(y)),int(radius),(255,0,255),2) #画出一个圆
            print(int(x),int(y))
            X_pid.update(x)  # 将X轴数据放入pid中计算输出值
            Y_pid.update(y)  # 将Y轴数据放入pid中计算输出值
            # print("X_pid.output==%d"%X_pid.output)        #打印X输出
            # print("Y_pid.output==%d"%Y_pid.output)        #打印Y输出
            angle_X = math.ceil(angle_X + 1 * X_pid.output)  # 更新X轴的舵机角度，用上一次的舵机角度加上一定比例的增量值取整更新舵机角度
            angle_Y = math.ceil(angle_Y + 0.8 * Y_pid.output)  # 更新Y轴的舵机角度，用上一次的舵机角度加上一定比例的增量值取整更新舵机角度
            # print("angle_X-----%d" % angle_X) #打印X轴舵机角度
            # print("angle_Y-----%d" % angle_Y) #打印Y轴舵机角度
            if angle_X > 180:  # 限制X轴最大角度
                angle_X = 180
            if angle_X < 0:  # 限制X轴最小角度
                angle_X = 0
            if angle_Y > 180:  # 限制Y轴最大角度
                angle_Y = 180
            if angle_Y < 0:  # 限制Y轴最小角度
                angle_Y = 0
            servo.set(servo_X, angle_X)  # 设置X轴舵机
            servo.set(servo_Y, angle_Y)  # 设置Y轴舵机
        else:
            pass
        cv2.imshow('frame',frame) #将具体的测试效果显示出来
        #cv2.imshow('mask',mask)
        #cv2.imshow('res',res)
        if cv2.waitKey(1) == ord('q'):  # 当按键按下q键时退出
            break

cap.release()
cv2.destroyAllWindows() #后面两句是常规操作,每次使用摄像头都需要这样设置一波
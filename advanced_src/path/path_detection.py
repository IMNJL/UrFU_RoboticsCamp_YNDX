#coding:utf-8
#Python中声明文件编码的注释，编码格式指定为utf-8
from socket import *
from time import ctime
import binascii
import RPi.GPIO as GPIO
import time
import threading
import cv2
import os

from xr_motor import RobotDirection
go = RobotDirection()



Path_Dect_px_top = 320
Path_Dect_px_bottom = 320
Path_Dect_px_sum  = 0	#坐标值求和



def PathDect(func):
	#global Path_Dect_px	#巡线中心点坐标值
	while True:
		#print 'Path_Dect_px %d '%Path_Dect_px	 #打印巡线中心点坐标值
		dx = Path_Dect_px_top - Path_Dect_px_bottom
		mid = int(Path_Dect_px_top + Path_Dect_px_bottom)/2

		print("dx==%d"%dx)
		print("mid==%s"%mid)

		if (mid < 260)&(mid > 0):	#如果巡线中心点偏左，就需要左转来校正。
			print("turn left")
			go.left()
		elif mid > 420:#如果巡线中心点偏右，就需要右转来校正。
			print("turn right")
			go.right()
		else :		#如果巡线中心点居中，就可以直行。
			if dx > 30:
				print("turn left")
				go.left()
			elif dx < -45:
				print("turn right")
				go.right()
			else:
				print("go stright")
				go.forward()
		time.sleep(0.007)
		go.stop()
		time.sleep(0.007)
cap = cv2.VideoCapture(0)	#实例化摄像头

t1 = threading.Thread(target=PathDect,args=(u'监听',))
t1.setDaemon(True)
t1.start()


#os.system('sudo python3 main.py')

while True:
	ret,frame = cap.read()	#capture frame_by_frame
	if ret:
		gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)	#获取灰度图像
		ret,thresh1=cv2.threshold(gray,120,255,cv2.THRESH_BINARY)#对灰度图像进行二值化
		Path_Dect_fre_count = 1
		for j in range(0,640,5):		#采样像素点，5为步进，一共128个点
			if thresh1[300,j] == 0:
				Path_Dect_px_sum = Path_Dect_px_sum + j		#黑色像素点坐标值求和
				Path_Dect_fre_count = Path_Dect_fre_count + 1	#黑色像素点个数求和
		Path_Dect_px_top = (Path_Dect_px_sum )/(Path_Dect_fre_count)	#黑色像素中心点为坐标和除以个数
		Path_Dect_px_sum = 0

		Path_Dect_fre_count = 1
		for j in range(0, 640, 5):  # 采样像素点，5为步进，一共128个点
			if thresh1[160, j] == 0:
				Path_Dect_px_sum = Path_Dect_px_sum + j  # 黑色像素点坐标值求和
				Path_Dect_fre_count = Path_Dect_fre_count + 1  # 黑色像素点个数求和
		Path_Dect_px_bottom = (Path_Dect_px_sum) / (Path_Dect_fre_count)  # 黑色像素中心点为坐标和除以个数
		Path_Dect_px_sum = 0

		cv2.imshow('BINARY',thresh1)		#树莓派桌面显示二值化图像，比较占资源默认注释掉调试时可以打开
		if cv2.waitKey(1)&0XFF ==ord('q'):#检测到按键q退出
			go.stop()
			break	
cap.release()
cv2.destroyAllWindows()
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
import time  


cap = cv2.VideoCapture(0)
cap.set(3, 320)
cap.set(4, 320)
#face.xml的位置要和本程序位于同一文件夹下
face_cascade = cv2.CascadeClassifier( 'face.xml' ) 
#死循环，同学们可以积累一下，这里的死循环的写法还有哪些其他的
while True:
	ret,frame = cap.read()
	if ret == True:
		gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		#要先将每一帧先转换成灰度图，在灰度图中进行查找
		faces = face_cascade.detectMultiScale(gray)
		max_face = 0
		value_x = 0
		if len(faces)>0:
			#print('face found!')
			for (x,y,w,h) in faces:
				#参数分别是“目标帧”，“矩形”，“矩形大小”，“线条颜色”，“宽度”
				cv2.rectangle(frame,(x,y),(x+h,y+w),(0,255,0),2)
				#max_face=w*h
				result = (x,y,w,h)
				x = result[0]
				y = result[1]

		cv2.imshow("capture", frame)
		if cv2.waitKey(1)==ord('q'):	# 当按键按下q键时退出
			break

cap.release()
cv2.destroyAllWindows()

import cv2
import numpy as np #导入库
blue_lower = np.array([100,43,46])
blue_upper = np.array([124,255,255]) #设置颜色区间
cap = cv2.VideoCapture(0)						#使用opencv获取摄像头
cap.set(3, 320)									#设置图像的宽为320像素
cap.set(4, 320)									#设置图像的高为320像素
while 1: #进入无线循环
	ret,frame = cap.read() #将摄像头拍摄到的画面作为frame的值
	if ret == 1:  # 判断摄像头是否工作
		frame = cv2.GaussianBlur(frame,(5,5),0) #高斯滤波GaussianBlur() 让图片模糊
		hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) #将图片的色域转换为HSV的样式 以便检测
		mask = cv2.inRange(hsv,blue_lower,blue_upper)  #设置阈值，去除背景 保留所设置的颜色

		mask = cv2.erode(mask,None,iterations=2) #显示腐蚀后的图像
		mask = cv2.GaussianBlur(mask,(3,3),0) #高斯模糊
		res = cv2.bitwise_and(frame,frame,mask=mask) #图像合并

		cnts = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2] #边缘检测

		if len(cnts) >0 : #通过边缘检测来确定所识别物体的位置信息得到相对坐标
			cnt = max(cnts,key=cv2.contourArea)
			(x,y),radius = cv2.minEnclosingCircle(cnt)
			cv2.circle(frame,(int(x),int(y)),int(radius),(255,0,255),2) #画出一个圆
			print(int(x),int(y))
		else:
			pass
		cv2.imshow('frame',frame) #将具体的测试效果显示出来
		cv2.imshow('mask',mask)
		cv2.imshow('res',res)
		if cv2.waitKey(1) == ord('q'):  # 当按键按下q键时退出
			break

cap.release()
cv2.destroyAllWindows() #后面两句是常规操作,每次使用摄像头都需要这样设置一波
# coding:utf-8
from builtins import hex, eval, int, object

"""
@version: python3.7
@Author  : xiaor
@Explain :控制舵机
@contact :
@Time    :2020/05/09
@File    :XiaoR_servo.py
@Software: PyCharm
"""

from xr_i2c import I2c

i2c = I2c()

import time


class Servo(object):
	'''
	舵机控制类
	'''
	def __init__(self):
		pass

	def angle_limit(self, angle):
		'''
		对舵机角度限幅，防止舵机堵转烧毁
		'''
		if angle > 160:  # 限制最大角度值
			angle = 160
		elif angle < 10:  # 限制最小角度值
			angle = 10
		return angle

	def set(self, servonum, servoangle):
		'''
		设置舵机角度
		:param servonum:舵机号
		:param servoangle:舵机角度
		:return:
		'''
		angle = self.angle_limit(servoangle)
		buf = [0xff, 0x01, servonum, angle, 0xff]
		try:
			i2c.writedata(i2c.mcu_address, buf)
		except Exception as e:
			print('servo write error:', e)

	def store(self):
		'''
		存储舵机角度
		:return:
		'''
		buf = [0xff, 0x33, 0x00, 0x00, 0xff]
		i2c.writedata(i2c.mcu_address, buf)

	def restore(self):
		'''
		恢复舵机角度
		:return:
		'''
		buf = [0xff, 0x32, 0x00, 0x00, 0xff]
		i2c.writedata(i2c.mcu_address, buf)

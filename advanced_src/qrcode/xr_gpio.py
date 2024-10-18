# coding:utf-8
'''
树莓派WiFi无线视频小车机器人驱动源码
作者：liuviking
版权所有：小R科技（深圳市小二极客科技有限公司www.xiao-r.com）；WIFI机器人网论坛 www.wifi-robots.com
本代码可以自由修改，但禁止用作商业盈利目的！
本代码已申请软件著作权保护，如有侵权一经发现立即起诉！
'''
'''
文 件 名：_XiaoRGEEK_GPIO_.py
功    能：引脚定义及初始化文件,提供IO口操作函数以及调速函数。需要设置引脚为输入/输出模式。输出参考LED0设置，输入参考IR_R设置
外部条用：
import _XiaoRGEEK_GPIO_ as XR
XR.GPIOSet(XR.LED0)		#LED0引脚输出高电平
XR.GPIOClr(XR.LED0)		#LED0引脚输出低电平
XR.DigitalRead(IR_R)	#读取IR_R引脚状态
XR.ENAset(100)			#设置ENA占空比来调速，0-100之间
XR.ENBset(100)			#设置ENB占空比来调速，0-100之间
'''
import RPi.GPIO as GPIO
import time

#######################################
#############信号引脚定义##############
#######################################
########LED口定义#################
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

########电机驱动接口定义#################
ENA = 13  # //L298使能A
ENB = 20  # //L298使能B
IN1 = 16  # //电机接口1
IN2 = 19  # //电机接口2
IN3 = 26  # //电机接口3
IN4 = 21  # //电机接口4

#########电机初始化为LOW##########
GPIO.setup(ENA, GPIO.OUT, initial=GPIO.LOW)
ENA_pwm = GPIO.PWM(ENA, 1000)
ENA_pwm.start(0)
ENA_pwm.ChangeDutyCycle(100)
GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ENB, GPIO.OUT, initial=GPIO.LOW)
ENB_pwm = GPIO.PWM(ENB, 1000)
ENB_pwm.start(0)
ENB_pwm.ChangeDutyCycle(100)
GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)

'''
设置gpio端口为电平
参数：gpio为设置的端口，status为状态值只能为True(高电平)，False(低电平)
'''


def digital_write(gpio, status):
	GPIO.output(gpio, status)


'''
读取gpio端口的电平
'''


def digital_read(gpio):
	return GPIO.input(gpio)


'''
设置电机调速端口ena的pwm
'''


def ena_pwm(pwm):
	ENA_pwm.ChangeDutyCycle(pwm)


'''
设置电机调速端口enb的pwm
'''


def enb_pwm(pwm):
	ENB_pwm.ChangeDutyCycle(pwm)

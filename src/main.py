import cv2
import numpy as np
import socket
import time
import robot as rb
import field as fld
from astar import astar

host = "192.168.2.89"
port = 2001

robot = rb.RobotControl(host="192.168.2.89", port=2001)


a = astar()
image = cv2.imread('maze.png')
not_contours = a.contours(image)

matr = a.get_matrix(not_contours)
coord, X, Y, X_border, Y_border = a.get_trajectory(matr, 5, 15, 380, 300)
a.draw_trajectory(coord, image, 5, 15, 380, 300, X, Y, X_border, Y_border)

# command_bytes = robot.set_robohand_position(90, 40, 90, 20)
# robot.send_to_robot(command_bytes)
# command_bytes = robot.set_robohand_position(70, 50, 90, 20)
# robot.send_to_robot(command_bytes)
# command_bytes = robot.set_robohand_position(50, 70, 90, 20)
# robot.send_to_robot(command_bytes)
# command_bytes = robot.set_robohand_position(50, 50, 90, 130)
# robot.send_to_robot(command_bytes)


# command_bytes = robot.set_robohand_position(95, 40, 90, 140)
# robot.send_to_robot(command_bytes)
# command_bytes = robot.set_defolt_robohand
# robot.send_to_robot(command_bytes)
# command_bytes = robot.set_robohand_position(70, 70, 90, 20)
# robot.send_to_robot(command_bytes)
# command_bytes = robot.set_robohand_position(70, 40, 90, 20)
# robot.send_to_robot(command_bytes)
# command_bytes = robot.set_robohand_position(70, 40, 90, 140)
# robot.send_to_robot(command_bytes)

# command_bytes = robot.set_defolt_robohand()
# robot.send_to_robot(command_bytes)

command_bytes = robot.set_robohand_position(100, 85, 90, 40)
robot.send_to_robot(command_bytes, 0)
command_bytes = robot.set_robohand_position(120, 85, 90, 40)
robot.send_to_robot(command_bytes, 0)
while True:

    print(robot.receive_from_robot())
    time.sleep(1)


# fld.field = fld.create_field_with_case(0, 1000)
# fld.field.draw()
# fld.field.plot()





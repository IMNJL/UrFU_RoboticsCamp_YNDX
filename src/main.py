import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
from A_Star import astar
import robot as rb
from manipulator import manipulator

host = "192.168.12.188"
port = 2001



a = astar()
image = cv2.imread('src/maze.png')
not_contours = a.contours(image)

matr = a.get_matrix(not_contours)
coord, X, Y, X_border, Y_border = a.get_trajectory(matr, 150, 150, 5, 15)

FINAL_PATH = a.path_segments(coord)
print(FINAL_PATH)
print(len(FINAL_PATH))

robot = rb.RobotControl(host=host, port=port)
# while True:
#     robot.send_to_robot(robot.move_direction('forward') + robot.set_left_motor_speed(50) + robot.set_right_motor_speed(50), 0)

# robot = rb.RobotControl(host="192.168.2.89", port=2001)
# while True:
#     robot.send_to_robot(robot._build_command([0x06, 0x04], 0.1))



# rotation_command = robot.set_rotation(90, 'left')
# if rotation_command:
#     robot.send_to_robot(rotation_command, 0.1)
# else:
#     print("Ошибка при создании команды вращения.")

robot.follow_path(FINAL_PATH)
# mn = manipulator() 

# while True:
#     mn.set_defolt_robohand()
#     x_position = robot.receive_from_robot()  # Get data from the robot (assuming this returns a valid coordinate)

#     if x_position < 20:
#         mn.cube_grab_kinematic(x_position)
#         time.sleep(2)

# robot.set_rotation(30)

a.draw_trajectory(coord, image, 150, 150, 5, 15, X, Y, X_border, Y_border)

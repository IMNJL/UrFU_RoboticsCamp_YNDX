import math
from robot import RobotControl


class manipulator:
    def __init__(self):
        self.robotcontrol = RobotControl(host="192.168.2.89", port=2001)  # Создаем экземпляр ClassA

    def method_b(self):
        result = self.robotcontrol.send_to_robot()  # Вызываем метод ClassA
        return f"ClassB calling: {result}"

    def set_servo_position(self, servo_id, angle):
        return self.robotcontrol._build_command([0x01], [servo_id, angle])

    def set_robohand_position(self, angle1, angle2, angle3, angle4):
        """Управляет положением всех четырех сервоприводов роборуки"""
        return (self.set_servo_position(0x02, angle2) +
                self.set_servo_position(0x01, angle1) +
                self.set_servo_position(0x03, angle3) +
                self.set_servo_position(0x04, angle4))

    def set_defolt_robohand(self):
        byte_command = self.robotcontrol._build_command([0x33], [0x00, 0x00])
        self.robotcontrol.send_to_robot(byte_command, 0)

    def press_the_button(self): #10 сантиметров от корпуса (плавно)
        angle1 = 85
        angle2 = 120
        for i in range(4):
            print(angle1)
            print(i)
            command_bytes = self.set_robohand_position(angle1, angle2, 90, 45)
            self.robotcontrol.send_to_robot(command_bytes, 0)
            print("GRAB")
            angle1 = 85 - i * 14
            angle2 = 95 - 1 * i

    def press_the_button2(self): #10 сантиметров от корпуса (резко)
        angle1 = 50
        angle2 = 150
        for i in range(3):
            print(angle1)
            print(i)
            command_bytes = self.set_robohand_position(angle1, angle2, 90, 45)
            self.robotcontrol.send_to_robot(command_bytes, 0)
            print("GRAB")
            angle2 = 150 - i * 40
            # angle2 = 95 - 1 * i

    def grab_the_cube(self): #7 сантиметров от корпуса
        angle1 = 85
        angle2 = 95
        self.set_defolt_robohand()
        command_bytes = b''
        for i in range(12):
            print(angle1)
            print(i)
            if angle1 == 35:
                self.robotcontrol.send_to_robot(command_bytes, 0)
                command_grab = self.set_robohand_position(angle1, angle2, 90, 37)
                self.robotcontrol.send_to_robot(command_grab, 0)
                print("GRAB")
            else:
                command_bytes += self.set_robohand_position(angle1, angle2, 90, 15)
                angle1 = 85 - i * 5
                angle2 = 95 - 3 * i


    @staticmethod
    def inverse_kinematic(x, y):
        height_offset = 5
        y -= height_offset # рука стоит на корпусе робота, учитываем возвышенность
        B = math.sqrt(x ** 2 + y ** 2)
        L1 = 13 # длина плеча 1
        L2 = 15 # длина плеча 2
        q1 = math.degrees(math.atan2(y, x))
        q2 = math.degrees(math.acos((L1 ** 2 - L2 ** 2 + B ** 2) / (2 * L1 * B)))
        Q1 = q1 + q2
        Q2 = -math.degrees(math.pi - math.acos((L1 ** 2 + L2 ** 2 - B ** 2) / (2 * L1 * L2)))
        return Q1, 180 - Q2

    def cube_grab_kinematic(self, x):
        y = 0.5
        self.set_defolt_robohand()
        cur_angle1 = 90
        cur_angle2 = 90
        grab_angle1, grab_angle2 = self.inverse_kinematic(x, y)
        delta1 = (grab_angle1 - cur_angle1)/10
        delta2 = (grab_angle2 - cur_angle2)/10
        command_bytes = b''
        for i in range(10):
            cur_angle1 = cur_angle1 - delta1
            cur_angle2 = cur_angle2 - delta2
            if cur_angle1 == grab_angle1:
                self.robotcontrol.send_to_robot(command_bytes, 0)
                command_grab = self.set_robohand_position(cur_angle1, cur_angle2, 90, 37)
                self.robotcontrol.send_to_robot(command_grab, 0)
            else:
                command_bytes += self.set_robohand_position(int(cur_angle1), int(cur_angle2), 90, 15)

    def press_button_kinematic(self, x, y):
        y = 8 # тесты фикс
        self.set_robohand_position(90, 90, 90, 37)
        cur_angle1 = 90
        cur_angle2 = 90
        press_angle1, press_angle2 = self.inverse_kinematic(x, y)
        delta1 = (press_angle1 - cur_angle1)/5
        delta2 = (press_angle2 - cur_angle2)/5
        command_bytes = b''
        for i in range(10):
            cur_angle1 = cur_angle1 - delta1
            cur_angle2 = cur_angle2 - delta2
            if cur_angle1 == press_angle1:
                self.robotcontrol.send_to_robot(command_bytes, 0)
                command_updown = (self.set_robohand_position(cur_angle1, cur_angle2 + 15, 90, 37) +
                                  self.set_robohand_position(cur_angle1, cur_angle2, 90, 37))
                self.robotcontrol.send_to_robot(command_updown, 0)
            else:
                command_bytes += self.set_robohand_position(int(cur_angle1), int(cur_angle2), 90, 15)

    def put_cube(self, x):
        y = 8 # тесты фикс
        self.set_robohand_position(90, 90, 90, 37)
        cur_angle1 = 90
        cur_angle2 = 90
        put_angle1, put_angle2 = self.inverse_kinematic(x, y)
        delta1 = (put_angle1 - cur_angle1)/10
        delta2 = (put_angle2 - cur_angle2)/10
        command_bytes = b''
        for i in range(10):
            cur_angle1 = cur_angle1 - delta1
            cur_angle2 = cur_angle2 - delta2
            if cur_angle1 == put_angle1:
                self.robotcontrol.send_to_robot(command_bytes, 0)
                command_grab = self.set_robohand_position(cur_angle1, cur_angle2, 90, 37)
                self.robotcontrol.send_to_robot(command_grab, 0)
            else:
                command_bytes += self.set_robohand_position(int(cur_angle1), int(cur_angle2), 90, 15)


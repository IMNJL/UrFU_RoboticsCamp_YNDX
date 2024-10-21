import socket
import time


class RobotControl:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.commands = {
            'forward': 0x01,  # Двигаться вперед
            'backward': 0x02,  # Двигаться назад
            'turn_left': 0x03,  # Повернуть налево
            'turn_right': 0x04,  # Повернуть направо
            'stop': 0x00  # Остановиться
        }

    def _build_command(self, header, data_bytes):
        """Собирает общую структуру команды с контрольными байтами"""
        return bytes([0xff] + header + data_bytes + [0xff])

    def send_to_robot(self, command, delay):
        """Отправка команды роботу через сокет"""
        try:
            # Создаем сокет
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"Соединение с {self.host}:{self.port}")

            # Устанавливаем соединение
            s.connect((self.host, self.port))
            print(f"Отправка команды: {command}")

            # Отправляем команду
            s.sendall(command)

            # Добавляем небольшую задержку между отправками команд
            time.sleep(delay)

            return True
        except socket.error as e:
            print(f"Ошибка сокета: {e}")
            return False
        finally:
            # Закрываем соединение
            s.close()
            print("Соединение закрыто")

    def receive_from_robot(self, buffer_size=1024):
        """Получение данных от робота через сокет"""
        try:
            # Создаем сокет
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"Соединение с {self.host}:{self.port}")

            # Устанавливаем соединение
            s.connect((self.host, self.port))

            print("Ожидание получения данных от робота...")
            # Получаем данные от робота
            byte_data = s.recv(buffer_size)  # Читаем данные из сокета
            num_array = [b for b in byte_data]

            print(f"Полученные данные: {num_array[3]}")
            return num_array[3]

        except socket.error as e:
            print(f"Ошибка сокета: {e}")
            return None
        finally:
            # Закрываем соединение
            s.close()
            print("Соединение закрыто")

    def move_direction(self, command):
        """Двигает робота в заданном направлении"""
        command_byte = self.commands.get(command, 0x00)
        return self._build_command([0x00], [command_byte, 0x00])

    def set_left_motor_speed(self, speed):
        """Устанавливает скорость левого двигателя (от 0 до 100)"""
        return self._build_command([0x02], [0x01, speed])

    def set_right_motor_speed(self, speed):
        """Устанавливает скорость правого двигателя (от 0 до 100)"""
        return self._build_command([0x02], [0x02, speed])

    def set_rotation_speed(self, angle):
        if angle == 75: #15 влево
            byte_command = self.set_left_motor_speed(100) + self.set_right_motor_speed(100) + self.move_direction('turn_left')
            self.send_to_robot(byte_command, 0.215)
        elif angle == 60: #30 влево
            byte_command = self.set_left_motor_speed(100) + self.set_right_motor_speed(100) + self.move_direction('turn_left')
            self.send_to_robot(byte_command, 0.287)
        elif angle == 45: #45 влево
            byte_command = self.set_left_motor_speed(100) + self.set_right_motor_speed(100) + self.move_direction('turn_left')
            self.send_to_robot(byte_command, 0.351)
        elif angle == 30: #60 влево
            byte_command = self.set_left_motor_speed(100) + self.set_right_motor_speed(100) + self.move_direction('turn_left')
            self.send_to_robot(byte_command, 0.419)
        elif angle == 15: #75 влево
            byte_command = self.set_left_motor_speed(100) + self.set_right_motor_speed(100) + self.move_direction('turn_left')
            self.send_to_robot(byte_command, 0.46)

    def set_rotation_func(self, angle):
        if angle < 90:
            byte_command = self.set_left_motor_speed(100) + self.set_right_motor_speed(100) + self.move_direction('turn_left')
            self.send_to_robot(byte_command, 0.0041 * (90 - angle) + 0.1598)
        elif angle > 90:
            byte_command = self.set_left_motor_speed(100) + self.set_right_motor_speed(100) + self.move_direction(
                'turn_right')
            self.send_to_robot(byte_command, 0.0041 * (angle - 90) + 0.1598)
        else:
            print("Вы не задали смещение")


    def move_robot(self, command, speed=50):
        """Комбинированная функция для движения робота с установкой скорости"""
        return self.set_left_motor_speed(speed) + self.set_right_motor_speed(speed) + self.move_direction(command)


    def set_rgb_lights(self, mode, color=0x00):
        """Устанавливает режим RGB-светодиодов"""
        if mode == 'normal':
            return self._build_command([0x06], [0x00, color])
        elif mode == 'irfollow':
            return self._build_command([0x06], [0x01, color])
        elif mode == 'trackline':
            return self._build_command([0x06], [0x02, color])
        elif mode == 'mode1':
            return self._build_command([0x06], [0x03, color])
        elif mode == 'mode2':
            return self._build_command([0x06], [0x04, color])
        else:
            raise ValueError("Invalid RGB mode")

    def set_car_lights(self, color):
        """Управляет фарами робота (включение/выключение)"""
        if color == 'green':
            return self._build_command([0x40], [0x00, 0x00])
        elif color == 'red':
            return self._build_command([0x40], [0x01, 0x00])
        else:
            raise ValueError("Invalid light state")


    def move_meters(self, meters, delay):
        byte_command = self.move_robot('forward', 100)
        self.send_to_robot(byte_command, delay)

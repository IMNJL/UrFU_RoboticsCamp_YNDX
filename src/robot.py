import socket
import time


class RobotControl:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.x = 0  # Начальная координата X
        self.y = 0
        self.orientation = 'up'  # Начальное направление робота
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
        if not (0 <= speed <= 255):
            raise ValueError(f"Некорректная скорость: {speed}. Должна быть от 0 до 255.")
        return self._build_command([0x02], [0x01, speed])

    def set_right_motor_speed(self, speed):
        """Устанавливает скорость правого двигателя (от 0 до 100)"""
        return self._build_command([0x02], [0x02, speed])

    def set_rotation(self, angle, direction):
        if direction == 'left':
            if angle == 15:
                byte_command = self.set_left_motor_speed(100) + self.set_right_motor_speed(100) + self.move_direction('turn_left')
                self.send_to_robot(byte_command, 0.235)
            elif angle == 30:
                byte_command = self.set_left_motor_speed(100) + self.set_right_motor_speed(100) + self.move_direction('turn_left')
                self.send_to_robot(byte_command, 0.2)
            elif angle == 45:
                byte_command = self.set_left_motor_speed(100) + self.set_right_motor_speed(100) + self.move_direction('turn_left')
                self.send_to_robot(byte_command, 0.23)
            elif angle == 60:
                byte_command = self.set_left_motor_speed(100) + self.set_right_motor_speed(100) + self.move_direction('turn_left')
                self.send_to_robot(byte_command, 0.38)
            elif angle == 90:
                byte_command = self.set_left_motor_speed(90) + self.set_right_motor_speed(80) + self.move_direction('turn_left')
                self.send_to_robot(byte_command, 0.57)
        else:        
            if angle == 15:
                byte_command = self.set_left_motor_speed(100) + self.set_right_motor_speed(100) + self.move_direction('turn_right')
                self.send_to_robot(byte_command, 0.235)
            elif angle == 30:
                byte_command = self.set_left_motor_speed(100) + self.set_right_motor_speed(100) + self.move_direction('turn_right')
                self.send_to_robot(byte_command, 0.22)
            elif angle == 45:
                byte_command = self.set_left_motor_speed(100) + self.set_right_motor_speed(100) + self.move_direction('turn_right')
                self.send_to_robot(byte_command, 0.3)
            elif angle == 60:
                byte_command = self.set_left_motor_speed(100) + self.set_right_motor_speed(100) + self.move_direction('turn_right')
                self.send_to_robot(byte_command, 0.39)
            elif angle == 90:
                byte_command = self.set_left_motor_speed(90) + self.set_right_motor_speed(80) + self.move_direction('turn_right')
                self.send_to_robot(byte_command, 0.587)
            
            
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


    def move_meters(self, cantimeters, delay):
        delay = 0.023506 * cantimeters + 0.189187
        byte_command = self.move_robot('forward', 80)
        self.send_to_robot(byte_command, delay)
   
    def follow_path(self, path_commands, path_speed=80, base_delay=0.023506, unit_delay=0.189187):
        if not path_commands:
            print("Путь не найден.")
            return

        print(f"Робот следует по пути из {len(path_commands)} команд.")

        # Определяем карту переходов для направлений
        orientation_map = {
            'up': {'dx': 0, 'dy': -1},
            'down': {'dx': 0, 'dy': 1},
            'left': {'dx': -1, 'dy': 0},
            'right': {'dx': 1, 'dy': 0}
        }

        # Проходим по списку команд
        for direction, steps in path_commands:
            print(f">>> Направление: {direction}, Шагов: {steps}")

            # Рассчитываем общее время движения
            delay = base_delay * steps + unit_delay

            # Если направление 'null', двигаемся прямо без поворота
            if direction == 'null':
                print("Направление 'null', двигаемся прямо.")
                move_command = (
                    self.move_direction('forward') +
                    self.set_left_motor_speed(path_speed) +
                    self.set_right_motor_speed(path_speed)
                )
                self.send_to_robot(move_command, delay=delay)

                # Обновляем координаты после завершения движения
                self.x += orientation_map[self.orientation]['dx'] * steps
                self.y += orientation_map[self.orientation]['dy'] * steps
                print(f"Текущие координаты: ({self.x}, {self.y})")

            else:
                # Если направление задано и не совпадает с текущей ориентацией, поворачиваем
                if direction != self.orientation:
                    turn_command = None

                    # Определяем команду поворота
                    if (self.orientation, direction) in [
                        ('up', 'right'), ('right', 'down'),
                        ('down', 'left'), ('left', 'up')
                    ]:
                        turn_command = 'turn_right'
                    elif (self.orientation, direction) in [
                        ('up', 'left'), ('left', 'down'),
                        ('down', 'right'), ('right', 'up')
                    ]:
                        turn_command = 'turn_left'
                    else:  # Поворот на 180°
                        turn_command = 'turn_right'
                        self.send_to_robot(self.move_direction(turn_command), delay=2)
                        self.update_orientation(direction)

                    # Выполняем поворот
                    if turn_command:
                        if turn_command == 'turn_left':
                            self.set_rotation(90)
                        else:
                            self.set_rotation_r(90)
                        self.update_orientation(direction)

                # Двигаемся вперед после поворота
                move_command = (
                    self.move_direction('forward') +
                    self.set_left_motor_speed(path_speed) +
                    self.set_right_motor_speed(path_speed)
                )
                self.send_to_robot(move_command, delay=delay)

                # Обновляем координаты
                self.x += orientation_map[self.orientation]['dx'] * steps
                self.y += orientation_map[self.orientation]['dy'] * steps
                print(f"Текущие координаты: ({self.x}, {self.y})")

        print("Робот завершил движение по пути.")


        
    def update_orientation(self, new_orientation):
        """Обновляет текущее направление робота."""
        print(f"Меняем ориентацию на: {new_orientation}")
        self.orientation = new_orientation
        
    def ultrasonic_avoid(self):
        distance = self.receive_from_robot()
        if distance < 2:
            command = self.move_direction('stop')

import os
import time
import threading
import serial.tools.list_ports
import sched
from data_parser import Parser


class Connection:

    def __init__(self, data, handler):
        self.handler = handler
        self.data = data
        self.parser = Parser()
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.thread = self.create_thread()
        self.kill = False
        self.port = None
        self.table = None
        self.interval = 1

    def establish_connection(self):
        if self.port is not None:
            self.port.close()
        ports = serial.tools.list_ports.comports()
        for device in ports:
            if device.vid is None or device.pid is None:
                continue
            if hex(device.vid) == '0x10c4' and hex(device.pid) == '0xea60':
                try:
                    self.port = serial.Serial(device.device, 2400, timeout=None, parity=serial.PARITY_NONE, rtscts=1)
                    return True
                except serial.serialutil.SerialException:
                    self.handler.info()
                    return False
        return False

    def start_measurement(self):
        self.kill = False
        self.scheduler.enter(self.interval, 1, self.get_data)
        self.scheduler.run()

    def get_data(self):
        data_string = None
        try:
            data_string = ""
            while len(data_string) != 14:
                self.port.reset_input_buffer()
                data_string = self.port.read_until(b'\n')
        except serial.serialutil.SerialException:
            self.handler.window.cont_measurement = False
        if self.kill:
            self.handler.window.cont_measurement = False
            return
        self.scheduler.enter(self.interval, 1, self.get_data)
        try:
            # print("device", data_string)
            correct = self.data.insert_value(self.parser.parse(data_string))
            if not correct:
                self.handler.window.cont_measurement = False
                return
            last_value = self.data.values[-1]
            self.table.add(last_value[0], last_value[1][0])
        except (ValueError, TypeError):
            self.handler.window.cont_measurement = False

    def create_thread(self):
        return threading.Thread(target=self.start_measurement)

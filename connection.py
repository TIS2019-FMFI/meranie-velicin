import os
import random
import time
import threading
import serial.tools.list_ports
import sched
from data_parser import Parser


class Connection:

    kill = False

    def __init__(self, data):
        self.data = data
        self.parser = Parser()
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.thread = threading.Thread(target=self.start_measurement)
        self.port = None

    def establish_connection(self):
        # ports = serial.tools.list_ports.comports()
        # if len(ports) == 0:
        #     os.system(r'driver\windows_10\CP210xVCPInstaller_x64.exe')
        # try:
        #     self.port = serial.Serial('COM3', 2400, timeout=None, parity=serial.PARITY_NONE, rtscts=1)
        # except serial.serialutil.SerialException:
        #     return False
        return True

    def start_measurement(self):
        if not self.establish_connection():
            return False
        self.scheduler.enter(1, 1, self.get_data)
        self.scheduler.run()

    def get_data(self):
        # data_string = self.port.read(14)
        if self.kill:
            return
        self.scheduler.enter(1, 1, self.get_data)
        data_string = 'aindrgvsoi' + str(random.randrange(1, 100))
        self.data.insert_value(data_string)

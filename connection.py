import os
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
        self.thread = threading.Thread(target=self.start_measurement, args=(self.data, ))
        self.port = None

    def establish_connection(self):
        ports = serial.tools.list_ports.comports()
        if len(ports) == 0:
            os.system(r'driver\windows_10\CP210xVCPInstaller_x64.exe')
        try:
            self.port = serial.Serial('COM3', 2400, timeout=None, parity=serial.PARITY_NONE, rtscts=1)
        except serial.serialutil.SerialException:
            return False
        return True

    def start_measurement(self, data):
        if not self.establish_connection():
            return False
        self.scheduler.enterabs(1, 1, self.get_data, (data, ))
        self.scheduler.run()

    def get_data(self, data):
        data_string = self.port.read(14)
        data.insert_value(self.parser.parse(data_string))
        if not self.kill:
            self.scheduler.enterabs(1, 1, self.get_data, (data, ))

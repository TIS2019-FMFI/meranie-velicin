import os
import time
import threading
import serial.tools.list_ports
import sched
from data_parser import Parser


class Connection:

    def __init__(self, data):
        self.data = data
        self.parser = Parser()
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.thread = self.create_thread()
        self.kill = False
        self.port_setup_successful = None
        self.port = None
        self.table = None

    def establish_connection(self):
        if self.port is not None:
            self.port.close()
        ports = serial.tools.list_ports.comports()
        if len(ports) == 0:
            os.system(r'driver\windows_10\CP210xVCPInstaller_x64.exe')
            ports = serial.tools.list_ports.comports()
        for device in ports:
            if hex(device.vid) == '0x10c4' and hex(device.pid) == '0xea60':
                try:
                    self.port = serial.Serial(device.device, 2400, timeout=None, parity=serial.PARITY_NONE, rtscts=1)
                    return True
                except serial.serialutil.SerialException:
                    return False
        return False

    def start_measurement(self):
        self.kill = False
        self.scheduler.enter(1, 1, self.get_data)
        self.scheduler.run()

    def get_data(self):
        data_string = None
        try:
            data_string = self.port.read(14)
        except serial.serialutil.SerialException:
            self.kill = True
        if self.kill:
            print('kill')
            return
        self.scheduler.enter(1, 1, self.get_data)
        print('enter', data_string)
        try:
            self.data.insert_value(self.parser.parse(data_string))
            last_value = self.data.values[-1]
            self.table.add(last_value[0], last_value[1][0])
        except ValueError:
            print('value error')
            pass

    def create_thread(self):
        return threading.Thread(target=self.start_measurement)

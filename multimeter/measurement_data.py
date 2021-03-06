import pickle
import xlsxwriter
import xlsxwriter.exceptions
from os import path
import datetime


class MeasurementData:

    def __init__(self):
        self.file_name = None
        self.interval = 1
        self.values = []

    def insert_value(self, value):
        if len(self.values) > 0 and self.values[-1][1][1] != value[1]:
            return False
        time = (1 + len(self.values)) * self.interval
        self.values.append((time, value))
        return True

    def get_last_value(self):
        try:
            return self.values[-1]
        except IndexError:
            return tuple()

    @staticmethod
    def already_exists(name, output_path=None):
        if output_path is not None:
            name = output_path + '/' + name
        if not path.exists(name):
            return False
        if not path.isfile(name):
            return False
        return True

    def export_to_excel(self):
        if self.already_exists(self.file_name + '.xlsx'):
            d = datetime.datetime.today()
            self.file_name += "_" + d.strftime('%d-%m-%Y')
        workbook = xlsxwriter.Workbook(self.file_name + '.xlsx')
        worksheet = workbook.add_worksheet()

        worksheet.write(0, 0, 'Čas')
        worksheet.write(1, 0, 'Hodnota')
        col = 1
        for value in self.values:
            worksheet.write(0, col, value[0])
            worksheet.write(1, col, value[1][0])
            col += 1

        chart = workbook.add_chart({'type': 'line'})
        chart.set_size(options={'width': 1000, 'height': 500})
        chart.add_series({'values': '=Sheet1!$B$2:$' + self.get_end_column() + '$2'})
        worksheet.insert_chart('A4', chart)

        try:
            workbook.close()
        except xlsxwriter.exceptions.FileCreateError:
            return False
        return True

    def get_end_column(self):
        length = len(self.values)
        res = ''
        while length >= 0:
            letter = length % 26
            res = chr(ord('A') + letter) + res
            length //= 26
            length -= 1
        return res

    def pickle(self):
        if self.file_name is None:
            return False
        if not path.exists('./data'):
            return False
        if self.already_exists('data/' + self.file_name + '.pickle'):
            d = datetime.datetime.today()
            self.file_name += "_" + d.strftime('%d-%m-%Y')
        with open('data/' + self.file_name + '.pickle', 'wb') as output:
            pickle.dump(obj=self, file=output)
        return True

    def clear(self):
        self.values.clear()
        self.file_name = None
        self.interval = 1


def unpickle(path):
    with open(path, 'rb') as read:
        return pickle.load(read)

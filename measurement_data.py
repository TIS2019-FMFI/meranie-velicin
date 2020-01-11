import pickle
import random
import xlsxwriter
import xlsxwriter.exceptions


class MeasurementData:

    def __init__(self):
        self.file_name = None
        self.values = []

    def insert_value(self, value):
        self.values.append(value)

    def get_last_value(self):
        try:
            return self.values[-1]
        except IndexError:
            return tuple()

    def export_to_excel(self):
        workbook = xlsxwriter.Workbook(self.file_name + '.xlsx')
        worksheet = workbook.add_worksheet()
        col = 0
        for items in self.values:
            worksheet.write(0, col, items[0])
            worksheet.write(1, col, items[1])
            col += 1

        chart = workbook.add_chart({'type': 'line'})
        chart.set_size(options={'width': 1000, 'height': 500})
        chart.add_series({'values': '=Sheet1!$B$2:$' + self.get_end_column() + '$2'})
        worksheet.insert_chart('A4', chart)

        try:
            workbook.close()
        except xlsxwriter.exceptions.FileCreateError:
            # TODO handle file write exception if target file is open
            return

    def get_end_column(self):
        length = len(self.values) - 1
        res = ''
        while length >= 0:
            letter = length % 26
            res = chr(ord('A') + letter) + res
            length //= 26
            length -= 1
        return res

    def pickle(self):
        print(self.file_name, self.values)
        if self.file_name is None:
            return False
        with open('data/' + self.file_name + '.pickle', 'wb') as output:
            pickle.dump(obj=self, file=output)


def unpickle(path):
    with open(path, 'rb') as read:
        return pickle.load(read)


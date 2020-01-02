import pickle


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

    def pickle(self):
        print(self.file_name, self.values)
        if self.file_name is None:
            return False
        with open('data/' + self.file_name + '.pickle', 'wb') as output:
            pickle.dump(obj=self, file=output)


def unpickle(path):
    with open(path, 'rb') as read:
        return pickle.load(read)

class MeasurementData:

    def __init__(self):
        self.values = []

    def insert_value(self, value):
        self.values.append(value)

    def get_last_value(self):
        try:
            return self.values[-1]
        except IndexError:
            return tuple()

    def pickle(self):
        pass

    def unpickle(self):
        pass

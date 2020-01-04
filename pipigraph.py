from winsound import Beep

class PipiGraph():

    def __init__(self):
        self.device = None
        #pristroj ...

    def play(self, value):
        #values: 0 - 1023
        Beep(500 + value, 500)


if __name__ == "__main__":
    ppg = PipiGraph()
    #for i in [100, 120, 80, 200, 1020, 500, 700, 1023]:
    for i in [10, 30, 50, 70, 50, 30, 10]:
        ppg.play(i)
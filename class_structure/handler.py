#!/usr/bin/env python3

import connection
import measurement


class Handler:

    def __init__(self, gui):
        self.gui = gui
        self.connection = connection.Connection()
        self.measurement = measurement.Measurement()

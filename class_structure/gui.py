#!/usr/bin/env python3

import handler
import graph_panel as graph
import menu_panel as menu
import table_panel as table


class GUI:

    def __init__(self):
        self.handler = handler.Handler(self)
        self.menu = menu.MenuPanel()
        self.table = table.TablePanel()
        self.graph = graph.GraphPanel()

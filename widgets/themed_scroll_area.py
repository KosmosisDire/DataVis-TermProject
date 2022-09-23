from typing import List
from PyQt6.QtWidgets import * 
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import * 
from PyQt6.QtCore import *

from styles import Styles
from widgets.custom_widget import CustomWidget
from widgets.vertical_group import VerticalGroup 

class ThemedScrollArea(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        self.setStyleSheet("background-color: transparent; border: 0px; border-radius: 0px;")
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setWidget(VerticalGroup())
        self.widgets: List[QWidget] = []

    def addWidget(self, widget: QWidget):
        self.widget().layout().addWidget(widget)
        self.widgets.append(widget)

    def addWidgets(self, widgets: List[QWidget]):
        for widget in widgets:
            self.addWidget(widget)

    def setLayout(self, layout: QLayout, spacing = 0, margins = (0, 0, 0, 0)):
        super().setLayout(layout)
        super().setContentsMargins(0, 0, 0, 0)
        super().widget().layout().setContentsMargins(*margins)
        super().widget().layout().setSpacing(spacing)

    def setSpacing(self, spacing: int):
        self.widget().layout().setSpacing(spacing)

    def setContentsMargins(self, margins: tuple[int, int, int, int]):
        self.widget().layout().setContentsMargins(*margins)
from typing import List
from PyQt6.QtWidgets import * 
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import * 
from PyQt6.QtCore import *

from styles import Styles 

class ThemedScrollArea(QScrollArea):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Shape.NoFrame)

    def addWidget(self, widget):
        self.layout().addWidget(widget)

    def setLayout(self, layout, spacing = 0, margins = (0, 0, 0, 0)):
        super().setLayout(layout)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout().setContentsMargins(*margins)
        self.layout().setSpacing(spacing)

    def addWidgets(self, widgets: List[QWidget]):
        for widget in widgets:
            self.addWidget(widget)
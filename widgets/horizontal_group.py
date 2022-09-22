from PyQt6.QtWidgets import * 
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import * 
from PyQt6.QtCore import * 




class HorizonalGroup(QWidget):
    def __init__(self, widgets: list[QWidget], spacing: int, parent=None):
        super().__init__(parent)
        self.widgets = widgets
        self.layout = QHBoxLayout()
        self.layout.setSpacing(spacing)
        for widget in self.widgets:
            self.layout.addWidget(widget)
        self.setLayout(self.layout)
        self.setContentsMargins(0, 0, 0, 0)

    def addWidget(self, widget: QWidget):
        self.layout.addWidget(widget)
        self.widgets.append(widget)
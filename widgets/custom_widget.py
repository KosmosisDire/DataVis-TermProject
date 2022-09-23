from email import policy
from typing import List
from PyQt6.QtWidgets import * 
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import * 
from PyQt6.QtCore import *


class CustomWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.widgets = []


    def width(self) -> int:
        return super().width() - self.contentsMargins().left() - self.contentsMargins().right()

    def height(self) -> int:
        return super().height() - self.contentsMargins().top() - self.contentsMargins().bottom()

    def left(self) -> int:
        return self.contentsMargins().left()
    
    def right(self) -> int:
        return self.width() + self.contentsMargins().left()

    def right_margin(self) -> int:
        return self.contentsMargins().right()
    
    def top(self) -> int:
        return self.contentsMargins().top()

    def bottom(self) -> int:
        return self.height() + self.contentsMargins().top()
    
    def bottom_margin(self) -> int:
        return self.contentsMargins().bottom()

    def rect(self) -> QtCore.QRect:
        return QtCore.QRect(self.left(), self.top(), self.width(), self.height())

    def addWidget(self, widget) -> QWidget:
        if(self.layout() is None):
            self.setLayout(QVBoxLayout())
        self.layout().addWidget(widget)
        self.widgets.append(widget)

        return widget

    def setLayout(self, layout: QLayout, spacing = 0, margins = (0, 0, 0, 0)):
        super().setLayout(layout)
        super().setContentsMargins(0, 0, 0, 0)
        super().layout().setContentsMargins(*margins)
        super().layout().setSpacing(spacing)

    def addWidgets(self, widgets: List[QWidget]):
        for widget in widgets:
            self.addWidget(widget)

from typing import List
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLayout
from PyQt6.QtGui import QPalette
from PyQt6.QtWidgets import QGraphicsDropShadowEffect

from styles import Styles


class CustomWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.widgets = []


    def width(self) -> int:
        
        return super().width() - self.left() - self.right_margin()

    def height(self) -> int:
        return super().height() - self.top() - self.bottom_margin()

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

    def fill(self, color: QColor | str):

        c = QColor(color)

        self.setAutoFillBackground(True)
        palette = self.palette()
        if palette is None:
            palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, c)
        self.setPalette(palette)

    def setShadow(self, blurRadius: int = Styles.theme.panel_shadow_radius, xOffset: int = 0, yOffset: int = 0, color: QtGui.QColor = Styles.theme.shadow_color):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(blurRadius)
        shadow.setOffset(xOffset, yOffset)
        shadow.setColor(color)
        self.setGraphicsEffect(shadow)

    def is_on_screen(self):
        if not self.visibleRegion().isEmpty():
            return True
        return False

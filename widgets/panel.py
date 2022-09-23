from PyQt6.QtWidgets import QWidget, QGraphicsDropShadowEffect, QLayout, QLabel
from PyQt6.QtGui import QColor, QPalette
from styles import Styles

from widgets.custom_widget import CustomWidget

class Panel(CustomWidget):
    def __init__(self, color: str = "transparent"):
        super(Panel, self).__init__()

        self.fill(color)

from PyQt6.QtWidgets import * 
from PyQt6.QtGui import * 
from PyQt6.QtCore import *
from styles import Styles


from widgets.custom_widget import CustomWidget

# adds a seperator line with space on either side
class HorizontalSeperator(CustomWidget):
    def __init__(self, spacing: int, thickness: int = 1):
        super().__init__()
        self.setFixedHeight(spacing)
        self.thickness = thickness

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # main panel
        painter.setPen(QPen(Qt.GlobalColor.transparent))
        painter.setBrush(QBrush(Styles.theme.seperator_color))
        painter.drawRect(0, self.height()//2 - self.thickness//2, self.width(), self.thickness)
        


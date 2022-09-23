from PyQt6.QtWidgets import QWidget, QGraphicsDropShadowEffect, QLayout, QLabel
from PyQt6.QtGui import QColor, QPalette

from widgets.custom_widget import CustomWidget

class Panel(CustomWidget, QLabel):
    def __init__(self, color = "transparent", shadow_radius = 0, shadow_color = QColor(0, 0, 0, 0), shadow_offset = (0, 0)):
        super(Panel, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

        if shadow_radius > 0:
            self.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=shadow_radius, xOffset=shadow_offset[0], yOffset=shadow_offset[1], color=shadow_color))

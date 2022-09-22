from PyQt6.QtWidgets import QWidget, QGraphicsDropShadowEffect, QLayout
from PyQt6.QtGui import QColor, QPalette

class BlankWidget(QWidget):
    def __init__(self, color = "transparent", shadow_radius = 0, shadow_color = QColor(0, 0, 0, 0), shadow_offset = (0, 0)):
        super(BlankWidget, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

        if shadow_radius > 0:
            self.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=shadow_radius, xOffset=shadow_offset[0], yOffset=shadow_offset[1], color=shadow_color))

    def addWidget(self, widget):
        self.layout().addWidget(widget)

    def setLayout(self, a0: QLayout):
        super().setLayout(a0)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

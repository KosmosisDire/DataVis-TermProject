from widgets.utility_widgets.custom_widget import CustomWidget
from PyQt6.QtGui import QColor, QPalette, QPaintEvent, QPainter, QPen


class Panel(CustomWidget):
    def __init__(self, color: QColor | str = "transparent", force_paint: bool = False, border_radius: int = 0, margins = (0,0,0,0), padding: int = 0):
        super(Panel, self).__init__()
        if not force_paint: 
            self.fill(color)
            
        self.setContentsMargins(*margins)

        self.color = color
        self.force_paint = force_paint
        self.border_radius = border_radius
        self.margins = margins
        self.padding = padding
        

    def paintEvent(self, a0: QPaintEvent) -> None:
        if not self.force_paint:
            return super().paintEvent(a0)

        painter = QPainter(self)
        painter.setBrush(QColor(self.color))
        painter.setPen(QPen(QColor(self.color)))
        painter.drawRoundedRect(self.rect(), self.border_radius, self.border_radius)

        return super().paintEvent(a0)


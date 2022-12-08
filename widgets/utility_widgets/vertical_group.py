import math
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from widgets.utility_widgets.custom_widget import CustomWidget 




class VerticalGroup(CustomWidget):
    def __init__(self, widgets: list[QWidget] = [], spacing: int = 0, margins = (math.inf, 0, 0, 0)):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.layout().setSpacing(spacing)

        if margins[0] == math.inf:
            margins = (0, spacing, 0, spacing)

        self.layout().setContentsMargins(*margins)
        
        for widget in widgets:
            self.addWidget(widget)


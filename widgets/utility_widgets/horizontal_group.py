import math
from PyQt6.QtWidgets import * 
from PyQt6 import *
from PyQt6.QtGui import * 
from PyQt6.QtCore import *

from widgets.utility_widgets.custom_widget import CustomWidget

class HorizontalGroup(CustomWidget):
    def __init__(self, widgets: list[QWidget] = [], spacing: int = 0, margins = (math.inf, 0, 0, 0)):
        super().__init__()
        self.setLayout(QHBoxLayout())
        self.layout().setSpacing(spacing)
        
        if margins[0] == math.inf:
            margins = (spacing, 0, spacing, 0)

        self.layout().setContentsMargins(*margins)

        for widget in widgets:
            self.addWidget(widget)
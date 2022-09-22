import string
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import * 
from PyQt6.QtCore import *
from styles import Styles

from widgets.colored_text import ColoredText


class LabeledWidget(QWidget):
    def __init__(self, label_text: string, widget: QWidget, parent=None):
        super().__init__(parent)
        self.label_text: string = label_text
        self.widget: QWidget = widget

        self.label = ColoredText(self.label_text, Styles.theme.label_color, Styles.theme.label_font_size)

        self.layout = QHBoxLayout()
        self.layout.setSpacing(Styles.theme.close_spacing)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.widget)
        self.setLayout(self.layout)
        self.setFont(QFont("Segoe UI", Styles.theme.label_font_size))
        

import string
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import QLabel

from styles import Styles

class ColoredText(QLabel):
    def __init__(self, text: string, color: QColor = None, fontSize: int = 24, margins = (0, 0, 0, 0)):
        super().__init__()
        self.text: string = text
        self.color: QColor = color
        self.fontSize: int = fontSize
        self.margins = margins

        if color == None:
            self.color = Styles.theme.label_color

        self.setText(self.text)
        self.setStyleSheet(f"background-color: transparent; color: {self.color.name()}; font-size: {self.fontSize}px; font-family: {Styles.theme.font_family};")
        self.setFont(QFont(Styles.theme.font_family, self.fontSize))
        self.setContentsMargins(*self.margins)
import string
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import QLabel

class ColoredText(QLabel):
    def __init__(self, text: string, color: QColor, fontSize: int = 24, margins = (0, 0, 0, 0)):
        super().__init__()
        self.text: string = text
        self.color: QColor = color
        self.fontSize: int = fontSize
        self.margins = margins

        self.setText(self.text)
        self.setStyleSheet(f"background-color: transparent; color: {self.color.name()}; font-size: {self.fontSize}px; font-family: Segoe UI;")
        self.setFont(QFont("Segoe UI", self.fontSize))
        self.setContentsMargins(*self.margins)
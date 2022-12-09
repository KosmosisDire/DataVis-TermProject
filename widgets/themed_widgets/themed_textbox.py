from typing import Callable
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtGui import QFont
from styles import Styles

class ThemedTextbox(QLineEdit):
    def __init__(self, textChanged: Callable[[str], any], placeholder: str = "", height: int = None, margins: tuple = (0,0,0,0)):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setFixedHeight(height or Styles.theme.button_height)
        self.setContentsMargins(*margins)

        self.setStyleSheet(f"""
            QLineEdit {{
                background-color: {Styles.theme.button_color_hex};
                color: {Styles.theme.button_text_color_hex};
                border: 1px;
                border-radius: {Styles.theme.control_radius}px;
                font-size: {Styles.theme.button_font_size};
                font-family: {Styles.theme.font_family};
            }}
        """)

        # when the text is changed and it's empty set the placeholder text color so a dimmer color
        self.textChanged.connect(lambda: self.style().unpolish(self) if self.text() == "" else self.style().polish(self))
        self.textChanged.connect(textChanged)



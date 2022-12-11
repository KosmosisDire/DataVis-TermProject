from time import time
from PyQt6.QtWidgets import * 
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import * 
from PyQt6.QtCore import *

from styles import Styles
from widgets.utility_widgets.custom_widget import CustomWidget 



class ThemedButton(QPushButton):
    def __init__(self, text: str, clicked: callable = None, shadow: bool = True):
        if clicked is not None: QPushButton.__init__(self, text, clicked=clicked)
        else: QPushButton.__init__(self, text)

        self.setFixedHeight(Styles.theme.button_height)

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {Styles.theme.button_color_hex};
                color: {Styles.theme.button_text_color_hex};
                border: 0px;
                border-radius: {Styles.theme.control_radius}px;
                font-size: {Styles.theme.button_font_size};
                font-family: Segoe UI;
            }}
            QPushButton:hover {{
                background-color: {Styles.theme.button_hover_color_hex};
            }}
            QPushButton:pressed {{
                background-color: {Styles.theme.button_pressed_color_hex};
            }}
        """)

        if shadow: self.setShadow()
        self.setFont(QFont("Segoe UI", Styles.theme.button_font_size))

    def setShadow(self, blurRadius: int = Styles.theme.control_shadow_radius, xOffset: int = 0, yOffset: int = 4, color: QtGui.QColor = Styles.theme.shadow_color):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(blurRadius)
        shadow.setOffset(xOffset, yOffset)
        shadow.setColor(color)
        self.setGraphicsEffect(shadow)


        
from time import time
from PyQt6.QtWidgets import * 
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import * 
from PyQt6.QtCore import *

from styles import Styles
from widgets.custom_widget import CustomWidget 



class ThemedButton(QPushButton):
    def __init__(self, text: str, clicked: callable = None):
        super(ThemedButton, self).__init__(text, clicked=clicked)

        self.setFixedHeight(Styles.theme.button_height)

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {Styles.theme.button_color_hex};
                color: {Styles.theme.button_text_color_hex};
                border: 0px;
                border-radius: {Styles.theme.corner_radius}px;
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

        self.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=6, xOffset=0, yOffset=3, color=QColor(0, 0, 0, 50)))
        self.setFont(QFont("Segoe UI", Styles.theme.button_font_size))


        
from typing import Any, Callable
from PyQt6.QtWidgets import * 
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import * 
from PyQt6.QtCore import *

from styles import Styles
from widgets.custom_widget import CustomWidget 



class ThemedRadioButton(QRadioButton):
    def __init__(self, stateChanged: Callable[[bool], Any], shadow: bool = True):
        super().__init__("")
        self.setStyleSheet(f"""
            QRadioButton
            {{
                background-color: transparent;
            }}

            QRadioButton::indicator {{
                width: {Styles.theme.button_height}px;
                height: {Styles.theme.button_height}px;
            }}
            QRadioButton::indicator:checked {{
                image: url(assets/radio_checked.png);
            }}
            QRadioButton::indicator:unchecked {{
                image: url(assets/radio_unchecked.png);
            }}
        """)

        stateChanged(self.isChecked())

        if shadow: self.setShadow()

        if stateChanged:
            self.clicked.connect(stateChanged)

    def setShadow(self, blurRadius: int = Styles.theme.control_radius, xOffset: int = 0, yOffset: int = 4, color: QtGui.QColor = Styles.theme.shadow_color):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(blurRadius)
        shadow.setOffset(xOffset, yOffset)
        shadow.setColor(color)
        self.setGraphicsEffect(shadow)
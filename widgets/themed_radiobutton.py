from typing import Any, Callable
from PyQt6.QtWidgets import * 
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import * 
from PyQt6.QtCore import *

from styles import Styles 



class ThemedRadioButton(QRadioButton):
    def __init__(self, callback: Callable[[bool], Any]):
        super().__init__("")
        self.setStyleSheet(f"""
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

        callback(self.isChecked())

        if callback:
            self.clicked.connect(callback)
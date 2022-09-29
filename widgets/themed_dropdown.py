from time import time
from typing import Any, Callable, Dict, Iterable, List
from PyQt6.QtWidgets import * 
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import * 
from PyQt6.QtCore import *

from styles import Styles
from widgets.custom_widget import CustomWidget 



class ThemedDropdown(QComboBox):
    def __init__(self, items: Dict[str, Any], itemChanged: Callable[[Any], Any] = None, shadow: bool = True):
        super(ThemedDropdown, self).__init__()
        self.items: Dict[str, Any] = dict()
        self.texts: List[str] = list()
        self.itemChanged = itemChanged

        self.currentIndexChanged.connect(self.index_changed)

        self.setStyleSheet(f"""
            QComboBox {{
                background-color: {Styles.theme.button_color_hex};
                color: {Styles.theme.button_text_color_hex};
                border: 0px;
                border-radius: {Styles.theme.control_radius}px;
                font-size: {Styles.theme.button_font_size};
                font-family: Segoe UI;
            }}
            QComboBox:hover {{
                background-color: {Styles.theme.button_hover_color_hex};
            }}
            QComboBox:pressed {{
                background-color: {Styles.theme.button_hover_color_hex};
            }}
            QComboBox::drop-down {{
                background-color: none;
                background-image: url(assets/dropdown.png);
                background-repeat: no-repeat;
                background-position: center;
                width: {Styles.theme.button_height}px;
                height: {Styles.theme.button_height}px;
                border: 0px;
                border-radius: {Styles.theme.control_radius}px;
            }}
            QComboBox QAbstractItemView 
            {{
                border: 0px;
                background-color: {Styles.theme.button_color_hex};
                color: {Styles.theme.button_text_color_hex};
                font-size: {Styles.theme.button_font_size};
                font-family: Segoe UI;
                selection-background-color: {Styles.theme.dark_background_color_hex};
            }}
        """)

        
        self.setFixedHeight(Styles.theme.button_height)
        self.setFont(QFont("Segoe UI", Styles.theme.button_font_size))
        if shadow: self.setShadow()
        self.addItems(items)
    
    def addItem(self, text: str, value: Any):
        self.items[text] = value
        self.texts.append(text)
        super(ThemedDropdown, self).addItem(text, value)

    def addItems(self, items: Dict[str, Any]):
        for item in items:
            self.addItem(item, items[item])

    def index_changed(self, index: int) -> None:
        self.itemChanged(self.items[self.texts[index]])

    def setShadow(self, blurRadius: int = Styles.theme.control_radius, xOffset: int = 0, yOffset: int = 4, color: QtGui.QColor = Styles.theme.shadow_color):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(blurRadius)
        shadow.setOffset(xOffset, yOffset)
        shadow.setColor(color)
        self.setGraphicsEffect(shadow)
        
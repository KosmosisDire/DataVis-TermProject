from typing import Any, Callable
from data_handler import DataHandler
from styles import Styles
from widgets.utility_widgets.custom_widget import CustomWidget
from PyQt6.QtWidgets import QCheckBox, QBoxLayout, QLabel
from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor, QPaintEvent, QPainter, QPen, QBrush, QFont, QFontMetrics
from PyQt6.QtCore import QRect
from widgets.new_widgets.flow_layout import FlowLayout
from widgets.utility_widgets.panel import Panel


class TagCheckbox(QCheckBox):
    def __init__(self, tag_name: str, padding: int, stateChanged: Callable[[bool, str], Any], font_size = Styles.theme.button_font_size, shadow: bool = True):
        super().__init__()

        self.setStyleSheet(f"""
            QCheckBox
            {{
                background-color: transparent;
                padding: {padding}px;
            }}

            QCheckBox::indicator {{
                width: {Styles.theme.button_height}px;
                height: {Styles.theme.button_height}px;
            }}
            QCheckBox::indicator:checked {{
                image: url(assets/radio_checked_round.png);
            }}
            QCheckBox::indicator:unchecked {{
                image: url(assets/radio_unchecked_round.png);
            }}
        """)

        

        if shadow: self.setShadow()

        if stateChanged:
            stateChanged(self.isChecked(), tag_name)
            self.clicked.connect(lambda: stateChanged(self.isChecked(), tag_name))

        self.tag_name = tag_name
        self.font_size = font_size
        self.padding = padding

        self.font_metrics: QFontMetrics = QFontMetrics(QFont(Styles.theme.font_family, self.font_size));
        self.text_size = self.font_metrics.boundingRect(self.tag_name)
        self.toggle_width = 32 # the image is 32 x 32 pixels
        self.setFixedWidth(self.text_size.width() + self.padding * 4 + self.toggle_width)

    def setShadow(self, blurRadius: int = Styles.theme.control_shadow_radius, xOffset: int = 0, yOffset: int = 4, color: QColor = Styles.theme.shadow_color):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(blurRadius)
        shadow.setOffset(xOffset, yOffset)
        shadow.setColor(color)
        self.setGraphicsEffect(shadow)

    def paintEvent(self, a0: QPaintEvent) -> None:
        painter = QPainter(self)
        # painter.setPen(QPen(Styles.theme.button_text_color, 2))
        painter.setPen(QPen(QColor("transparent")))
        painter.setBrush(QBrush(Styles.theme.button_color))

        painter.setClipRect(self.rect())
        radius = self.rect().height()//2
        painter.drawRoundedRect(0, 0, self.rect().width(), self.height(), radius, radius)

        painter.setPen(QPen(Styles.theme.button_text_color))
        painter.setBrush(QBrush(Styles.theme.button_text_color))
        painter.setFont(QFont(Styles.theme.font_family, self.font_size))


        painter.drawText(self.toggle_width + self.padding, self.padding, self.rect().width() - self.toggle_width, self.rect().height() + self.padding * 2, 0, self.tag_name)

        return super().paintEvent(a0)

class TagSelector(CustomWidget):
    def __init__(self, tags: list[str], max_height: int = 200):
        super().__init__()
        self.tags: list[str] = []
        self.selected_tags: list[str] = []
        self.tag_checkboxes: list[TagCheckbox] = []

        self.setMaximumHeight(max_height)
        
        background:Panel = self.addWidget(Panel())
        self.sizer:Panel = background.addWidget(Panel(Styles.theme.mid_background_color, True, Styles.theme.panel_radius))
        layout: FlowLayout = FlowLayout(None, 8, 8, 8)
        self.sizer.setLayout(layout)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.doLayout(self.rect(), False)
        
        
        self.add_tags(tags)

    def tag_selection_changed(self, checked: bool, tag_name: str):
        if checked:
            self.selected_tags.append(tag_name)
        else:
            if tag_name in self.selected_tags: self.selected_tags.remove(tag_name)

    def get_selected_tags(self) -> list[str]:
        return self.selected_tags

    def get_all_tags(self) -> list[str]:
        return self.tags
    
    def get_unselected_tags(self) -> list[str]:
        return [tag for tag in self.tags if tag not in self.selected_tags]

    def add_tag(self, tag: str):
        self.tags.append(tag)
        tag_button = TagCheckbox(tag, 4, self.tag_selection_changed)
        self.tag_checkboxes.append(tag_button)
        self.sizer.addWidget(tag_button)

    def add_tags(self, tags: list[str]):
        for tag in tags:
            self.add_tag(tag)
        
    def clear_tags(self):
        self.selected_tags.clear()
        for tag_button in self.tag_checkboxes:
            self.layout().removeWidget(tag_button)
            tag_button.deleteLater()

        self.tag_checkboxes.clear()

    def update_tags(self, tags: list[str]):
        self.clear_tags()
        self.add_tags(tags)

    

    
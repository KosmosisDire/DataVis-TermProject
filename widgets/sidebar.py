from time import time
from PyQt6.QtWidgets import * 
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import * 
from PyQt6.QtCore import * 

import math

from styles import Styles
from widgets.custom_widget import CustomWidget
from widgets.horizontal_group import HorizontalGroup
from widgets.vertical_group import VerticalGroup

# Custom collapsable sidebar widget. Uses paintEvent to draw rounded corners, and a callback for the collapse/expand animation.
class Sidebar(VerticalGroup):
    def __init__(self, header_height = 64, blurRadius = 24):
        super().__init__()
        self._collapsed = False
        self._widthAnimation = QPropertyAnimation(self, b"maximumWidth", self)
        self._widthAnimation.setDuration(250)
        self._widthAnimation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self._widthAnimation.setStartValue(Styles.theme.min_sidebar_width)
        self._widthAnimation.setEndValue(header_height//2)
        

        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)

        self.header_height = header_height

        self.layout().setAlignment(Qt.AlignmentFlag.AlignTop)

        self.header_frame = super().addWidget(HorizontalGroup())
        self.header_frame.setFixedHeight(self.header_height)

        self.main_container = super().addWidget(VerticalGroup())
        self.main_container.layout().setAlignment(Qt.AlignmentFlag.AlignTop)

        self.toggle_button = QPushButton("", clicked=self.toggle)
        self.toggle_button.setIcon(QIcon("assets/collapse.png"))
        self.toggle_button.setStyleSheet(f"border: 0px;")
        self._button_pixmap = QtGui.QPixmap("assets/collapse.png")


        self._button_animation = QtCore.QVariantAnimation(
            self,
            startValue=0.0,
            endValue=-180.0,
            duration=200,
            valueChanged=self.on_button_animate
        )
        self._button_animation.finished.connect(self.on_toggleanim_finished)

        self.header_frame.addWidget(self.toggle_button)



        self.expand()

    def addWidget(self, widget: QWidget) -> QWidget:
        self.main_container.addWidget(widget)
        return widget

    def getLayout(self) ->QLayout:
        return self.main_container.layout()

    def set_container_layout(self, layout: QLayout):
        self.main_container.setLayout(layout)

    @QtCore.pyqtSlot(QtCore.QVariant)
    def on_button_animate(self, value):
        t = QtGui.QTransform()
        t.rotate(value)
        self._button_pixmap.transformed(t).save("assets/collapse_rotate.png")
        self.toggle_button.setIcon(QIcon("assets/collapse_rotate.png"))

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # main panel
        painter.setPen(QPen(Qt.GlobalColor.transparent))
        painter.setBrush(QBrush(Styles.theme.dark_background_color))
        painter.drawRoundedRect(self.rect(), Styles.theme.panel_radius, Styles.theme.panel_radius)
        painter.drawRect(QRectF(0, 0, Styles.theme.panel_radius, self.height())) # left corners are filled so they aren't rounded

        # header
        painter.setBrush(QBrush(Styles.theme.light_background_color))
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.header_height), Styles.theme.panel_radius, Styles.theme.panel_radius) 
        painter.drawRect(QRectF(0, 0, Styles.theme.panel_radius, self.header_height)) # left corners are filled so they aren't rounded
        painter.drawRect(QRectF(self.width() - Styles.theme.panel_radius, self.header_height-Styles.theme.panel_radius, Styles.theme.panel_radius, Styles.theme.panel_radius)) # bottom right corner is filled so it isn't rounded

    def on_toggleanim_finished(self):
        if(self._collapsed):
            self.main_container.setVisible(False)
            self.toggle_button.setFixedSize(self.header_height//2, self.header_height)
        else:
            self.toggle_button.setFixedSize(self.header_height//2 + Styles.theme.medium_spacing, self.header_height)

    def collapse(self):
        self._widthAnimation.setDirection(QPropertyAnimation.Direction.Forward)
        self._widthAnimation.start()
        self._button_animation.setDirection(QPropertyAnimation.Direction.Forward)
        self._button_animation.start()

    def expand(self):
        self._widthAnimation.setDirection(QPropertyAnimation.Direction.Backward)
        self._widthAnimation.start()
        self._button_animation.setDirection(QPropertyAnimation.Direction.Backward)
        self._button_animation.start()
        self.main_container.setVisible(True)
        self.header_frame.layout().setAlignment(Qt.AlignmentFlag.AlignRight)
        

    def toggle(self):
        if self._collapsed:
            self.expand()
        else:
            self.collapse()
        self._collapsed = not self._collapsed

    def on_resize(self, event):
        value: int = max(int(event.size().width() / 5), Styles.theme.min_sidebar_width)

        if not self._collapsed:
            self.setMaximumWidth(value)

        self._widthAnimation.setStartValue(value)
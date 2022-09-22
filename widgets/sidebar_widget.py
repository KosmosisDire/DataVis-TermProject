from time import time
from PyQt6.QtWidgets import * 
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import * 
from PyQt6.QtCore import * 

import math

from styles import Styles

# Custom collapsable sidebar widget. Uses paintEvent to draw rounded corners, and a callback for the collapse/expand animation.
class Sidebar(QWidget):
    def __init__(self, header_height = 64, blurRadius = 24, parent=None):
        super(Sidebar, self).__init__(parent)
        self._collapsed = False
        self._widthAnimation = QPropertyAnimation(self, b"maximumWidth", self)
        self._widthAnimation.setDuration(250)
        self._widthAnimation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self._widthAnimation.setStartValue(Styles.theme.min_sidebar_width)
        self._widthAnimation.setEndValue(40)

        self.header_height = header_height

        self.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=blurRadius, xOffset=4, yOffset=0, color=QColor(0, 0, 0, 100)))

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        header_frame = QFrame()
        header_frame.setFixedHeight(self.header_height)

        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        header_frame.setLayout(header_layout)

        self.toggle_button = QPushButton("", clicked=self.toggle)
        self.toggle_button.resize(23, header_height)
        self.toggle_button.setIcon(QIcon("assets/collapse.png"))
        self.toggle_button.setIconSize(QSize(21, header_height))
        self.toggle_button.setStyleSheet(f"""
        QPushButton 
        {{ 
            border: 0px;
        }}
        """)
        self._button_pixmap = QtGui.QPixmap("assets/collapse.png")

        self._button_animation = QtCore.QVariantAnimation(
            self,
            startValue=0.0,
            endValue=-180.0,
            duration=200,
            valueChanged=self.on_button_animate
        )

        header_layout.addWidget(self.toggle_button)

        layout.addWidget(header_frame)

        # create main container for the sidebar
        self.main_container = QWidget()
        layout.addWidget(self.main_container)

        super().setLayout(layout)

        self.expand()

    def addWidget(self, widget):
        self.main_container.layout().addWidget(widget)

    def setLayout(self, a0: QLayout):
        self.main_container.setLayout(a0)

    def getLayout(self):
        return self.main_container.layout()

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
        painter.drawRoundedRect(self.rect(), Styles.theme.corner_radius, Styles.theme.corner_radius)
        painter.drawRect(QRectF(0, 0, Styles.theme.corner_radius, self.height())) # left corners are filled so they aren't rounded

        # header
        painter.setBrush(QBrush(Styles.theme.light_background_color))
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.header_height), Styles.theme.corner_radius, Styles.theme.corner_radius) 
        painter.drawRect(QRectF(0, 0, Styles.theme.corner_radius, self.header_height)) # left corners are filled so they aren't rounded
        painter.drawRect(QRectF(self.width() - Styles.theme.corner_radius, self.header_height-Styles.theme.corner_radius, Styles.theme.corner_radius, Styles.theme.corner_radius)) # bottom right corner is filled so it isn't rounded

    def collapse(self):
        self._widthAnimation.setDirection(QPropertyAnimation.Direction.Forward)
        self._widthAnimation.start()
        self._button_animation.setDirection(QPropertyAnimation.Direction.Forward)
        self._button_animation.start()
        self.main_container.setVisible(False)

    def expand(self):
        self._widthAnimation.setDirection(QPropertyAnimation.Direction.Backward)
        self._widthAnimation.start()
        self._button_animation.setDirection(QPropertyAnimation.Direction.Backward)
        self._button_animation.start()
        self.main_container.setVisible(True)

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
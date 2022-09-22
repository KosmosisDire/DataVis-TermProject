import random
from time import time
from typing import List, Tuple
from PyQt6.QtWidgets import * 
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import * 
from PyQt6.QtCore import *
from data_handler import DataHandler
from global_settings import GlobalSettings
import datetime, pytz

from styles import Styles
from widgets.time_range_picker import TimeRangeChangedEvent


class ThemedPlot(QWidget):
    def __init__(self, title: str, column_name: str, parent: QWidget = None):
        super().__init__(parent)
        self.title = title
        self.column_name = column_name

        self.data: List[float] = []
        self.timestamps: List[int] = []

        self.painter_path: QPainterPath = None

        self.time_range = GlobalSettings.time_range
        self.aggregation = GlobalSettings.aggregation_seconds
        self.local_time = GlobalSettings.local_time

        GlobalSettings.instance.time_range_changed.connect(self.update_data)
        GlobalSettings.instance.aggregation_changed.connect(self.update_plot)
        GlobalSettings.instance.local_time_changed.connect(self.update_plot)

        self.setStyleSheet(f"""
            background-color: {Styles.theme.dark_background_color_hex};
            border-radius: {Styles.theme.corner_radius}px;
        """)

        self.update_data()

    def width(self) -> int:
        return super().width() - self.contentsMargins().left() - self.contentsMargins().right()

    def height(self) -> int:
        return super().height() - self.contentsMargins().top() - self.contentsMargins().bottom()

    def left(self) -> int:
        return self.contentsMargins().left()
    
    def right(self) -> int:
        return self.width() + self.contentsMargins().left()

    def right_margin(self) -> int:
        return self.contentsMargins().right()
    
    def top(self) -> int:
        return self.contentsMargins().top()

    def bottom(self) -> int:
        return self.height() + self.contentsMargins().top()
    
    def bottom_margin(self) -> int:
        return self.contentsMargins().bottom()

    def update_data(self):
        print("updating data")
        self.data = DataHandler.get(*GlobalSettings.time_range, self.column_name)
        self.timestamps = DataHandler.get(*GlobalSettings.time_range, "Unix Timestamp (UTC)")
        self.timestamps = [timestamp // 1000 for timestamp in self.timestamps]
        self.update_plot()

    def update_plot(self):
        if(len(self.data) == 0):
            self.update()
            return

        max_value: float = max(self.data)

        self.painter_path = QPainterPath()
        self.painter_path.moveTo(self.left(), self.bottom())

        last_timestamp: int = self.timestamps[0]

        avg: int = 0
        counter: int = 0
        i: int = 0
        for value in self.data:
            timestamp: int = self.timestamps[i]

            x_pos = int((self.width() * (float(i) / len(self.data)))) + self.left()
            y_pos = int(self.height() * (1 - value / max_value)) + self.top()
            avg += y_pos

            counter += 1
            i += 1
            if timestamp - last_timestamp >= GlobalSettings.aggregation_seconds:
                avg /= counter
                self.painter_path.lineTo(x_pos, avg)
                avg = 0
                counter = 0
                last_timestamp = timestamp

        self.update()

    def check_for_settings_change(self):
        if self.time_range != GlobalSettings.time_range:
            self.time_range = GlobalSettings.time_range
            self.update_data()

        if self.aggregation != GlobalSettings.aggregation_seconds or self.local_time != GlobalSettings.local_time:
            self.time_range = GlobalSettings.time_range
            self.aggregation = GlobalSettings.aggregation_seconds
            self.local_time = GlobalSettings.local_time
            self.update_plot()
        
    def paintEvent(self, event: QPaintEvent):

        self.check_for_settings_change()

        if len(self.data) == 0:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # paint plot
        painter.setBrush(QBrush(QColor("transparent")))
        painter.setPen(QPen(QColor(Styles.theme.data_colors_hex[0]), 1, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))

        painter.drawPath(self.painter_path)

    def resizeEvent(self, event: QResizeEvent):
        if len(self.data) > 0:
            self.update_plot()
        QWidget.resizeEvent(self, event)

        
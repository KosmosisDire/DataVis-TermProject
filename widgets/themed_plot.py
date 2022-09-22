import math
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

        GlobalSettings.instance.time_range_changed.connect(self.update_data)
        GlobalSettings.instance.aggregation_changed.connect(self.update_data)
        GlobalSettings.instance.local_time_changed.connect(self.update_plot)

        self.setStyleSheet(f"""
            background-color: {Styles.theme.dark_background_color_hex};
            border-radius: {Styles.theme.corner_radius}px;
        """)

        self.color = random.choice(Styles.theme.data_colors_hex)

        self.max_value: float = 0
        self.min_value: float = 0

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

    def round_down_to_nearest(self, value: int, nearest: int) -> int:
        return math.floor(value / nearest) * nearest

    def round_up_to_nearest(self, value: int, nearest: int) -> int:
        return math.ceil(value / nearest) * nearest

    def update_data(self):
        rounded_time_range = (self.round_down_to_nearest(GlobalSettings.time_range[0], GlobalSettings.aggregation_seconds * 100), self.round_up_to_nearest(GlobalSettings.time_range[1], GlobalSettings.aggregation_seconds * 100))
        self.data = DataHandler.get(*rounded_time_range, self.column_name)
        self.timestamps = DataHandler.get(*rounded_time_range, "Unix Timestamp (UTC)")
        self.timestamps = [timestamp // 1000 for timestamp in self.timestamps]
        self.update_plot()


    def timestamp_to_x(self, timestamp: int) -> int:
        return int(self.width() * (timestamp - GlobalSettings.time_range[0]) / (GlobalSettings.time_range[1] - GlobalSettings.time_range[0])) + self.left()

    def value_to_y(self, value:float, max_value:float, min_value:float) -> int:
        return int(self.height() * (1 - (value - min_value) / (max_value - min_value))) + self.top()


    def update_plot(self):
        
        if(len(self.data) == 0):
            self.update()
            return

        self.painter_path = QPainterPath()

        if self.max_value == 0:
            self.max_value = max(self.data)
            self.min_value = min(self.data)

        self.max_value = (max(self.data) * 1.01 + self.max_value) / 2 # smooth out jumps in the min and max values
        self.min_value = (min(self.data) * 0.99  + self.min_value) / 2 # smooth out jumps in the min and max values

        # move path to the first point
        self.painter_path.moveTo(self.timestamp_to_x(self.timestamps[0]), self.value_to_y(self.data[0], self.max_value, self.min_value))

        y_avg: int = 0
        x_avg: int = 0
        counter: int = 0
        for i in range(1, len(self.data)):
            timestamp: int = self.timestamps[i]
            value: float = self.data[i]

            x_pos = self.timestamp_to_x(timestamp)
            y_pos = self.value_to_y(value, self.max_value, self.min_value)
            
            y_avg += y_pos
            x_avg += x_pos

            counter += 1
            if timestamp % GlobalSettings.aggregation_seconds == 0:
                y_avg /= counter
                x_avg /= counter
                self.painter_path.lineTo(x_avg, y_avg)
                y_avg = 0
                x_avg = 0
                counter = 0

        self.update()
        
    def paintEvent(self, event: QPaintEvent):

        if len(self.data) == 0:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # paint plot
        painter.setBrush(QBrush(QColor("transparent")))
        painter.setPen(QPen(QColor(self.color), 2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))

        painter.drawPath(self.painter_path)

    def resizeEvent(self, event: QResizeEvent):
        if len(self.data) > 0:
            self.update_plot()
        QWidget.resizeEvent(self, event)

        
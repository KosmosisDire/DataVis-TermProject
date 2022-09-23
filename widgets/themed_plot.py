import math
import random
from time import time
from typing import List, Tuple
from venv import create
from PyQt6.QtWidgets import * 
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import * 
from PyQt6.QtCore import *
from data_handler import DataHandler
from global_settings import GlobalSettings
import datetime, pytz

from styles import Styles
from widgets.custom_widget import CustomWidget
from widgets.time_range_picker import TimeRangeChangedEvent


class ThemedPlot(CustomWidget):
    def __init__(self, title: str, column_name: str, height: int = 100, max_horizontal_marker_count = 10, max_vertical_marker_count = 5, horizonatal_marker_interval = 10000, vertical_marker_interval = 1):
        super().__init__()
        self.title = title
        self.column_name = column_name

        self.data: List[float] = []
        self.timestamps: List[int] = []

        self.final_data: List[float] = []
        self.final_timestamps: List[int] = []

        self.painter_path: QPainterPath = None

        GlobalSettings.instance.time_range_changed.connect(self.create_plot_path)
        GlobalSettings.instance.aggregation_changed.connect(self.regenerate_plot)
        GlobalSettings.instance.moving_average_seconds_changed.connect(self.regenerate_plot)
        GlobalSettings.instance.local_time_changed.connect(self.update)
        GlobalSettings.instance.use_angle_aggregation_changed.connect(self.regenerate_plot)

        self.time_range_last = GlobalSettings.time_range
        self.aggregation_last = GlobalSettings.aggregation_seconds
        self.local_time_last = GlobalSettings.local_time

        self.color = random.choice(Styles.theme.data_colors_hex)

        self.max_value: float = 0
        self.min_value: float = 0

        self.setContentsMargins(Styles.theme.large_spacing, 0, Styles.theme.close_spacing, Styles.theme.medium_spacing)

        self.setFixedHeight(height + self.top() + self.bottom_margin())
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)

        self.max_horizontal_marker_count = max_horizontal_marker_count
        self.max_vertical_marker_count = max_vertical_marker_count
        self.horizonatal_marker_interval = horizonatal_marker_interval
        self.vertical_marker_interval = vertical_marker_interval

        self.vertical_markers: List[str] = []
        self.horizontal_markers: List[str] = []

        self.update_data()

    def update_data(self):
        time_range = DataHandler.get_time_range() 
        self.data = DataHandler.get(*time_range, self.column_name)
        self.timestamps = DataHandler.get(*time_range, "Unix Timestamp (UTC)")
        self.timestamps = [timestamp // 1000 for timestamp in self.timestamps]
        self.regenerate_plot()

    def regenerate_plot(self):
        if(len(self.data) == 0):
            self.update()
            return

        if(self.min_value == 0 and self.max_value == 0):
            self.max_value = max(self.data)
            self.min_value = min(self.data)
        
        moving_avg_pass_data = []
        moving_avg_pass_timestamps = []

        if (GlobalSettings.moving_average_seconds > DataHandler.get_time_interval()):
            y_avg: int = self.data[0]
            avg_num = GlobalSettings.moving_average_seconds / DataHandler.get_time_interval()
            for i in range(1, len(self.data)):
                timestamp: int = self.timestamps[i]
                value: float = self.data[i]

                y_avg = 0
                c = 0
                for j in range(math.floor(-avg_num/2), math.ceil(avg_num/2)):
                    if(i+j >= 0 and i+j < len(self.data)):
                        y_avg += self.data[i+j]
                        c += 1
                y_avg /= c

                moving_avg_pass_data.append(y_avg)
                moving_avg_pass_timestamps.append(timestamp)
        else:
            moving_avg_pass_data = self.data
            moving_avg_pass_timestamps = self.timestamps
        
        aggregation_pass_data = []
        aggregation_pass_timestamps = []

        y_avg: int = 0
        x_avg: int = 0
        counter: float = 0.0
        for i in range(0, len(moving_avg_pass_data)):
            timestamp: int = moving_avg_pass_timestamps[i]
            value: float = moving_avg_pass_data[i]

            x_avg += timestamp
            y_avg += value

            counter += 1.0
            if timestamp % GlobalSettings.aggregation_seconds <= DataHandler.get_time_interval():
                y_avg /= counter
                x_avg /= counter
                aggregation_pass_data.append(y_avg)
                aggregation_pass_timestamps.append(x_avg)
                y_avg = 0
                x_avg = 0
                counter = 0.0

        if not GlobalSettings.use_angle_aggregation:
            self.final_data = aggregation_pass_data
            self.final_timestamps = aggregation_pass_timestamps
            self.create_plot_path()
            return

        self.final_data = []
        self.final_timestamps = []
        
        # initialize first line
        last_point = (aggregation_pass_timestamps[0], aggregation_pass_data[0])
        this_point = (aggregation_pass_timestamps[1], aggregation_pass_data[1])
        last_slope = float(this_point[1] - last_point[1]) / (float(this_point[0] - last_point[0]) / 10000.0)
        self.final_data.append(last_point[1])
        self.final_timestamps.append(last_point[0])
        self.final_data.append(this_point[1])
        self.final_timestamps.append(this_point[0])
        last_point = this_point

        # process the rest of the data
        data_len = len(aggregation_pass_data)
        for i in range(2, data_len):

            value = aggregation_pass_data[i]
            timestamp = aggregation_pass_timestamps[i]

            slope = float(value - last_point[1]) / (float(timestamp - last_point[0]) / 10000.0)
            angle = abs(math.degrees(math.atan((slope - last_slope) / (1 + slope * last_slope))))
            last_slope = slope
            
            if angle < 5 and i != data_len-1:
                continue
            
            self.final_timestamps.append(last_point[0])
            self.final_data.append(last_point[1])

            last_point = (float(timestamp), float(value))

        self.create_plot_path()

    def create_plot_path(self):
        if(GlobalSettings.isVisibleWidget(self) == False):
            return

        self.painter_path = QPainterPath()
        self.painter_path.moveTo(self.timestamp_to_x(self.final_timestamps[0]), self.value_to_y(self.final_data[0], self.max_value, self.min_value))

        max_val_local = self.final_data[0]
        min_val_local = self.final_data[0]
        for i in range(1, len(self.final_data)):
            timestamp: int = self.timestamp_to_x(self.final_timestamps[i])
            value: float = self.value_to_y(self.final_data[i], self.max_value, self.min_value)

            if self.is_timestamp_out_of_range(self.final_timestamps[i]):
                self.painter_path.moveTo(timestamp, value)
                continue
                
            max_val_local = max(max_val_local, self.final_data[i] * 1.01)
            min_val_local = min(min_val_local, self.final_data[i] * 0.99)

            
            self.painter_path.lineTo(timestamp, value)

        self.max_value = (self.max_value + max_val_local) / 2
        self.min_value = (self.min_value + min_val_local) / 2
        
        self.update()

    def paintEvent(self, event: QPaintEvent):

        if len(self.final_data) == 0 or not self.painter_path:
            return


        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.setBrush(QBrush(Styles.theme.dark_background_color))
        painter.setPen(QPen(QColor("transparent")))
        painter.drawRoundedRect(self.rect(), Styles.theme.corner_radius, Styles.theme.corner_radius)

        # paint plot
        painter.setBrush(QBrush(QColor("transparent")))
        painter.setClipRect(self.rect())
        painter.setPen(QPen(QColor(self.color), 1, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))

        painter.drawPath(self.painter_path)

    def timestamp_to_x(self, timestamp: int) -> int:
        return int(self.width() * (timestamp - GlobalSettings.time_range[0]) / (GlobalSettings.time_range[1] - GlobalSettings.time_range[0])) + self.left()

    def value_to_y(self, value:float, max_value:float, min_value:float) -> int:
        return int(self.height() * (1 - (value - min_value) / max(max_value - min_value, 0.001))) + self.top()

    def is_timestamp_out_of_range(self, timestamp: int) -> bool:
        return timestamp - GlobalSettings.time_range[0] < -GlobalSettings.aggregation_seconds * 10 or timestamp - GlobalSettings.time_range[1] > GlobalSettings.aggregation_seconds * 10

    def resizeEvent(self, event: QResizeEvent):
        if len(self.data) > 0:
            self.create_plot_path()
        QWidget.resizeEvent(self, event)

        
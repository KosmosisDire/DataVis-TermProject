import datetime
from functools import partial
import math
import random
import time
from typing import List, Tuple
from PyQt6.QtWidgets import * 
from PyQt6 import *
from PyQt6.QtGui import * 
from PyQt6.QtCore import *
from data_handler import DataHandler
import asyncio

from styles import Styles
from widgets.custom_widget import CustomWidget

import numpy as np

from widgets.time_range_picker import clamp

def binarySearch(data, val):
    lo, hi = 0, len(data) - 1
    best_ind = lo
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if data[mid] < val:
            lo = mid + 1
        elif data[mid] > val:
            hi = mid - 1
        else:
            best_ind = mid
            break
        # check if data[mid] is closer to val than data[best_ind] 
        if abs(data[mid] - val) < abs(data[best_ind] - val):
            best_ind = mid
    return best_ind


class ThemedPlot(CustomWidget):
    def __init__(self, height: int = 80, max_horizontal_marker_count = 10, max_vertical_marker_count = 5, horizonatal_marker_interval = 10000, vertical_marker_interval = 1):
        super().__init__()

        self.time_range: Tuple[int, int] = (0, 0)

        self.data: List[float] = []
        self.timestamps: List[int] = []

        self.moving_avg = 1
        self.moving_avg_data = []
        self.moving_avg_timestamps = []

        self.aggregation_interval = 1
        self.aggregated_data = []
        self.aggregated_timestamps = []

        self.final_data: List[float] = []
        self.final_timestamps: List[int] = []

        self.painter_path: QPainterPath = None
        self.number_path: QPainterPath = None

        self.color = random.choice(Styles.theme.data_colors_hex)

        self.max_value: float = 0
        self.min_value: float = 0

        self.setContentsMargins(Styles.theme.large_spacing, Styles.theme.close_spacing, Styles.theme.medium_spacing, Styles.theme.medium_spacing)

        self.set_height(height)
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)

        self.max_horizontal_marker_count = max_horizontal_marker_count
        self.max_vertical_marker_count = max_vertical_marker_count
        self.horizontal_marker_interval = horizonatal_marker_interval
        self.vertical_marker_interval = vertical_marker_interval

        self.vertical_markers: List[str] = []
        self.horizontal_markers: List[str] = []

    def plot(self, X: List[float], Y: List[float]):
        self.data = Y
        self.timestamps = X

        if(self.min_value == 0 and self.max_value == 0):
            self.max_value = max(self.data)
            self.min_value = min(self.data)

        self.set_moving_average(self.moving_avg)

    def plot(self, Y: List[float]):
        self.data = Y
        self.timestamps = DataHandler.get_timestamps()

        if(self.min_value == 0 and self.max_value == 0):
            self.max_value = max(self.data)
            self.min_value = min(self.data)

        self.set_moving_average(self.moving_avg)

    def set_moving_average(self, window_seconds: int):
        self.moving_avg = window_seconds
        if len(self.data) == 0: return

        if (self.moving_avg < DataHandler.get_time_interval()):
            self.moving_avg_data = self.data
            self.moving_avg_timestamps = self.timestamps
            self.set_aggregation_interval(self.aggregation_interval)
            return

        self.moving_avg_data: List[float] = []
        self.moving_avg_timestamps = self.timestamps

        window_size = int(self.moving_avg / DataHandler.get_time_interval()) + 1

        npdata: np.ndarray = np.array(self.data)
        npdatalen = npdata.shape[0]
        
        y_sum: float = npdata[0]
        count = 0
        for i in range(1, npdatalen):
            y_sum += npdata[i]
            
            if i >= window_size:
                y_sum -= npdata[i - window_size]
                count = window_size
            else:
                count += 1

            self.moving_avg_data.append(y_sum / count)

        self.set_aggregation_interval(self.aggregation_interval)

    def set_aggregation_interval(self, interval_seconds: int):
        self.aggregation_interval = max(interval_seconds, 1)

        if len(self.moving_avg_data) == 0: return

        self.final_data = []
        self.final_timestamps = []

        self.max_value = self.moving_avg_data[0]
        self.min_value = self.moving_avg_data[-1]

        y_avg: float = 0
        x_avg: int = 0
        counter: float = 0.0
        data_len = len(self.moving_avg_data)
        for i in range(0, data_len):
            timestamp: int = self.moving_avg_timestamps[i]
            value: float = self.moving_avg_data[i]

            x_avg += timestamp
            y_avg += value

            if not self.is_timestamp_out_of_range(timestamp):
                self.max_value = max(self.max_value, value)
                self.min_value = min(self.min_value, value)

            counter += 1.0
            if timestamp % self.aggregation_interval <= DataHandler.get_time_interval():
                y_avg /= counter
                x_avg /= counter
                self.final_data.append(y_avg)
                self.final_timestamps.append(x_avg)
                y_avg = 0
                x_avg = 0
                counter = 0.0

        self.render_plot()
    
    def render_plot(self):
        if len(self.final_data) == 0: return
        if not self.is_on_screen(): return
        
        start = time.perf_counter_ns()
        
        start_range_estimation = max(binarySearch(self.final_timestamps, self.time_range[0]) - 1, 0)
        end_range_estimation = min(binarySearch(self.final_timestamps, self.time_range[1]) + 1, len(self.final_timestamps)-1)

        initial_pos = QPointF(self.timestamp_to_x(self.final_timestamps[start_range_estimation]), self.value_to_y(self.final_data[start_range_estimation], self.max_value, self.min_value))
        start_range_estimation += 1

        self.painter_path = QPainterPath()
        self.painter_path.moveTo(initial_pos + QPointF(0, self.height()))
        self.painter_path.lineTo(initial_pos)
        
        max_val_local = self.final_data[start_range_estimation]
        min_val_local = self.final_data[start_range_estimation]

        for i in range(start_range_estimation, end_range_estimation):
            timestamp: int = self.timestamp_to_x(self.final_timestamps[i])
            value: float = self.value_to_y(self.final_data[i], self.max_value, self.min_value)
                
            max_val_local = max(max_val_local, self.final_data[i] * 1.01)
            min_val_local = min(min_val_local, self.final_data[i] * 0.99)
            
            self.painter_path.lineTo(timestamp, value)

        self.painter_path.lineTo(self.painter_path.currentPosition() + QPointF(0, self.height()))

        self.max_value = (self.max_value + max_val_local) / 2
        self.min_value = (self.min_value + min_val_local) / 2

        #self.painter_path = self.painter_path.simplified()

        self.generate_markers()

    def generate_markers(self):
        def round_down_to_nearest(x: float, a: float):
            return math.floor(x / a) * a

        self.number_path = QPainterPath()

        normal_range_y = self.max_value - self.min_value
        normal_range_x = self.time_range[1] - self.time_range[0]

        num_y_markers = min(int(normal_range_y / self.vertical_marker_interval), self.max_vertical_marker_count) + 1
        num_x_markers = min(int(normal_range_x / self.horizontal_marker_interval), self.max_horizontal_marker_count) + 1

        last_number = math.inf
        for i in range(0, self.max_vertical_marker_count):
            value = round_down_to_nearest(self.min_value + normal_range_y * (i / self.max_vertical_marker_count), self.vertical_marker_interval)
            if value == last_number: continue
            self.number_path.addText(-28, self.bottom() - (i/self.max_vertical_marker_count) * self.height(), QFont(Styles.theme.font_family, 8), f"{value:>6.2g}")
            last_number = value
        
        last_number = math.inf
        for i in range(0, self.max_horizontal_marker_count):
            value = round_down_to_nearest(self.time_range[0] + normal_range_x * (i / self.max_horizontal_marker_count), self.horizontal_marker_interval)
            if value == last_number: continue
            self.number_path.addText((i/self.max_horizontal_marker_count) * self.width(), self.bottom() + 11, QFont(Styles.theme.font_family, 8), datetime.datetime.fromtimestamp(value).strftime("%H:%M:%S"))
            last_number = value
        

        self.update()

    def paintEvent(self, event: QPaintEvent):

        if len(self.final_data) == 0 or not self.painter_path:
            return

        start = time.perf_counter_ns()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.setBrush(QBrush(Styles.theme.dark_background_color))
        painter.setPen(QPen(Styles.theme.mid_background_color.darker(180), 1))
        painter.drawRoundedRect(self.rect(), Styles.theme.panel_radius, Styles.theme.panel_radius)

        # shadow
        painter.setBrush(QBrush(QColor("transparent")))
        painter.setPen(QPen(Styles.theme.mid_background_color.darker(170), 2))
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), Styles.theme.panel_radius, Styles.theme.panel_radius)

        painter.setPen(QPen(Styles.theme.mid_background_color.darker(160), 3))
        painter.drawRoundedRect(self.rect().adjusted(3, 3, -3, -3), Styles.theme.panel_radius, Styles.theme.panel_radius)

        painter.setPen(QPen(Styles.theme.mid_background_color.darker(150), 4))
        painter.drawRoundedRect(self.rect().adjusted(6, 6, -6, -6), Styles.theme.panel_radius, Styles.theme.panel_radius)

        # paint plot
        painter.setBrush(QBrush(QColor("transparent")))
        painter.setClipRect(self.rect())
        painter.setPen(QPen(QColor(self.color), 1, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))

        painter.translate(self.left(), 0)
        painter.drawPath(self.painter_path.translated(-self.left(), 0))

        # paint markers
        painter.setClipping(False)
        painter.setPen(QPen(QColor("transparent")))
        painter.setBrush(QBrush(Styles.theme.label_color))
        painter.drawPath(self.number_path)

        end = time.perf_counter_ns()

    def timestamp_to_x(self, timestamp: int) -> int:
        return int(self.width() * (timestamp - self.time_range[0]) / max(self.time_range[1] - self.time_range[0], 0.001)) + self.left() 

    def value_to_y(self, value:float, max_value:float, min_value:float) -> int:
        return int(self.height() * (1 - (value - min_value) / max(max_value - min_value, 0.001))) + self.top()

    def is_timestamp_out_of_range(self, timestamp: int) -> bool:
        return timestamp - self.time_range[0] < - self.aggregation_interval * 10 or timestamp - self.time_range[1] > self.aggregation_interval * 10

    def erase(self):
        self.data = []
        self.moving_avg_data = []
        self.moving_avg_timestamps = []
        self.final_data = []
        self.final_timestamps = []
        self.painter_path = None
        self.update()

    def set_height(self, height: int):
        self.setFixedHeight(height + self.top() + self.bottom_margin())
        self.render_plot()

    def set_markers(self, max_horizontal: int, max_vertical: int, horizontal_interval: int, vertical_interval: int):
        self.max_horizontal_marker_count = max_horizontal
        self.max_vertical_marker_count = max_vertical
        self.horizontal_marker_interval = horizontal_interval
        self.vertical_marker_interval = vertical_interval
        self.render_plot()

    def set_time_range(self, lower_utc_timestamp: int, upper_utc_timestamp: int):
        self.time_range = (lower_utc_timestamp, upper_utc_timestamp)
        self.render_plot()

        
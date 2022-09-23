from ast import Global
from typing import List, Tuple
from PyQt6.QtCore import pyqtSignal, QObject
from widgets.time_range_picker import TimeRangeChangedEvent


class GlobalSettings(QObject):
    time_range: Tuple[int, int] = (0, 0)
    aggregation_seconds: int = 0
    moving_average_seconds: int = 0
    local_time: bool = False
    use_angle_aggregation: bool = False

    time_range_changed: pyqtSignal = pyqtSignal()
    aggregation_changed: pyqtSignal = pyqtSignal()
    moving_average_seconds_changed: pyqtSignal = pyqtSignal()
    local_time_changed: pyqtSignal = pyqtSignal()
    use_angle_aggregation_changed: pyqtSignal = pyqtSignal()
    instance = None

    def __init__(self):
        super().__init__()
        GlobalSettings.instance = self # singleton, seems to be the only way to emit signals from static methods

    def emit_time_range_changed(self, event: TimeRangeChangedEvent):
        self.time_range_changed.emit()

    def emit_aggregation_changed(self, seconds: int):
        self.aggregation_changed.emit()

    def emit_moving_average_seconds_changed(self, seconds: int):
        self.moving_average_seconds_changed.emit()
    
    def emit_local_time_changed(self, local_time: bool):
        self.local_time_changed.emit()

    def emit_use_angle_aggregation_changed(self, use_angle_aggregation: bool):
        self.use_angle_aggregation_changed.emit()

    def time_range_changed_callback(event: TimeRangeChangedEvent):
        GlobalSettings.time_range = (event.start_time_seconds, event.end_time_seconds)
        GlobalSettings.instance.emit_time_range_changed(GlobalSettings.time_range)

    def aggregation_changed_callback(choice: str):
        seconds = 60
        match(choice):
            case "30 Seconds": seconds = 30
            case "1 Minute": seconds = 60
            case "2 Minutes": seconds = 120
            case "4 Minutes": seconds = 240
            case "5 Minutes": seconds = 300
            case "10 Minutes": seconds = 600
            case "15 Minutes": seconds = 900
            case "30 Minutes": seconds = 1800
            case "1 Hour": seconds = 3600
            case _: seconds = 60

        GlobalSettings.aggregation_seconds = seconds

        GlobalSettings.instance.emit_aggregation_changed(seconds)

    def moving_average_seconds_changed_callback(choice: str):
        seconds = 0
        match(choice):
            case "None": seconds = 0
            case "30 Seconds": seconds = 30
            case "1 Minute": seconds = 60
            case "2 Minutes": seconds = 120
            case "4 Minutes": seconds = 240
            case "5 Minutes": seconds = 300
            case "10 Minutes": seconds = 600
            case "15 Minutes": seconds = 900
            case "30 Minutes": seconds = 1800
            case "1 Hour": seconds = 3600
            case _: seconds = 0

        GlobalSettings.moving_average_seconds = seconds

        GlobalSettings.instance.emit_moving_average_seconds_changed(seconds)

    def local_time_changed_callback(local_time: bool):
        GlobalSettings.local_time = local_time
        GlobalSettings.instance.emit_local_time_changed(local_time)

    def use_angle_aggregation_changed_callback(use_angle_aggregation: bool):
        GlobalSettings.use_angle_aggregation = use_angle_aggregation
        GlobalSettings.instance.emit_use_angle_aggregation_changed(use_angle_aggregation)

    def isVisibleWidget(widget):
        if not widget.visibleRegion().isEmpty():
            return True
        return False

GlobalSettings()
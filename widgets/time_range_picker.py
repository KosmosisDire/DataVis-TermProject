from datetime import datetime
from typing import Any, Callable, Tuple
from PyQt6.QtWidgets import * 
from PyQt6 import *
from PyQt6.QtGui import * 
from PyQt6.QtCore import * 

from styles import Styles
from widgets.custom_widget import CustomWidget



def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)

# this widget has two sliders which collider with eachother and are dragged by the mouse. Used to select a time window.
class TimeRangePicker(CustomWidget):
    def __init__(self, height: int, valueChanged: Callable[[Tuple[int, int]], Any] = None, push_behavior: bool = True):
        super().__init__()

        self.right_bubble: QPixmap = QPixmap("assets/right_bubble.png")
        self.left_bubble: QPixmap = QPixmap("assets/left_bubble.png")

        self.setContentsMargins(Styles.theme.close_spacing + 100, Styles.theme.close_spacing, Styles.theme.close_spacing + 100, Styles.theme.close_spacing)
        self.setMinimumWidth(640)
        self.setFixedHeight(height + self.top() + self.contentsMargins().bottom())

        self.min_time: int = 0
        self.max_time: int = 1
        self.valueChanged: Callable[[Tuple[int, int]], Any] = valueChanged
        self.start_time: int = self.min_time
        self.end_time: int = self.max_time
        self.push_behavior: bool = push_behavior

        self._start_rect: QRect = QRect(0, 0, 0, 0)
        self._end_rect: QRect = QRect(0, 0, 0, 0)
        self._middle_rect: QRect = QRect(0, 0, 0, 0)

        self._mouse_x_delta: int = 0
        self._mouse_x_last: int = 0
        self._dragging_start: bool = False
        self._dragging_end: bool = False

        self.handle_radius = Styles.theme.control_radius
        self.handle_width = Styles.theme.slider_handle_width

        self.display_data: list = []
        self.painter_path: QPainterPath = QPainterPath()

        self._last_start_time = self.start_time
        self._last_end_time = self.end_time

    def paintEvent(self, event: QPaintEvent):
        self._update_handles()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(Qt.GlobalColor.transparent))

        #draw background
        painter.setBrush(QBrush(Styles.theme.dark_background_color))
        draw_rect = QRect(self.left(), self.top(), self.width(), self.height())
        painter.drawRoundedRect(draw_rect, Styles.theme.control_radius, Styles.theme.control_radius, Qt.SizeMode.AbsoluteSize)

        if len(self.display_data) > 0:
            #draw data path
            painter.setBrush(QBrush(QColor("transparent")))
            painter.setPen(QPen(QColor("white"), 1, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
            painter.drawPath(self.painter_path) 

            # draw time label bubbles
            bubble_x_offset = 5
            bubble_y_offset = -21
            painter.drawPixmap(self._start_rect.left() - self.left_bubble.width() + bubble_x_offset, self.bottom() + bubble_y_offset, self.left_bubble)
            painter.drawPixmap(self._end_rect.right() - bubble_x_offset, self.bottom() + bubble_y_offset, self.right_bubble)

            # draw time labels
            painter.setPen(QPen(Styles.theme.label_color, 1, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
            painter.setFont(QFont("Segoe UI", 8))
            painter.drawText(self._start_rect.left() - self.left_bubble.width() - bubble_x_offset-2, self.bottom() + bubble_y_offset + 6, self.left_bubble.width(), self.left_bubble.height(), Qt.AlignmentFlag.AlignRight, datetime.fromtimestamp(self.start_time).strftime("%b %d, %H:%M"))
            painter.drawText(self._end_rect.right() + bubble_x_offset + 2, self.bottom() + bubble_y_offset + 6, self.right_bubble.width(), self.right_bubble.height(), Qt.AlignmentFlag.AlignLeft, datetime.fromtimestamp(self.end_time).strftime("%b %d, %H:%M"))

        #draw shroud
        painter.setBrush(QBrush(Styles.theme.shroud_color))
        painter.setPen(QPen(Qt.GlobalColor.transparent))
        painter.setOpacity(Styles.theme.shroud_opacity)
        left_shroud = QRect(self.left(), self.top(), self._start_rect.right() - self.left(), self.height())
        right_shroud = QRect(self._end_rect.right(), self.top(), self.width() - self._end_rect.right() + self.left(), self.height())
        painter.drawRoundedRect(left_shroud, Styles.theme.control_radius, Styles.theme.control_radius, Qt.SizeMode.AbsoluteSize)
        painter.drawRoundedRect(right_shroud, Styles.theme.control_radius, Styles.theme.control_radius, Qt.SizeMode.AbsoluteSize)

        # draw handles
        painter.setBrush(QBrush(Styles.theme.label_color))
        painter.setOpacity(1)
        painter.drawRoundedRect(self._start_rect, self.handle_radius, self.handle_radius)
        painter.drawRoundedRect(self._end_rect, self.handle_radius, self.handle_radius)

        # fill in inside corners
        painter.drawRect(QRectF(self._start_rect.x() + self._start_rect.width() - self.handle_radius, self.top(), self.handle_radius, self._start_rect.height())) 
        painter.drawRect(QRectF(self._end_rect.x(), self.top(), self.handle_radius, self._end_rect.height()))

        if self._last_start_time != self.start_time or self._last_end_time != self.end_time:
            self._last_start_time = self.start_time
            self._last_end_time = self.end_time
            self.valueChanged((self.start_time, self.end_time))


    def value_to_y(self, value:float, max_value:float, min_value:float) -> int:
        return int(self.height() * (1 - (value - min_value) / (max_value - min_value))) + self.top()

    def set_plot_data(self, data: list):
        self.display_data = data

        max_value: float = max(self.display_data)
        min_value: float = min(self.display_data)

        self.painter_path = QPainterPath()
        self.painter_path.moveTo(self.left(), self.value_to_y(self.display_data[0], max_value, min_value))

        # divisor = max(int(min(len(self.display_data), 1000) / self.width() * 4), 2)
        divisor = 1

        y_avg: int = 0
        counter: int = 0
        for i in range(1, len(self.display_data)):
            value: float = self.display_data[i]

            x_pos = int(self.left() + i / len(self.display_data) * self.width())
            y_pos = self.value_to_y(value, max_value, min_value)
            
            y_avg += y_pos

            counter += 1
            if counter == divisor:
                y_avg /= counter
                self.painter_path.lineTo(x_pos, y_avg)
                y_avg = 0
                counter = 0

        self.update()

    def _update_handles(self):
        x_pos = int((self.width()) * (self.start_time - self.min_time) / (self.max_time - self.min_time))
        self._start_rect = QRect(x_pos + self.left() - self.handle_width, self.top(), self.handle_width, self.height())

        x_pos = int((self.width()) * (self.end_time - self.min_time) / (self.max_time - self.min_time))
        self._end_rect = QRect(x_pos + self.left(), self.top(), self.handle_width, self.height())

        self._middle_rect = QRect(self._start_rect.right(), self.top(), self._end_rect.left() - self._start_rect.right(), self.height())

    def set_start_value(self, seconds_since_epoch: int):
        self.start_time = seconds_since_epoch
        self.start_time = int(clamp(self.start_time, self.min_time, self.max_time))

        if self.push_behavior:
            if self.start_time > self.end_time:
                self.set_end_value(self.start_time)

        self.update()

    def set_end_value(self, seconds_since_epoch: int):
        self.end_time = seconds_since_epoch
        self.end_time = int(clamp(self.end_time, self.min_time, self.max_time))

        if self.push_behavior:
            if self.end_time < self.start_time:
                self.set_start_value(self.end_time)

        self.update()

    def move_start_by_pixels(self, pixels: int):
        self.set_start_value(self.start_time + pixels * (self.max_time - self.min_time) / self.width())

    def move_end_by_pixels(self, pixels: int): 
        self.set_end_value(self.end_time + pixels * (self.max_time - self.min_time) / self.width())



    def mousePressEvent(self, event: QMouseEvent) -> None:
        if self._start_rect.contains(event.pos()):
            self._dragging_start = True
            self._dragging_end = False
        elif self._end_rect.contains(event.pos()):
            self._dragging_end = True
            self._dragging_start = False
        elif self._middle_rect.contains(event.pos()):
            self._dragging_start = True
            self._dragging_end = True
        else:
            self._dragging_start = False
            self._dragging_end = False

        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self._mouse_x_last == 0:
            self._mouse_x_last = event.globalPosition().x()

        self._mouse_x_delta = event.globalPosition().x() - self._mouse_x_last
        self._mouse_x_last = event.globalPosition().x()

        if self._dragging_start:
            self.move_start_by_pixels(self._mouse_x_delta)
        
        if self._dragging_end:
            self.move_end_by_pixels(self._mouse_x_delta)
            
        # valueChanged is called from repaint, since thats the only time it matters

        self.update()
        
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self._mouse_x_last = 0
        self._mouse_x_delta = 0
            
        self._dragging_start = False
        self._dragging_end = False

        return super().mouseReleaseEvent(event)

    def resizeEvent(self, event: QResizeEvent):
        if len(self.display_data) > 0:
            self.set_plot_data(self.display_data)
        QWidget.resizeEvent(self, event)

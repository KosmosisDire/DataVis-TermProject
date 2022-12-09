

import asyncio
import time
from typing import List, Tuple
from widgets.themed_plot import ThemedPlot
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *



class PlotHandler:
    plots: List[ThemedPlot] = []

    time_range = (0, 0)
    plot_height = 80

    moving_average = 1
    aggregation_interval = 1

    max_horizontal_marker_count = 15
    max_vertical_marker_count = 10
    horizonatal_marker_interval = 5000
    vertical_marker_interval = 0.5

    def add_plot(plot: ThemedPlot):
        PlotHandler.plots.append(plot)
        plot.set_time_range(*PlotHandler.time_range)
        plot.set_height(PlotHandler.plot_height)
        plot.set_moving_average(PlotHandler.moving_average)
        plot.set_aggregation_interval(PlotHandler.aggregation_interval)
        plot.set_markers(PlotHandler.max_horizontal_marker_count, PlotHandler.max_vertical_marker_count, PlotHandler.horizonatal_marker_interval, PlotHandler.vertical_marker_interval)
        
    def add_plots(plots: List[ThemedPlot]):
        PlotHandler.plots.extend(plots)
        for plot in plots:
            plot.set_time_range(*PlotHandler.time_range)
            plot.set_height(PlotHandler.plot_height)
            plot.set_moving_average(PlotHandler.moving_average)
            plot.set_aggregation_interval(PlotHandler.aggregation_interval)
            plot.set_markers(PlotHandler.max_horizontal_marker_count, PlotHandler.max_vertical_marker_count, PlotHandler.horizonatal_marker_interval, PlotHandler.vertical_marker_interval)

    def remove_plot(plot: ThemedPlot):
        PlotHandler.plots.remove(plot)

    def remove_plot_at(index: int):
        PlotHandler.plots.pop(index)

    def get_plot(index: int) -> ThemedPlot:
        return PlotHandler.plots[index]

    def plot_count() -> int:
        return len(PlotHandler.plots)

    def clear_plots():
        PlotHandler.plots.clear()
    
    def erase_plots():
        for plot in PlotHandler.plots:
            plot.erase()

    def regenerate_plots():
        start = time.perf_counter_ns()

        for plot in PlotHandler.plots:
            plot.render_plot()

        print(f"Regenerated plots in {time.perf_counter_ns() - start} ns")

    def set_time_range(time_range: Tuple[int, int]):
        if time_range == PlotHandler.time_range or time_range[0] > time_range[1]:
            return
        
        start = time.perf_counter_ns()

        PlotHandler.time_range = time_range
        for plot in PlotHandler.plots:
            plot.set_time_range(*time_range)


        print(f"Set time range in {time.perf_counter_ns() - start} ns")

    def set_plot_height(height: int):
        if height == PlotHandler.plot_height or height < 1:
            return

        PlotHandler.plot_height = height
        for plot in PlotHandler.plots:
            plot.set_height(height)
    
    def set_aggregation_interval(interval: int):
        if interval == PlotHandler.aggregation_interval or interval < 1:
            return

        PlotHandler.aggregation_interval = interval
        for plot in PlotHandler.plots:
            plot.set_aggregation_interval(interval)

    def set_moving_average(moving_average: int):
        if moving_average == PlotHandler.moving_average or moving_average < 1:
            return

        PlotHandler.moving_average = moving_average
        for plot in PlotHandler.plots:
            plot.set_moving_average(moving_average)

    def set_markers(max_horizontal: int, max_vertical: int, horizontal_interval: int, vertical_interval: int):
        if (max_horizontal == PlotHandler.max_horizontal_marker_count and
            max_vertical == PlotHandler.max_vertical_marker_count and
            horizontal_interval == PlotHandler.horizonatal_marker_interval and
            vertical_interval == PlotHandler.vertical_marker_interval):
            return

        PlotHandler.max_horizontal_marker_count = max_horizontal
        PlotHandler.max_vertical_marker_count = max_vertical
        PlotHandler.horizonatal_marker_interval = horizontal_interval
        PlotHandler.vertical_marker_interval = vertical_interval
        for plot in PlotHandler.plots:
            plot.set_markers(max_horizontal, max_vertical, horizontal_interval, vertical_interval)


    

    

    
    

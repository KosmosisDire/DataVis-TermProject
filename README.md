# Data Vis Term Project

This project conains many custom widgets specific to this project.

## Libraries Needed
- [pyqt6](https://pypi.org/project/PyQt6/)
- [pandas](https://pypi.org/project/pandas/)


## Important Widgets:

### Time Range Picker
```python
TimeRangePicker(height: int, min_time: datetime, max_time: datetime, valueChanged: Callable[[TimeRangeChangedEvent], Any] = None, start_time: datetime = None, end_time: datetime = None, push_behavior: bool = True)
```
- height: how many pixels tall is the time box.
- min_time: what is the oldest date available to pick from (leftmost bound)
- max_time: what is the newest date available to pick from (rightmost bound)
- valueChanged: a function that will be called when the value is changed. The `TimeRangeChangedEvent` class tells what times were picked, and must be a parameter of the function.
- start_time: initial time for the left handle
- end_time: initial time for the right handle
- push_behavior: should the handles be able to push eachother around or do they just stop the other one from moving at all.

Important functions:
- `def set_plot_data(self, data: list):`
  - Given a list of numerical data, this function will show a preview of that data inside of the time box.

### Sidebar Widget
```
Sidebar(header_height = 64, blurRadius = 24, parent = None)
```python
A somewhat internally complicated class. Some important functions include:
- `def addWidget(self, widget):`
- `def collapse(self):`
- `def expand(self):`
- `def toggle(self):`

### Themed Plot
```python
ThemedPlot( title: str, column_name: str, parent: QWidget = None)
```
This is a very important class, and functions differently than pyqt's built-in plot.
- title: the name of the plot
- column_name: the name of the data to pull from the database. For example the "Temp avg" column.

The plot will automatically grab the data for that plot and update along with any changes to the time range or settings.

## Misc Themed Widgets:

### Themed Button
```python
ThemedButton(text: str, callback: callable, parent: QWidget = None)
```
Functions basically the same as a normal button but with easier access to the clicked event, and automatic theming

### Themed Dropdown
```python
ThemedDropdown(items: list, callback: Callable[[str], Any] = None, parent: QWidget = None)
```
Function basically the same as a normal dropdown box, but with automatic theming.

### Themed Radio Button
```python
ThemedRadioButton(callback: Callable[[bool], Any])
```
Simple radio button with custom checked and unchecked images.

### Labeled Control
```python
LabeledControl(label_text: string, widget: QWidget, parent = None)
```
This widget puts a label out in front of a widget. This is useful for things like radio buttons or dropdown boxes that need a label beside them.
The label text is themed automatically.

### Colored Text
```python
ColoredText(text: string, color: QColor, fontSize: int = 24, margins = (0, 0, 0, 0))
```
A simple text widget that can be colored and styles easily from the constructor

### Horizontal Seperator
```python
HorizontalSeperator(spacing: int, thickness: int = 1)
```
Basically just a horizontal line with space above and below it. The space, and line thickness are adjustable. The line's color is set by the styles.py theme

### Horizontal Group
```python
HorizontalGroup(widgets: list[QWidget], spacing: int, parent=None)
```
A simple widget that takes a list of other widgets to line up in a horizontal layout.

### Blank Widget:
```python
BlankWidget(color = "transparent", shadow_radius = 0, shadow_color = QColor(0, 0, 0, 0), shadow_offset = (0, 0)))
```
This is a very simple blank widget with a solid background. Can be used for panels or containers for other widgets.
- color: any string describing a color, usually hex, rgb, or a color name
- shadow_radius: the size of the drop shadow, none if set to 0

### Themed Scroll Area
```python
ThemedScrollArea(parent = None)
```
This basically works like the normal scroll area but it start without margins which is usually how you want a scroll area.

# Data Vis Term Project

![image](https://user-images.githubusercontent.com/39423700/192062305-b4223a4f-156d-44e7-8732-79ba7ce60b66.png)



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
```python
Sidebar(header_height = 64)
```
A somewhat internally complicated class. Some important functions include:
- `def addWidget(self, widget):`
- `def collapse(self):`
- `def expand(self):`
- `def toggle(self):`

### Themed Plot
```python
ThemedPlot( title: str, column_name: str)
```
This is a very important class, and functions differently than pyqt's built-in plot.
- title: the name of the plot
- column_name: the name of the data to pull from the database. For example the "Temp avg" column.

The plot will automatically grab the data for that plot and update along with any changes to the time range or settings.

## Misc Themed Widgets:

These are more general purpose widgets that follow the theme described in styles.py.
Most of these also have these functions:
```python
setShadow(self, blurRadius: int = Styles.theme.panel_shadow_radius, xOffset: int = 0, yOffset: int = 0, color: QtGui.QColor = Styles.theme.shadow_color):
# sets the object to have a drop shadow with the given parameters.

def fill(self, color: QColor | str):
# fills the background of the widget with this color.

def addWidget(self, widget) -> QWidget:
# adds a widget to the widgets layout, if the widget has no layout, create one.

def addWidgets(self, widgets: List[QWidget]):
# adds a list of widgets

def setLayout(self, layout: QLayout, spacing = 0, margins = (0, 0, 0, 0)):
sets the layout, as well as that layout's spacing, and margins.

```

### Themed Button
```python
ThemedButton(text: str, callback: callable)
```
Functions basically the same as a normal button but with easier access to the clicked event, and automatic theming

### Themed Dropdown
```python
ThemedDropdown(items: list, callback: Callable[[str], Any] = None)
```
Function basically the same as a normal dropdown box, but with automatic theming.

### Themed Radio Button
```python
ThemedRadioButton(callback: Callable[[bool], Any])
```
Simple radio button with custom checked and unchecked images.

### Labeled Control
```python
LabeledControl(label_text: string, widget: QWidget, spacing: int = Styles.theme.medium_spacing, margins = (math.inf, 0, 0, 0))
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

### Vertical / Horizontal Group
```python
HorizontalGroup(widgets: list[QWidget] = [], spacing: int = 0, margins = (math.inf, 0, 0, 0))
# or
VerticalGroup(widgets: list[QWidget] = [], spacing: int = 0, margins = (math.inf, 0, 0, 0))
```
A simple widget that takes a list of other widgets to line up in a horizontal or vertical list / layout.

### Panel:
```python
Panel(color = "transparent")
```
This is a very simple blank widget with a solid background. Can be used for panels or containers for other widgets.
- color: any string describing a color, usually hex, or a color name

### Themed Scroll Area
```python
ThemedScrollArea()
```
This basically works like the normal scroll area but it start without margins which is usually how you want a scroll area.

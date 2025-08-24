import sys
import importlib
import inspect
from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QListWidget, QListWidgetItem, QStyledItemDelegate
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QColor
import widgets
from resources import resources_rc


# def get_all_widget_classes(package):
#     widget_classes = []
#     for name in getattr(package, '__all__', []):  # Items in __all__
#         # Import module by full path
#         module = importlib.import_module(f"{package.__name__}.{name}")
#         # Get classes defined in each module
#         for _, obj in inspect.getmembers(module, inspect.isclass):
#             if obj.__module__ == module.__name__:
#                 widget_classes.append(obj)
#     return widget_classes

def get_all_widget_classes(package):
    widgets = getattr(package, "WIDGET_CLASSES", [])
    widgets = sorted(widgets, key=lambda cls: getattr(cls, 'GROUP', None) or '')

    return widgets


class HeaderDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        text = index.data()
        if text.startswith("---"):
            painter.save()
            painter.fillRect(option.rect, QColor("#E0E0E0"))
            painter.drawText(option.rect, Qt.AlignCenter, text.strip("- "))
            painter.restore()
        else:
            super().paint(painter, option, index)


class MainWindow(QMainWindow):
    VERSION = "v2.0"
    WIDTH = 1000
    HEIGHT = 600

    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"Helper Tools {self.VERSION}")
        self.setGeometry(100, 100, self.WIDTH, self.HEIGHT)
        self.setWindowIcon(QIcon(":/icons/icons/helper_tool_main_icon.png"))

        self.widgets = get_all_widget_classes(widgets)
        self.widget_classes = {}

        # Set up the list widget for available tools on the left
        self.list_widget = QListWidget()

        already_listed_group = []
        for widget in self.widgets:
            group_attr = getattr(widget, 'GROUP', None)
            if group_attr is not None and group_attr not in already_listed_group:
                self.list_widget.addItem(f"--- {group_attr} ---")
                already_listed_group.append(group_attr)
            self.list_widget.addItem(widget.TITLE)
            self.widget_classes[widget.TITLE] = widget

        self.list_widget.setItemDelegate(HeaderDelegate())

        self.list_widget.itemClicked.connect(self.add_selected_widget)

        # Calculate width based on the widest item in the list
        max_text_width = max(
            self.list_widget.fontMetrics().boundingRect(item.text()).width()
            for item in [self.list_widget.item(i) for i in range(self.list_widget.count())]
        )
        self.list_widget.setFixedWidth(max_text_width + 20)  # Add padding for margins

        # Create a left dock for the list widget and dock it permanently
        list_dock = QDockWidget("Tool Selector", self)
        list_dock.setWidget(self.list_widget)
        list_dock.setAllowedAreas(Qt.LeftDockWidgetArea)
        list_dock.setFeatures(QDockWidget.NoDockWidgetFeatures)  # Disable undocking
        self.addDockWidget(Qt.LeftDockWidgetArea, list_dock)

        self.widget_count = {}  # Track the count of each widget type
        self.right_dock_widgets = []  # Track right-side dock widgets for vertical stacking

        # Enable all areas for docking
        self.setDockOptions(QMainWindow.AllowNestedDocks | QMainWindow.AllowTabbedDocks)

    def add_selected_widget(self, item: QListWidgetItem):
        widget_name = item.text()

        # Increment the count for this widget type
        self.widget_count[widget_name] = self.widget_count.get(widget_name, 0) + 1
        count = self.widget_count[widget_name]

        # Get the widget class and create a unique instance with a new title
        widget_class = self.widget_classes.get(widget_name)
        if widget_class:
            widget_instance = widget_class()
            unique_title = f"{widget_name} {count}"
            self.add_widget(widget_instance, unique_title)

    def add_widget(self, widget, unique_title):
        # Create a QDockWidget and set the widget as its content
        dock_widget = QDockWidget(unique_title, self)
        dock_widget.setWidget(widget)
        dock_widget.setFloating(False)  # Default to docked

        # Add the dock widget to the right side of the main window
        self.addDockWidget(Qt.RightDockWidgetArea, dock_widget)
        dock_widget.setAllowedAreas(Qt.RightDockWidgetArea)

        # If there are already widgets on the right side, stack the new widget below the previous one
        if self.right_dock_widgets:
            self.tabifyDockWidget(self.right_dock_widgets[-1], dock_widget)

            # Schedule the selection of new tab after the event loop resumes
            QTimer.singleShot(0, dock_widget.raise_)

        # Track this widget in the right dock list for stacking
        self.right_dock_widgets.append(dock_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

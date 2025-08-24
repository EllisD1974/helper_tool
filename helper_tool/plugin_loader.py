import os
import importlib.util
import inspect
from PyQt5.QtWidgets import QWidget
from helper_tool.base_widget import BaseHelperWidget  # adjust import path


PLUGIN_PATH = "plugins"

def load_plugins(alternate_plugin_path: str = None):
    plugin_path = alternate_plugin_path or PLUGIN_PATH
    plugin_path = os.path.abspath(plugin_path)

    widgets = []

    for fname in os.listdir(plugin_path):
        if not fname.endswith(".py") or fname.startswith("__"):
            continue

        module_name = fname[:-3]
        file_path = os.path.join(plugin_path, fname)

        # Load module dynamically
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Find all classes that subclass BaseHelperWidget
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, BaseHelperWidget) and obj is not BaseHelperWidget:
                widgets.append(obj)

    # Sort widgets by GROUP attribute (like get_all_widget_classes)
    widgets = sorted(widgets, key=lambda cls: getattr(cls, "GROUP", "") or "")

    return widgets

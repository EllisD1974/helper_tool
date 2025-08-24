from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit
from PyQt5.QtCore import QSettings


class DbCredentialsWidget(QWidget):
    """Widget for entering database connection credentials."""

    def __init__(self, company_id: str, app_id: str, settings_namespace: str, parent=None):
        super().__init__(parent)

        self.company_id = company_id
        self.app_id = app_id
        self.namespace = settings_namespace

        self.inputs = {}
        layout = QVBoxLayout()

        self._add_input(layout, "Host:", "host", default="localhost")
        self._add_input(layout, "Database:", "dbname")
        self._add_input(layout, "Port:", "port", default="5432")
        self._add_input(layout, "Username:", "user")
        self._add_input(layout, "Password:", "password", echo_mode=QLineEdit.Password)

        self.setLayout(layout)

    def _add_input(self, layout, label_text, key, echo_mode=QLineEdit.Normal, default=""):
        """Helper to create and store labeled input fields."""
        row = QHBoxLayout()
        label = QLabel(label_text)
        line_edit = QLineEdit()
        line_edit.setEchoMode(echo_mode)
        line_edit.setText(default)

        row.addWidget(label)
        row.addWidget(line_edit)
        layout.addLayout(row)

        self.inputs[key] = line_edit

    def get_credentials(self) -> dict:
        """Return current credentials as a dictionary."""
        return {key: field.text() for key, field in self.inputs.items()}

    def set_credentials(self, credentials: dict):
        """Set input values based on a dictionary."""
        for key, value in credentials.items():
            if key in self.inputs:
                self.inputs[key].setText(value)

    def save_credentials(self):
        settings = QSettings(self.company_id, self.app_id)
        for key, field in self.inputs.items():
            settings.setValue(f"{self.namespace}/{key}", field.text())

    def load_credentials(self):
        settings = QSettings(self.company_id, self.app_id)
        for key in self.inputs:
            value = settings.value(f"{self.namespace}/{key}", "")
            self.inputs[key].setText(value)

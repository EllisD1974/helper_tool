from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from .logging_utils import get_logger


class BaseHelperWidget(QWidget):
    TITLE = "Base Helper Widget"

    def __init__(self):
        super().__init__()

        self.logger = get_logger(__name__)
        self.logger.debug(f"{self.TITLE} initialized")

        self.setWindowTitle(self.TITLE)

        # Set up layout(s)
        layout = QVBoxLayout()
        self.layout = QVBoxLayout()
        self.status_layout = QVBoxLayout()
        layout.addLayout(self.layout)
        layout.addLayout(self.status_layout)

        # Status label
        self.status_label = QLabel(f"_____")
        self.status_layout.addWidget(self.status_label)

        # Set main layout
        self.setLayout(layout)


    def update_status(self, text: str) -> None:
        """Update the status label."""
        self.status_label.setText(text)
        self.status_label.repaint()
        self.logger.info(text)

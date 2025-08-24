from loguru import logger as log  # noqa: D100
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QWidget
from .base_widget import BaseHelperWidget


class TextReplaceWidget(BaseHelperWidget):  # noqa: D101
    TITLE = "Text Replace"
    GROUP = "General"

    def __init__(self):  # noqa: D107
        super().__init__()

        self.setWindowTitle(self.TITLE)

        # Set up the layout and widgets
        layout = QVBoxLayout()

        # First large text box for input
        self.input_text_edit = QTextEdit()
        self.input_text_edit.setPlaceholderText("Paste or type your text here...")
        layout.addWidget(QLabel("Original Text:"))
        layout.addWidget(self.input_text_edit)

        # First single-line text box for character to be replaced
        self.replace_text_input = QLineEdit()
        # self.replace_text_input.setMaxLength(1)
        self.replace_text_input.setPlaceholderText("Character to replace...")
        layout.addWidget(QLabel("Character to Replace:"))
        layout.addWidget(self.replace_text_input)

        # Second single-line text box for replacement character
        self.replacement_text_input = QLineEdit()
        # self.replacement_text_input.setMaxLength(1)
        self.replacement_text_input.setPlaceholderText("Replacement character...")
        layout.addWidget(QLabel("Replacement Character:"))
        layout.addWidget(self.replacement_text_input)

        # Second large text box for output
        self.output_text_edit = QTextEdit()
        self.output_text_edit.setReadOnly(True)
        self.output_text_edit.setPlaceholderText("Modified text will appear here...")
        layout.addWidget(QLabel("Modified Text:"))
        layout.addWidget(self.output_text_edit)

        # Create Copy to Clipboard button
        self.copy_button = QPushButton("Copy to Clipboard", self)
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        layout.addWidget(self.copy_button)

        # Connect signals
        self.input_text_edit.textChanged.connect(self.update_output_text)
        self.replace_text_input.textChanged.connect(self.update_output_text)
        self.replacement_text_input.textChanged.connect(self.update_output_text)

        # Set main layout
        self.layout.addLayout(layout)

        self.update_status("Loaded")

    def update_output_text(self):  # noqa: D102
        # Get the input text and characters
        input_text = self.input_text_edit.toPlainText()
        replace_char = self.replace_text_input.text()
        replacement_char = self.replacement_text_input.text()

        if replace_char == "\\n":
            replace_char = "\n"
        if replacement_char == "\\n":
            replacement_char = "\n"

        # If both characters are present, perform replacement
        if replace_char and replacement_char:
            modified_text = input_text.replace(replace_char, replacement_char)
        else:
            # No replacement if characters are missing
            modified_text = input_text

        # Update the output text edit
        self.output_text_edit.setPlainText(modified_text)

    def copy_to_clipboard(self):  # noqa: D102
        try:
            clipboard = QApplication.clipboard()
            clipboard.setText(self.output_text_edit.toPlainText())
        except Exception as e:
            self.update_status(f"Clipboard error: {e}")

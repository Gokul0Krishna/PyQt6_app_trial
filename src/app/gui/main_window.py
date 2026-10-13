# src/myapp/gui/main_window.py

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QListWidget, QMessageBox
)
from core.ai_conn import AI_response
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MyApp")
        self.resize(500, 400)

        # --- Central widget and main layout ---
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # --- Input row ---
        input_row = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type something...")
        self.add_button = QPushButton("Add")
        input_row.addWidget(self.input_field)
        input_row.addWidget(self.add_button)
        layout.addLayout(input_row)

        # --- List showing items ---
        self.item_list = QListWidget()
        layout.addWidget(self.item_list)

        # --- Clear button ---
        self.clear_button = QPushButton("Clear All")
        layout.addWidget(self.clear_button, alignment=Qt.AlignmentFlag.AlignRight)

        # --- Status bar ---
        self.statusBar().showMessage("Ready")

        # --- Connect signals to slots ---
        self.add_button.clicked.connect(self.process_query)
        self.input_field.returnPressed.connect(self.process_query)
        self.clear_button.clicked.connect(self.clear_items)
        self.item_list.itemClicked.connect(self.on_item_clicked)

    def process_query(self):
        """Slot: send query to local Ollama LLM and display result."""
        text = self.input_field.text().strip()
        if not text:
            self.statusBar().showMessage("Cannot send empty query!", 3000)
            return

        self.statusBar().showMessage("Generating command...", 3000)
        
        try:
            # Call your AI function
            result = AI_response(text)
            # Add both prompt and result or just result to the list
            self.item_list.addItem(f"Q: {text}\nCmd: {result.strip()}")
            self.input_field.clear()
            self.statusBar().showMessage("Done", 3000)
        except Exception as e:
            self.statusBar().showMessage(f"Error: {str(e)}", 4000)

    def clear_items(self):
        """Slot: confirm, then clear the list."""
        if self.item_list.count() == 0:
            return
        reply = QMessageBox.question(
            self, "Clear All",
            "Remove all items?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.item_list.clear()
            self.statusBar().showMessage("List cleared", 3000)

    def on_item_clicked(self, item):
        """Slot: react when a list item is clicked."""
        self.statusBar().showMessage(f"Selected: {item.text()}", 3000)
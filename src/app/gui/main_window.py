# src/myapp/gui/main_window.py

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QListWidget, QMessageBox
)
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
        self.add_button.clicked.connect(self.add_item)
        self.input_field.returnPressed.connect(self.add_item)
        self.clear_button.clicked.connect(self.clear_items)
        self.item_list.itemClicked.connect(self.on_item_clicked)

    def add_item(self):
        """Slot: read input and append to the list."""
        text = self.input_field.text().strip()
        if not text:
            self.statusBar().showMessage("Cannot add empty item!", 3000)
            return
        self.item_list.addItem(text)
        self.input_field.clear()
        self.statusBar().showMessage(f"Added: {text}", 3000)

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
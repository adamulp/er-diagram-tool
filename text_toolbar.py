from PyQt5.QtWidgets import (
    QToolBar,
    QAction,
    QComboBox,
    QSpacerItem,
    QSizePolicy,
    QWidget,
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt


class TextToolbar(QToolBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent

        # Define a list of preferred fonts
        preferred_fonts = [
            "Noto Sans",
            "Arial",
            "Times New Roman",
            "Georgia",
            "Verdana",
            "Tahoma",
            "Courier New",
            "Comic Sans MS",  # Optionally include
            "Trebuchet MS",
            "Impact",
        ]

        # Bold action
        self.bold_action = QAction(QIcon("icons/bold.svg"), "Bold", self)
        self.bold_action.setCheckable(True)
        self.bold_action.triggered.connect(self.toggle_bold)
        self.addAction(self.bold_action)

        # Italic action
        self.italic_action = QAction(QIcon("icons/italic.svg"), "Italic", self)
        self.italic_action.setCheckable(True)
        self.italic_action.triggered.connect(self.toggle_italic)
        self.addAction(self.italic_action)

        # Underline action
        self.underline_action = QAction(QIcon("icons/underline.svg"), "Underline", self)
        self.underline_action.setCheckable(True)
        self.underline_action.triggered.connect(self.toggle_underline)
        self.addAction(self.underline_action)

        spacer = QWidget(self)
        spacer.setFixedWidth(20)
        self.addWidget(spacer)

        # Custom font selection box using QComboBox
        self.font_box = QComboBox(self)
        for font in preferred_fonts:
            self.font_box.addItem(font)
        self.font_box.setCurrentText("Noto Sans")
        self.font_box.currentTextChanged.connect(self.change_font)
        self.addWidget(self.font_box)

        # Font size selection box
        self.size_box = QComboBox(self)
        self.size_box.setEditable(True)
        self.size_box.addItems([str(i) for i in range(8, 30, 2)])
        self.size_box.setCurrentIndex(2)
        self.size_box.currentTextChanged.connect(self.change_font_size)
        self.addWidget(self.size_box)

    def apply_format_to_selected_item(self, format_function):
        selected_items = self.main_window.get_selected_items()
        for item in selected_items:
            if hasattr(item, "text_item"):
                text_item = item.text_item
                cursor = text_item.textCursor()
                cursor.select(cursor.Document)  # Select the entire text
                format_function(cursor)  # Apply the formatting function
                text_item.setTextCursor(cursor)  # Set the updated cursor back

                # Unselect the text by setting the cursor position at the end
                cursor.clearSelection()
                text_item.setTextCursor(cursor)

    def toggle_bold(self):
        def format_function(cursor):
            fmt = cursor.charFormat()
            fmt.setFontWeight(
                QFont.Bold if self.bold_action.isChecked() else QFont.Normal
            )
            cursor.setCharFormat(fmt)

        self.apply_format_to_selected_item(format_function)

    def toggle_italic(self):
        def format_function(cursor):
            fmt = cursor.charFormat()
            fmt.setFontItalic(self.italic_action.isChecked())
            cursor.setCharFormat(fmt)

        self.apply_format_to_selected_item(format_function)

    def toggle_underline(self):
        def format_function(cursor):
            fmt = cursor.charFormat()
            fmt.setFontUnderline(self.underline_action.isChecked())
            cursor.setCharFormat(fmt)

        self.apply_format_to_selected_item(format_function)

    def change_font(self, font_name):
        def format_function(cursor):
            fmt = cursor.charFormat()
            fmt.setFontFamily(font_name)
            cursor.setCharFormat(fmt)

        self.apply_format_to_selected_item(format_function)

    def change_font_size(self, size):
        def format_function(cursor):
            fmt = cursor.charFormat()
            fmt.setFontPointSize(float(size))
            cursor.setCharFormat(fmt)

        self.apply_format_to_selected_item(format_function)

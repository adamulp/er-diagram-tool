from PyQt5.QtWidgets import QToolBar, QAction, QGraphicsTextItem
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsScene  # Ensure QGraphicsScene is imported


class TextToolbar(QToolBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Bold Action
        self.bold_action = QAction(QIcon("icons/bold.svg"), "Bold", self)
        self.bold_action.setCheckable(True)
        self.bold_action.triggered.connect(self.toggle_bold)
        self.addAction(self.bold_action)

        # Italic Action
        self.italic_action = QAction(QIcon("icons/italic.svg"), "Italic", self)
        self.italic_action.setCheckable(True)
        self.italic_action.triggered.connect(self.toggle_italic)
        self.addAction(self.italic_action)

        # Underline Action
        self.underline_action = QAction(QIcon("icons/underline.svg"), "Underline", self)
        self.underline_action.setCheckable(True)
        self.underline_action.triggered.connect(self.toggle_underline)
        self.addAction(self.underline_action)

    def toggle_bold(self):
        self._toggle_font_style(QFont.bold)

    def toggle_italic(self):
        self._toggle_font_style(QFont.italic)

    def toggle_underline(self):
        self._toggle_font_style(QFont.underline)  # Correctly use QFont.Underline

    def _toggle_font_style(self, font_style):
        selected_items = self._get_selected_text_items()
        for item in selected_items:
            current_font = item.font()
            if font_style == QFont.Bold:
                current_font.setBold(not current_font.bold())
            elif font_style == QFont.Italic:
                current_font.setItalic(not current_font.italic())
            elif font_style == QFont.Underline:
                current_font.setUnderline(not current_font.underline())
            item.setFont(current_font)

    def _get_selected_text_items(self):
        # Get the scene from the parent widget
        scene = self.parent().findChild(QGraphicsScene)
        if scene:
            return [
                item
                for item in scene.selectedItems()
                if isinstance(item, QGraphicsTextItem)
            ]
        return []

from PyQt5.QtWidgets import QGraphicsItem, QGraphicsTextItem
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtCore import Qt


class ErDiagramItem(QGraphicsItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.text_item = QGraphicsTextItem("", self)
        self.text_item.setTextInteractionFlags(
            Qt.TextEditorInteraction
        )  # Allow text editing
        self.text_item.setDefaultTextColor(Qt.black)

        # Set flags for item interaction
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)  # Allow movement
        self.setFlag(
            QGraphicsItem.ItemSendsGeometryChanges
        )  # Notify changes in geometry

        self.text_item.setVisible(True)  # Ensure text item is visible

    def set_text(self, text):
        self.text_item.setPlainText(text)
        self.update_size()

    def update_size(self):
        pass  # To be implemented by derived classes

    def paint_selection(self, painter):
        if self.isSelected():
            pen = QPen(Qt.blue, 2, Qt.DashLine)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)  # Transparent fill
            painter.drawRect(self.boundingRect())

    def clear_text_editing(self):
        if self.text_item.hasFocus():
            self.text_item.setTextInteractionFlags(Qt.NoTextInteraction)
            self.text_item.clearFocus()

from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtCore import QRectF, Qt
from er_diagram import ErDiagramItem


class RectItem(QGraphicsRectItem, ErDiagramItem):
    def __init__(self, x, y, width, height):
        # Initialize both parent classes
        QGraphicsRectItem.__init__(self)
        ErDiagramItem.__init__(self)

        # Initialize the QGraphicsRectItem with the provided dimensions
        self.setRect(QRectF(0, 0, width, height))

        # Set additional properties
        self.setBrush(QBrush(Qt.lightGray))
        self.setPen(QPen(Qt.black))
        self.setPos(x, y)
        self.update_size()

    def update_size(self):
        super().update_size()
        if hasattr(self, "text_item") and self.text_item is not None:
            text_rect = self.text_item.boundingRect()
            rect = QRectF(
                0, 0, max(100, text_rect.width() + 10), max(60, text_rect.height() + 10)
            )
            self.setRect(rect)
            self.text_item.setPos(5, 5)

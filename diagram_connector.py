from PyQt5.QtWidgets import QGraphicsLineItem
from PyQt5.QtGui import QPen
from PyQt5.QtCore import Qt, QPointF


class DiagramConnector(QGraphicsLineItem):
    def __init__(self, start_item, end_item, parent=None):
        super().__init__(parent)
        self.start_item = start_item
        self.end_item = end_item
        self.setPen(QPen(Qt.black, 2))

        self.update_position()

    def update_position(self):
        """Update the position of the connector based on the connected items."""
        start_point = self.get_center(self.start_item)
        end_point = self.get_center(self.end_item)
        self.setLine(start_point.x(), start_point.y(), end_point.x(), end_point.y())

    def get_center(self, item):
        """Get the center point of a given item."""
        rect = item.boundingRect()
        return QPointF(
            item.pos().x() + rect.width() / 2, item.pos().y() + rect.height() / 2
        )

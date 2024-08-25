from PyQt5.QtWidgets import QGraphicsLineItem
from PyQt5.QtGui import QPen
from PyQt5.QtCore import Qt, QLineF, QPointF


class ConnectionNode:
    """Represents a connection point on a shape."""

    def __init__(self, item, connection_type):
        self.item = item
        self.connection_type = connection_type

    def position(self):
        """Return the position of the node."""
        if isinstance(self.item, QPointF):
            return self.item  # If item is already a QPointF, return it directly
        else:
            return self.item.pos()  # Assuming item is a QGraphicsItem


class DiagramConnector(QGraphicsLineItem):
    def __init__(self, start_pos=None, end_pos=None, parent=None):
        super().__init__(parent)
        self.start_pos = start_pos if start_pos else QPointF()
        self.end_pos = end_pos if end_pos else QPointF()
        self.is_preview = True  # Initially, it's a preview (dashed)

        self.update_position()

    def update_position(self):
        """Update the line's position based on start and end points."""
        self.setLine(QLineF(self.start_pos, self.end_pos))

        if self.is_preview:
            self.setPen(QPen(Qt.black, 2, Qt.DashLine))
        else:
            self.setPen(QPen(Qt.black, 2, Qt.SolidLine))

    def set_end_pos(self, end_pos):
        """Set the end position of the connector."""
        self.end_pos = end_pos
        self.update_position()

    def finalize(self, end_pos):
        """Finalize the connector, change to solid line."""
        self.is_preview = False
        self.set_end_pos(end_pos)

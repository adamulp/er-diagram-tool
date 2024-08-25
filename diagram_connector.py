from PyQt5.QtWidgets import QGraphicsLineItem
from PyQt5.QtGui import QPen
from PyQt5.QtCore import Qt, QPointF, QLineF


class ConnectionNode:
    """Represents a connection point on a shape."""

    def __init__(self, item, connection_type):
        self.item = item
        self.connection_type = connection_type


class DiagramConnector(QGraphicsLineItem):
    def __init__(self, start_node=None, end_node=None, parent=None):
        super().__init__(parent)

        self.start_node = start_node  # ConnectionNode or None
        self.end_node = end_node  # ConnectionNode or None
        self.setPen(QPen(Qt.black, 2))

        # Update line based on nodes
        self.update_position()

    def update_position(self):
        if self.start_node and self.end_node:
            # Both nodes are defined
            self.setLine(QLineF(self.start_node.item.pos(), self.end_node.item.pos()))
        elif self.start_node:
            # Only start node is defined
            self.setLine(QLineF(self.start_node.item.pos(), self.line().p2()))
        elif self.end_node:
            # Only end node is defined
            self.setLine(QLineF(self.line().p1(), self.end_node.item.pos()))

    def set_end_point(self, end_point):
        """Set the end point when drawing the connector dynamically in white space."""
        self.setLine(QLineF(self.line().p1(), end_point))

    def set_start_point(self, start_point):
        """Set the start point when drawing the connector dynamically in white space."""
        self.setLine(QLineF(start_point, self.line().p2()))

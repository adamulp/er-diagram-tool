from PyQt5.QtCore import QPointF, QLineF, QRectF
from PyQt5.QtGui import QPen, QPolygonF, QBrush, QPainterPath
from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsPolygonItem
from diagram_connector import DiagramConnector


class DoubleArrowConnector(DiagramConnector):
    def __init__(self, start_node, end_node, parent=None):
        super().__init__(start_node, end_node, parent)

        self.arrow_size = 10  # Size of the arrowheads

        # Create the arrowheads at both ends
        self.start_arrow_head = QGraphicsPolygonItem(self)
        self.end_arrow_head = QGraphicsPolygonItem(self)
        self.update_arrows()

    def update_position(self):
        """Update the line and arrowheads based on the positions of start_node and end_node."""
        super().update_position()

        # Update the start and end arrowheads
        self.update_arrows()

    def update_arrows(self):
        """Calculate and update the arrowheads at both ends."""
        line = self.line()

        # Calculate the start arrowhead
        angle = line.angle() + 180
        arrow_p1 = line.p1() + QPointF(
            self.arrow_size * -0.707, self.arrow_size * 0.707
        ).rotated(angle)
        arrow_p2 = line.p1() + QPointF(
            self.arrow_size * 0.707, self.arrow_size * 0.707
        ).rotated(angle)
        self.start_arrow_head.setPolygon(QPolygonF([line.p1(), arrow_p1, arrow_p2]))

        # Calculate the end arrowhead
        angle = line.angle()
        arrow_p1 = line.p2() + QPointF(
            self.arrow_size * -0.707, self.arrow_size * 0.707
        ).rotated(angle)
        arrow_p2 = line.p2() + QPointF(
            self.arrow_size * 0.707, self.arrow_size * 0.707
        ).rotated(angle)
        self.end_arrow_head.setPolygon(QPolygonF([line.p2(), arrow_p1, arrow_p2]))

        # Set the pen and brush for arrows
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        brush = QBrush(Qt.black)
        self.start_arrow_head.setPen(pen)
        self.start_arrow_head.setBrush(brush)
        self.end_arrow_head.setPen(pen)
        self.end_arrow_head.setBrush(brush)

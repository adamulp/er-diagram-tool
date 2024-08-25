from PyQt5.QtCore import QPointF, QLineF, QRectF
from PyQt5.QtGui import QPen, QPolygonF, QBrush, QPainterPath
from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsPolygonItem
from diagram_connector import DiagramConnector


class DoubleArrowConnector(DiagramConnector):
    def __init__(self, start_item, end_item, parent=None):
        super().__init__(start_item, end_item, parent)

        self.arrow_size = 10  # Size of the arrowheads

        # Create the main line connecting the two items
        self.line_item = QGraphicsLineItem(self)
        self.update_position()

        # Create the arrowheads at both ends
        self.start_arrow_head = QGraphicsPolygonItem(self)
        self.end_arrow_head = QGraphicsPolygonItem(self)
        self.update_arrows()

    def update_position(self):
        """Update the line and arrowheads based on the positions of start_item and end_item."""
        line = QLineF(self.start_item.pos(), self.end_item.pos())
        self.line_item.setLine(line)

        # Update the start and end arrowheads
        self.update_arrows()

    def update_arrows(self):
        """Calculate and update the arrowheads at both ends."""
        line = self.line_item.line()

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

    def boundingRect(self):
        """Calculate the bounding rectangle of the connector."""
        return self.childrenBoundingRect()

    def shape(self):
        """Define the shape for collision detection."""
        path = QPainterPath()
        path.addPolygon(self.start_arrow_head.polygon())
        path.addPolygon(self.end_arrow_head.polygon())
        return path

    def paint(self, painter, option, widget=None):
        """Custom paint method."""
        # Draw the line
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        painter.setPen(pen)
        painter.drawLine(self.line_item.line())

        # Draw the arrowheads
        painter.setBrush(Qt.black)
        painter.drawPolygon(self.start_arrow_head.polygon())
        painter.drawPolygon(self.end_arrow_head.polygon())

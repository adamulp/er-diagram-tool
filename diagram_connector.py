from PyQt5.QtWidgets import QGraphicsLineItem
from PyQt5.QtGui import QPen
from PyQt5.QtCore import Qt, QLineF, QPointF, QRectF


class DiagramConnector(QGraphicsLineItem):
    def __init__(self, start_item=None, start_pos=None, parent=None):
        super().__init__(parent)
        self.start_item = start_item
        self.end_item = None
        self.start_pos = start_pos if start_pos else QPointF()
        self.end_pos = None
        self.setPen(QPen(Qt.black, 2, Qt.DashLine))
        self.minimum_length = 50  # Minimum length for the connector

    def set_end_item(self, end_item):
        self.end_item = end_item

    def set_end_pos(self, end_pos):
        self.end_pos = end_pos
        if not self.end_item:
            self.setLine(QLineF(self.start_pos, self.end_pos))

    def finalize(self, end_pos):
        """Finalize the connector by attaching it to the perimeter of the start and end items."""
        if self.start_item:
            start_pos = self.get_perimeter_intersection(
                self.start_item, self.end_pos or end_pos
            )
        else:
            start_pos = self.start_pos

        if self.end_item:
            end_pos = self.get_perimeter_intersection(self.end_item, start_pos)
        else:
            end_pos = end_pos

        # Calculate the length of the connector
        line = QLineF(start_pos, end_pos)
        line_length = line.length()

        if line_length < self.minimum_length and line_length > 0:
            # Extend the line to the minimum length
            scale_factor = self.minimum_length / line_length
            dx = line.dx() * (scale_factor - 1)
            dy = line.dy() * (scale_factor - 1)
            end_pos = QPointF(line.p2().x() + dx, line.p2().y() + dy)
            line.setP2(end_pos)

            # Handle collision with other shapes (optional)
            self.handle_collision(line)

        self.setLine(line)
        self.setPen(QPen(Qt.black, 2, Qt.SolidLine))

    def get_perimeter_intersection(self, item, other_pos):
        """Calculate the intersection point of the connector with the item's perimeter."""
        rect = item.boundingRect().translated(item.pos())
        line = QLineF(rect.center(), other_pos)

        return self.find_intersection_with_rectangle(rect, line)

    def handle_collision(self, line):
        """Adjust the position of nearby shapes if the connector gets too close."""
        # Calculate a bounding rectangle around the line
        bounding_rect = QRectF(line.p1(), line.p2()).normalized().adjusted(-5, -5, 5, 5)

        # Check for items near the extended connector line
        near_items = self.scene().items(bounding_rect)
        for item in near_items:
            if (
                isinstance(item, ErDiagramItem)
                and item != self.start_item
                and item != self.end_item
            ):
                # Adjust the position of the item slightly to avoid overlap
                item.moveBy(10, 10)

    def find_intersection_with_rectangle(self, rect, line):
        """Find the intersection point of a line with a rectangle's perimeter."""
        edges = [
            QLineF(rect.topLeft(), rect.topRight()),  # Top edge
            QLineF(rect.topRight(), rect.bottomRight()),  # Right edge
            QLineF(rect.bottomRight(), rect.bottomLeft()),  # Bottom edge
            QLineF(rect.bottomLeft(), rect.topLeft()),  # Left edge
        ]

        intersect_point = QPointF()
        for edge in edges:
            if line.intersect(edge, intersect_point) == QLineF.BoundedIntersection:
                return intersect_point

        return line.p2()  # Default to the end point if no intersection

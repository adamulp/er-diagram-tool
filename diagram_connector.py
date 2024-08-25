from PyQt5.QtWidgets import QGraphicsLineItem
from PyQt5.QtGui import QPen, QPolygonF
from PyQt5.QtCore import Qt, QLineF, QPointF, QRectF
from er_diagram import ErDiagramItem
import math

from triangle_special_generalization import TriangleItem
from diamond_relationship import DiamondItem
from rectangle_table import RectItem
from oval_attribute import OvalItem


class DiagramConnector(QGraphicsLineItem):
    def __init__(self, start_item=None, start_pos=None, parent=None):
        super().__init__(parent)
        self.start_item = start_item
        self.end_item = None
        self.start_pos = start_pos if start_pos else QPointF()
        self.end_pos = None
        self.setPen(QPen(Qt.black, 2, Qt.DashLine))
        self.minimum_length = 50  # Minimum length for the connector

    def set_end_pos(self, end_pos):
        """Set the end position of the connector."""
        self.end_pos = end_pos
        # Update the line to the new end position
        if self.start_pos:
            self.setLine(QLineF(self.start_pos, self.end_pos))

    def set_end_item(self, end_item):
        """Set the end item of the connector and update its position."""
        self.end_item = end_item
        # If the start position is set, update the end position based on the end item
        if self.start_pos and self.end_item:
            self.end_pos = self.get_perimeter_intersection(
                self.end_item, self.start_pos
            )
            self.setLine(QLineF(self.start_pos, self.end_pos))

    def finalize(self, end_pos):
        """Finalize the connector by attaching it to the perimeter of the start and end items."""
        print(f"Start item: {self.start_item}")
        print(f"End item: {self.end_item}")

        if self.start_item:
            start_pos = self.get_perimeter_intersection(
                self.start_item, self.end_pos or end_pos
            )
        else:
            start_pos = self.start_pos

        if self.end_item:
            end_pos = self.get_perimeter_intersection(self.end_item, start_pos)
        else:
            end_pos = self.end_pos or end_pos

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
        if isinstance(item, OvalItem):
            return self.find_intersection_with_oval(item, other_pos)
        elif isinstance(item, TriangleItem):
            return self.find_intersection_with_triangle(item, other_pos)
        elif isinstance(item, DiamondItem):
            return self.find_intersection_with_diamond(item, other_pos)
        else:
            return self.find_intersection_with_rectangle(
                item.boundingRect().translated(item.pos()),
                QLineF(item.pos(), other_pos),
            )

    def find_intersection_with_oval(self, oval, other_pos):
        """Find the intersection point of a line with the perimeter of an oval."""
        rect = oval.boundingRect().translated(oval.pos())
        center = rect.center()

        # Normalize the line vector
        direction = other_pos - center
        angle = math.atan2(direction.y(), direction.x())

        # Calculate the point on the ellipse's perimeter
        a = rect.width() / 2.0
        b = rect.height() / 2.0
        x = a * math.cos(angle)
        y = b * math.sin(angle)

        return center + QPointF(x, y)

    def find_intersection_with_triangle(self, triangle, other_pos):
        """Find the intersection point of a line with the perimeter of a triangle."""
        # Assuming the triangle points are stored in a QPolygonF
        rect = triangle.boundingRect().translated(triangle.pos())
        triangle_points = QPolygonF(
            [
                rect.topLeft(),
                QPointF(rect.center().x(), rect.bottom()),
                rect.topRight(),
            ]
        )

        # Find intersection with triangle edges
        return self.find_intersection_with_polygon(triangle_points, other_pos)

    def find_intersection_with_diamond(self, diamond, other_pos):
        """Find the intersection point of a line with the perimeter of a diamond."""
        rect = diamond.boundingRect().translated(diamond.pos())
        diamond_points = QPolygonF(
            [
                QPointF(rect.center().x(), rect.top()),
                QPointF(rect.right(), rect.center().y()),
                QPointF(rect.center().x(), rect.bottom()),
                QPointF(rect.left(), rect.center().y()),
            ]
        )

        # Find intersection with diamond edges
        return self.find_intersection_with_polygon(diamond_points, other_pos)

    def find_intersection_with_polygon(self, polygon, other_pos):
        """Helper function to find the intersection of a line with any polygon."""
        center = polygon.boundingRect().center()
        line = QLineF(center, other_pos)

        for i in range(len(polygon)):
            edge = QLineF(polygon[i], polygon[(i + 1) % len(polygon)])
            intersect_point = QPointF()
            if line.intersect(edge, intersect_point) == QLineF.BoundedIntersection:
                return intersect_point

        return polygon.boundingRect().center()

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

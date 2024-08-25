from diagram_connector import DiagramConnector
from PyQt5.QtGui import QPolygonF, QBrush, QPen
from PyQt5.QtCore import QPointF, Qt


class ArrowConnector(DiagramConnector):
    def __init__(self, start_node, end_node, parent=None):
        super().__init__(start_node, end_node, parent)

    def update_position(self):
        super().update_position()

        # Create an arrowhead at the end of the connector
        arrow_size = 10
        line = self.line()
        angle = line.angle()

        # Calculate points for the arrowhead
        arrow_p1 = line.p2() + QPointF(arrow_size * -0.707, arrow_size * 0.707).rotated(
            angle - 150
        )
        arrow_p2 = line.p2() + QPointF(arrow_size * 0.707, arrow_size * 0.707).rotated(
            angle + 150
        )

        arrow_head = QPolygonF([line.p2(), arrow_p1, arrow_p2])
        self.scene().addPolygon(arrow_head, QPen(Qt.black), QBrush(Qt.black))

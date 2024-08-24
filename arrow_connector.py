from diagram_connector import DiagramConnector
from PyQt5.QtGui import QPolygonF, QBrush
from PyQt5.QtCore import QPointF, Qt


class ArrowConnector(DiagramConnector):
    def __init__(self, start_item, end_item, parent=None):
        super().__init__(start_item, end_item, parent)

    def update_position(self):
        super().update_position()

        # Create an arrowhead at the end of the connector
        arrow_size = 10
        line = self.line()
        angle = line.angle()

        # Calculate points for the arrowhead
        arrow_p1 = line.p2() - QPointF(
            arrow_size * Qt.cos(angle + 150), arrow_size * Qt.sin(angle + 150)
        )
        arrow_p2 = line.p2() - QPointF(
            arrow_size * Qt.cos(angle - 150), arrow_size * Qt.sin(angle - 150)
        )

        arrow_head = QPolygonF([line.p2(), arrow_p1, arrow_p2])
        self.arrow_head_item = self.scene().addPolygon(
            arrow_head, QPen(Qt.black), QBrush(Qt.black)
        )

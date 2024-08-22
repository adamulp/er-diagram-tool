from PyQt5.QtWidgets import (
    QGraphicsView,
    QGraphicsScene,
    QGraphicsRectItem,
    QApplication,
    QGraphicsItem,
)
from PyQt5.QtGui import QCursor, QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QRectF


class SimpleItem(QGraphicsRectItem):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setBrush(QBrush(Qt.lightGray))


class SimpleCanvas(QGraphicsView):
    def __init__(self, scene=None, parent=None):
        if scene is None:
            scene = QGraphicsScene()
        scene.setSceneRect(0, 0, 800, 600)
        super().__init__(scene, parent)

        self.setRenderHint(QPainter.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setScene(scene)
        self.setup_scene()

    def setup_scene(self):
        # Add a single SimpleItem to test movement
        item = SimpleItem(100, 100, 100, 100)
        self.scene().addItem(item)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        print("Mouse pressed:", event.pos())

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        print("Mouse moved:", event.pos())

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        print("Mouse released:", event.pos())

    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        print("Mouse double-clicked:", event.pos())


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    view = SimpleCanvas()
    view.setWindowTitle("Simple Canvas")
    view.resize(800, 600)
    view.show()
    sys.exit(app.exec_())

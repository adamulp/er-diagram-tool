from diagram_connector import DiagramConnector


class LineConnector(DiagramConnector):
    def __init__(self, start_node, end_node, parent=None):
        super().__init__(start_node, end_node, parent)

    def update_position(self):
        super().update_position()
        # No additional features needed for a simple line connector

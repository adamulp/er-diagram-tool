from diagram_connector import DiagramConnector


class LineConnector(DiagramConnector):
    def __init__(self, start_pos=None, end_pos=None, parent=None):
        super().__init__(start_pos, end_pos, parent)

    # You can add any specific methods for LineConnector here if needed

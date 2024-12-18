# TODO: switch to PyQt6

import sys

from models import graphs, visual

from PyQt6.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = visual.MainWindow(graphs.graph_actions)
    window.show()

    app.exec()
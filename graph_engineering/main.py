import sys

from models import actions, visual # type: ignore[import-not-found]

from PyQt6.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = visual.MainWindow(actions.actions)
    window.show()

    app.exec()
from . import actions

import matplotlib.pyplot as plt
import numpy as np
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):

    def __init__(self, graph_actions: dict[str, list[str]]) -> None:

        super().__init__()
        self.showMaximized()

        self.setWindowTitle("Widgets App")

        layout = QVBoxLayout()
        widget = QWidget()

        self.function = actions.Function([actions.linear])
        self.graph_holder = QLabel()
        self.added_actions_list = QListWidget()
        self.all_actions_list = QListWidget()
        for action in graph_actions:
            action_item = QListWidgetItem(self.all_actions_list)
            action_item.setText(action)


        self.input_getter: QLineEdit | None = None
        def select_action(action_item: QListWidgetItem):
            # if user selects one action, and then 
            # decides to switch it, remove old input getter
            if self.input_getter:
                layout.removeWidget(self.input_getter)
            self.input_getter = QLineEdit(parent=self)
            self.input_getter.setPlaceholderText("Type float value")
            def add_action():
                # isdigit() returns False if encounters minus
                if not self.input_getter.text().replace('-','').isdigit():
                    self.input_getter.clear()
                    self.input_getter.setPlaceholderText(
                        "Float value only! Note: separate fractional part by a dot, not a comma."
                        )
                    return
                
                self.function.add_func(eval(f"actions.{action_item.text()}"), (float(self.input_getter.text())))
                total_rows = self.added_actions_list.currentRow()

                new_action_item = QListWidgetItem(self.added_actions_list)
                new_action_item.setText(f"{action_item.text()} {self.input_getter.text()}")
                self.added_actions_list.insertItem(total_rows, new_action_item)

                self.update_graph(1000, -10, 10)
                layout.removeWidget(self.input_getter)
                self.input_getter.deleteLater()
                self.input_getter = None

            self.input_getter.returnPressed.connect(add_action)
            layout.addWidget(self.input_getter)
            self.show()


        self.all_actions_list.itemClicked.connect(select_action)
        layout.addWidget(self.added_actions_list)
        layout.addWidget(self.all_actions_list)
        layout.addWidget(self.graph_holder)
        widget.setLayout(layout)

        self.update_graph(1000, -10, 10)
        self.setCentralWidget(widget)


    def update_graph(self, fs: int, start_x: int, end_x: int):
        x = np.linspace(start=start_x, stop=end_x, num=fs)
        y = self.function(x)
        # preserve scale
        plt.clf()
        plt.ylim(start_x, end_x)
        plt.grid(True)
        plt.plot(x, y, c="blue")
        plt.savefig("graph.png")
        self.graph_holder.setPixmap(QPixmap("graph.png"))
        self.show()
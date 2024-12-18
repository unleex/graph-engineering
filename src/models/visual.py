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

from . import graphs


graph_actions = dict(sorted({"Linear": ["scale", "move"]}.items()))


class MainWindow(QMainWindow):

    def __init__(self, graph_actions: dict[str, list[str]]) -> None:

        super().__init__()

        self.setWindowTitle("Widgets App")

        layout = QVBoxLayout()
        widget = QWidget()

        self.graph = graphs.BaseGraph()

        graph_holder = QLabel(self)
        self.graph_holder = graph_holder
        graph_list = QListWidget(self)
        for graph_kind in graph_actions:
            item = QListWidgetItem(graph_list)
            item.setText(graph_kind)

        def change_graph(graph_item: QListWidgetItem):
            self.graph = eval(f"graphs.{graph_item.text()}")()
            self.action_list.clear()
            for action in graph_actions[self.graph.__class__.__qualname__]:
                item = QListWidgetItem(self.action_list)
                item.setText(action)
            self.update_graph(1000, -10, 10)
        graph_list.itemClicked.connect(change_graph)
        layout.addWidget(graph_list)


        self.input_getter: QLineEdit | None = None
        def select_action(action_item: QListWidgetItem):
            # if user selects one action, and then 
            # decides to switch it, remove old input getter
            if self.input_getter:
                layout.removeWidget(self.input_getter)
            self.input_getter = QLineEdit(parent=self)
            self.input_getter.setPlaceholderText("Type float value")
            def make_action():
                # isdigit() returns False if encounters minus
                if not self.input_getter.text().replace('-','').isdigit():
                    self.input_getter.clear()
                    self.input_getter.setPlaceholderText(
                        "Float value only! Note: separate fractional part by a dot, not a comma."
                        )
                    return
                
                getattr(self.graph, action_item.text())(float(self.input_getter.text()))
                self.update_graph(1000, -10, 10)
                layout.removeWidget(self.input_getter)
                self.input_getter.deleteLater()
                self.input_getter = None
            self.input_getter.returnPressed.connect(make_action)
            layout.addWidget(self.input_getter)
            self.show()
        self.action_list = QListWidget(self)
        self.action_list.itemClicked.connect(select_action)
        layout.addWidget(self.action_list)
        

        layout.addWidget(graph_holder)
        widget.setLayout(layout)

        # Устанавливаем центральный виджет окна. Виджет будет расширяться по умолчанию,
        # заполняя всё пространство окна.
        self.setCentralWidget(widget)
        self.update_graph(1000, -10, 10)


    def update_graph(self, fs: int, start_x: int, end_x: int):
        x = np.linspace(start=start_x, stop=end_x, num=fs)
        y = self.graph.f(x)
        # preserve scale
        plt.clf()
        plt.ylim(start_x, end_x)
        plt.grid(True)
        plt.plot(x, y, c="blue")
        plt.savefig("graph.png")
        self.graph_holder.setPixmap(QPixmap("graph.png"))
        self.show()
graph_actions = dict(sorted({"Linear": ["scale", "move"]}.items()))


import matplotlib.pyplot as plt
import numpy as np


class BaseGraph:

    def __init__(self, *args, **kwargs) -> None:
        ...
    
    def show(self, fs: int, start_x: int, end_x: int) -> None:
        ...


class Linear(BaseGraph):
    
    def __init__(self, k: float = 1, b: float = 0):
        self.k = k
        self.b = b

        def f(x: float) -> float:
            return self.k * x + self.b
        
        self.f = np.vectorize(f)
        

    def scale(self, k: float) -> None:
        self.k = k


    def move(self, b: float) -> None:
        self.b = b

    
    def show(self, fs: int, start_x: int, end_x: int):
        x = np.linspace(start=start_x, stop=end_x, num=fs)
        y = self.f(x)
        # preserve scale
        plt.ylim(start_x, end_x)
        plt.grid(True)
        plt.plot(x, y)
        plt.show()
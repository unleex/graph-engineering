import numpy as np


graph_actions = dict(sorted({"Linear": ["scale", "move"]}.items()))
__all__ = list(graph_actions.keys()) + ["BaseGraph"]


class BaseGraph:

    def __init__(self, *args, **kwargs) -> None:
        ...
        self.f = np.vectorize(lambda x: None)


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
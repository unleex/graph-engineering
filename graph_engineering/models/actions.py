from graph_engineering.utils.utils import chain_functions

from functools import partial
import typing

import numpy as np


actions = ["scale", "shift"]


class Function:

    def __init__(self, functions: list[typing.Callable] = []):

        self.functions = functions
        if len(functions) > 1:
            chained = chain_functions(*functions) # type: ignore[arg-type]
        else:
            chained = functions[0]
        self.f = np.vectorize(chained) 

    #TODO: don't reassign chained from ground up for every adding
    def add_func(self, function: typing.Callable, parameter: float):
        self.functions.append(partial(function, parameter))
        self.f = np.vectorize(chain_functions(*self.functions)) # type: ignore[arg-type]

    
    def __call__(self, x: np.ndarray):

        if not self.functions:
            raise ValueError("Functions missing!")
        return self.f(x)
    

def scale(x: float, k: float):
    return x * k


def shift(x: float, b: float):
    return x + b


def linear(x: float):
    return x
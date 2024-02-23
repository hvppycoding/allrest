from allrest.restreeabstractevaluator import RESTreeAbstractEvaluator
from allrest.restree import RESTree
import copy


class RESTreeLengthEvaluator(RESTreeAbstractEvaluator):
    def __init__(self, weight: float=1.0):
        super().__init__(weight)
    
    def get_cost(self, restree: RESTree) -> float:
        x = [restree.x(i) for i in range(restree.n_pins)]
        y = [restree.y(i) for i in range(restree.n_pins)]
        x_low = copy.copy(x)
        x_high = copy.copy(x)
        y_low = copy.copy(y)
        y_high = copy.copy(y)
        
        for nv, nh in restree.res:
            x_low[nh] = min(x_low[nh], x[nv])
            x_high[nh] = max(x_high[nh], x[nv])
            y_low[nv] = min(y_low[nv], y[nh])
            y_high[nv] = max(y_high[nv], y[nh])
            
        length = 0
        for i in range(restree.n_pins):
            length += x_high[i] - x_low[i] + y_high[i] - y_low[i]
        return length
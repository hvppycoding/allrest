from allrest.restreeabstractevaluator import RESTreeAbstractEvaluator
from allrest.restree import RESTree
from allrest.overflowmanager import OverflowManager
import copy
from typing import Callable


class RESTreeOverflowEvaluator(RESTreeAbstractEvaluator):
    def __init__(self, overflow_manager: OverflowManager):
        super().__init__("RESTreeOverflowEvaluator")
        self.overflow_manager = overflow_manager
    
    def get_cost(self, restree: RESTree, callback: Callable[[str, float, str], None]=None) -> float:
        overflows = 0
        for i in range(restree.n_pins):
            y = restree.y(i)
            x_low = restree.x_low(i)
            x_high = restree.x_high(i)
            overflows += self.overflow_manager.count_hoverflow(y, x_low, x_high)
            
        for i in range(restree.n_pins):
            x = restree.x(i)
            y_low = restree.y_low(i)
            y_high = restree.y_high(i)
            overflows += self.overflow_manager.count_voverflow(x, y_low, y_high)
        if callback is not None:
            callback(self.name, overflows, "overflows")
        return overflows
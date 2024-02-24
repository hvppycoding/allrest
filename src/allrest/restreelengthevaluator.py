from allrest.restreeabstractevaluator import RESTreeAbstractEvaluator
from allrest.restree import RESTree
from typing import Callable
import copy


class RESTreeLengthEvaluator(RESTreeAbstractEvaluator):
    def __init__(self):
        super().__init__("RESTreeLengthEvaluator")
    
    def get_cost(self, restree: RESTree, callback: Callable[[str, float, str], None]=None) -> float:
        cost = restree.length()
        if callback:
            callback(self.name, cost, "length")
        return cost
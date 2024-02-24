from typing import List, Callable
from allrest.restreeabstractevaluator import RESTreeAbstractEvaluator
from allrest.restree import RESTree


class RESTreeCompositeEvaluator(RESTreeAbstractEvaluator):
    def __init__(self, evaluators: List[RESTreeAbstractEvaluator]):
        super().__init__("RESTreeCompositeEvaluator")
        self.evaluators: List[RESTreeAbstractEvaluator] = evaluators
        
    def add_evaluator(self, evaluator: RESTreeAbstractEvaluator) -> None:
        self.evaluators.append(evaluator)
        
    def get_cost(self, restree: RESTree, callback: Callable[[str, float, str], None]=None) -> float:
        cost = 0
        for evaluator in self.evaluators:
            cost += evaluator.get_cost(restree, callback=callback)
        if callback:
            callback(self.name, cost, "")
        return cost
        
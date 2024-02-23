from typing import List
from allrest.restreeabstractevaluator import RESTreeAbstractEvaluator
from allrest.restree import RESTree


class RESTreeCompositeEvaluator(RESTreeAbstractEvaluator):
    def __init__(self, evaluators: List[RESTreeAbstractEvaluator], weight: float=1.0):
        super().__init__(weight)
        self.evaluators: List[RESTreeAbstractEvaluator] = evaluators
        
    def add_evaluator(self, evaluator: RESTreeAbstractEvaluator) -> None:
        self.evaluators.append(evaluator)
        
    def get_cost(self, restree: RESTree) -> float:
        cost = 0
        for evaluator in self.evaluators:
            cost += evaluator.get_cost(restree)
        return cost
        
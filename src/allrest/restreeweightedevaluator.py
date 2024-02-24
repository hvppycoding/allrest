from typing import List, Callable
from allrest.restreeabstractevaluator import RESTreeAbstractEvaluator
from allrest.restree import RESTree


class RESTreeWeightedEvaluator(RESTreeAbstractEvaluator):
    def __init__(self, evaluator: RESTreeAbstractEvaluator, weight: float=1.0):
        super().__init__("RESTreeWeightedEvaluator")
        self.evaluator: RESTreeAbstractEvaluator = evaluator
        self.weight: float = weight
        
    def get_cost(self, restree: RESTree, callback: Callable=None) -> float:
        messages = []
        def callback_wrapper(name, cost, msg):
            messages.append((name, cost, msg))
        
        cost = self.evaluator.get_cost(restree, callback=callback_wrapper) * self.weight
        if callback:
            str_messages = [f"{name}: {c:.3g} {msg}" for name, c, msg in messages]
            msg = "+".join(str_messages)
            callback(f"{self.name}({self.weight:.3g})", cost, f"({msg})" )
        return cost
        
from allrest.restreeabstractevaluator import RESTreeAbstractEvaluator
from allrest.restree import RESTree


class Optimizer:
    def __init__(self, evaluator: RESTreeAbstractEvaluator):
        self.evaluator: RESTreeAbstractEvaluator = evaluator
    
    def optimize(self, restree: RESTree) -> RESTree:
        pass
    
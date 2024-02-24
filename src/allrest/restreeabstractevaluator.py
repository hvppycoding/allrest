from typing import List
from abc import ABC, abstractmethod
from allrest.res import RES
from allrest.restree import RESTree
from allrest.pin import Pin
from allrest.treeconverter import TreeConverter
from allrest.steinergraph import SteinerGraph
import numpy as np


class RESTreeAbstractEvaluator(ABC):
    def __init__(self, weight: float = 1.0):
        self.weight: float = weight
        
    def get_weighted_cost(self, restree: RESTree) -> float:
        return self.get_cost(restree) * self.weight
         
    @abstractmethod
    def get_cost(self, restree: RESTree) -> float:
        pass


if __name__ == "__main__":
    from allrest.restreelengthevaluator import RESTreeLengthEvaluator
    from allrest.restreelengthevaluator2 import RESTreeLengthEvaluator2
    from allrest.restreedetourevaluator import RESTreeDetourEvaluator
    from allrest.restreeoverflowevaluator import RESTreeOverflowEvaluator
    from allrest.overflowmanager import OverflowManager
    from allrest.utils.test import generate_random_restree, generate_random_overflow_manager
    
    nx = 20
    ny = 10
    
    for i in range(1):
        ofm: OverflowManager = generate_random_overflow_manager(nx=nx, ny=ny)
        restree: RESTree = generate_random_restree(ny=ny, nx=nx, slack_mean=0, slack_std=10e-12)
        wirelength = RESTreeLengthEvaluator().get_cost(restree)
        detour = RESTreeDetourEvaluator().get_cost(restree)
        overflow = RESTreeOverflowEvaluator(ofm).get_cost(restree)
        
        from allrest.utils.render import render_RESTree
        render_RESTree(restree, f"restree{i}.png", overflow_manager=ofm)   
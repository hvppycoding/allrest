from allrest.overflowmanager import OverflowManager
from allrest.restree import RESTree
from allrest.restreeabstractevaluator import RESTreeAbstractEvaluator
from typing import List, Dict, Set, Tuple
from allrest.restreeoptimizer import RESTreeOptimizer
from allrest.utils import outputmanager
from allrest.restree import RESTree
from allrest.utils.render import render_RESTree
import copy

class ForestOptimizer:
    def __init__(self, 
                 restrees: List[RESTree],
                 overflow_manager: OverflowManager,
                 evaluator: RESTreeAbstractEvaluator):
        self.overflow_manager: OverflowManager = overflow_manager
        self.trees: List[RESTree] = restrees
        self.tree_costs: List[float] = [0 for _ in self.trees]
        self.evalutor: RESTreeAbstractEvaluator = evaluator
        self.treeoptimizer: RESTreeOptimizer = RESTreeOptimizer(evaluator=evaluator)
        self.initialize()
        
    def initialize(self):
        for tree in self.trees:
            for i in range(tree.n_pins):
                self.overflow_manager.change_husage(tree.y(i), tree.x_low(i), tree.x_high(i), +1)
                self.overflow_manager.change_vusage(tree.x(i), tree.y_low(i), tree.y_high(i), +1)
        for i, tree in enumerate(self.trees):
            self.tree_costs[i] = self.evalutor.get_cost(tree)
        outputmanager.info("Initialized ForestOptimizer:" + str(sum(self.tree_costs)))
        
    def optimize(self):
        for i, tree in enumerate(self.trees):
            new_tree = self.treeoptimizer.optimize(tree)
            new_cost = self.evalutor.get_cost(new_tree)
            
            if new_cost < self.tree_costs[i]:
                prev_filepath = outputmanager.get_output_path("optimized_tree_{}.png".format(i))
                new_filepath = outputmanager.get_output_path("optimized_tree_{}_new.png".format(i))
                render_RESTree(self.trees[i], filepath=prev_filepath, overflow_manager=self.overflow_manager)
                render_RESTree(new_tree, filepath=new_filepath, overflow_manager=self.overflow_manager)
                self.trees[i] = new_tree
                self.tree_costs[i] = new_cost
                
                
                
            
        outputmanager.info("Optimized ForestOptimizer:" + str(sum(self.tree_costs)))
            
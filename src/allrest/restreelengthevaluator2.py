from allrest.restreeabstractevaluator import RESTreeAbstractEvaluator
from allrest.restree import RESTree
from allrest.treeconverter import TreeConverter
from allrest.steinergraph import SteinerGraph, SteinerNode
from typing import Set


class RESTreeLengthEvaluator2(RESTreeAbstractEvaluator):
    def __init__(self, weight: float=1.0):
        super().__init__(weight)
    
    def calculate_wirelength(self, node: SteinerNode, visited: Set[SteinerNode]):
        if node in visited:
            return 0
        visited.add(node)
        wirelength = 0
        for neighbor in node.neighbors:
            if neighbor in visited:
                continue
            wirelength += abs(node.x - neighbor.x) + abs(node.y - neighbor.y)
            wirelength += self.calculate_wirelength(neighbor, visited)
        return wirelength
    
    def get_cost(self, restree: RESTree) -> float:
        steiner_graph: SteinerGraph = TreeConverter(restree).convert()
        driver_index = restree.driver_index
        driver_node: SteinerNode = steiner_graph.get_node(driver_index)
        return self.calculate_wirelength(driver_node, set())

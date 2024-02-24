from allrest.restreeabstractevaluator import RESTreeAbstractEvaluator
from allrest.restree import RESTree
from allrest.treeconverter import TreeConverter
from allrest.steinergraph import SteinerGraph, SteinerNode
from typing import Set, Callable


class RESTreeLengthEvaluator2(RESTreeAbstractEvaluator):
    def __init__(self):
        super().__init__("RESTreeLengthEvaluator2")
    
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
    
    def get_cost(self, restree: RESTree, callback: Callable[[str, float, str], None]=None) -> float:
        steiner_graph: SteinerGraph = TreeConverter(restree).convert_to_steiner_graph()
        driver_index = restree.driver_index
        driver_node: SteinerNode = steiner_graph[driver_index]
        cost = self.calculate_wirelength(driver_node, set())
        if callback:
            callback(self.name, cost, "wirelength")
        return cost

from allrest.restreeabstractevaluator import RESTreeAbstractEvaluator
from allrest.restree import RESTree
from allrest.pin import Pin
from allrest.treeconverter import TreeConverter
from allrest.steinergraph import SteinerGraph, SteinerNode
from typing import Set, Dict, Callable
import copy
import math


def default_weight_function(pin: Pin) -> float:
    if pin.is_driver:
        return 0
    a = -pin.slack * 1E+11
    return math.exp(a)


class RESTreeDetourEvaluator(RESTreeAbstractEvaluator):
    def __init__(self, weight_function: Callable[[Pin], float]=default_weight_function):
        super().__init__("RESTreeDetourEvaluator")
        self.weight_function: Callable[[Pin], float] = weight_function
    
    def get_cost(self, restree: RESTree, callback: Callable[[str, float, str], None]=None) -> float:
        pathlengths: Dict[int, int] = self.calculate_pathlength_from_driver(restree)
        manhattan_distances: Dict[int, int] = self.calculate_manhattan_distance_from_driver(restree)
        
        total_cost = 0
        for i in range(restree.n_pins):
            if i not in pathlengths:
                raise ValueError(f"Pin {i} not in pathlengths")
            if i not in manhattan_distances:
                raise ValueError(f"Pin {i} not in manhattan_distances")
            detour = pathlengths[i] - manhattan_distances[i]
            slack = restree.pins[i].slack
            weight = self.weight_function(restree.pins[i])
            cost = weight * detour
            # print(f"Pin {i} detour: {detour}, cost: {cost:.6f}, weight: {weight:.6f}, slack: {slack:.6g}")
            total_cost += cost
        if callback:
            callback("RESTreeDetourEvaluator", total_cost, "detour cost")
        return total_cost
    
    def calculate_manhattan_distance_from_driver(self, restree: RESTree) -> Dict[int, int]:
        driver_index = restree.driver_index
        drv_x = restree.x(driver_index)
        drv_y = restree.y(driver_index)
        
        manhattan_distances: Dict[int, int] = {}
        for i in range(restree.n_pins):
            x = restree.x(i)
            y = restree.y(i)
            manhattan_distance = abs(drv_x - x) + abs(drv_y - y)
            manhattan_distances[i] = manhattan_distance
            
        return manhattan_distances
        
    def calculate_pathlength_from_driver(self, restree: RESTree) -> Dict[int, int]:
        steiner_graph: SteinerGraph = TreeConverter(restree).convert_to_steiner_graph()
        driver_index = restree.driver_index
        driver_node: SteinerNode = steiner_graph[driver_index]
        
        pathlengths = {}
        self.calculate_pathlength_helper(driver_node, 0, pathlengths)
        
        for node in steiner_graph._nodes:
            if node.index not in pathlengths:
                raise ValueError(f"Node {node.index} not in pathlengths")
        
        filtered_pathlengths = {}
        for index, pathlength in sorted(pathlengths.items()):
            node = steiner_graph[index]
            if node.is_pin:
                filtered_pathlengths[index] = pathlength
        return filtered_pathlengths
    
    def calculate_pathlength_helper(self, node: SteinerNode, curpathlength: int, pathlengths: Dict[int, int]):
        pathlengths[node.index] = curpathlength
        
        for neighbor in node.neighbors:
            if neighbor.index in pathlengths:
                continue
            additional_length = abs(node.x - neighbor.x) + abs(node.y - neighbor.y)
            next_pathlength = curpathlength + additional_length
            self.calculate_pathlength_helper(neighbor, next_pathlength, pathlengths)

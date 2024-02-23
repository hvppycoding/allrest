from typing import List
from allrest.res import RES
from allrest.restree import RESTree
from allrest.pin import Pin


class SteinerNode:
    def __init__(self, index: int, x: int, y: int, is_pin: bool, pin: Pin=None):
        self.index: int = index
        self.x: int = x
        self.y: int = y
        self.is_pin: bool = is_pin
        self.pin: Pin = pin
        self.neighbors: List[SteinerNode] = []
        
    def add_neighbor(self, neighbor: "SteinerNode") -> None:
        self.neighbors.append(neighbor)


class SteinerGraph:
    def __init__(self, nodes: List[SteinerNode]):
        self._nodes: List[SteinerNode] = nodes
        
    def get_node(self, index: int) -> SteinerNode:
        return self._nodes[index]
        
    def __str__(self):
        node_strs = []
        for node in self._nodes:
            node_strs.append(str(node))
        return "\n\n".join(node_strs)
    
    def add_node(self, node: SteinerNode) -> None:
        self._nodes.append(node)
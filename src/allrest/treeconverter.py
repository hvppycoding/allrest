from typing import List, Dict
from enum import Enum
from allrest.pin import Pin
from allrest.restree import RESTree
from allrest.res import RES
from allrest.steinergraph import SteinerGraph, SteinerNode
from allrest.steinertree import SteinerTree, SteinerTreeBranch


class ConverterNode:
    def __init__(self, index: int, x: int, y: int, is_pin: bool, pin: Pin):
        self.index: int = index
        self.x: int = x
        self.y: int = y
        self.is_pin: bool = is_pin
        self.pin: Pin = pin
        # Sorted by x(ascending)
        self.right_neighbors: List[ConverterNode] = []
        # Sorted by x(descending)
        self.left_neighbors: List[ConverterNode] = []
        self.up_neighbors: List[ConverterNode] = []  # Sorted by y(ascending)
        # Sorted by y(descending)
        self.down_neighbors: List[ConverterNode] = []
        
    def remove_neighbor(self, neighbor: "ConverterNode") -> None:
        if neighbor in self.right_neighbors:
            self.right_neighbors.remove(neighbor)
        if neighbor in self.left_neighbors:
            self.left_neighbors.remove(neighbor)
        if neighbor in self.up_neighbors:
            self.up_neighbors.remove(neighbor)
        if neighbor in self.down_neighbors:
            self.down_neighbors.remove(neighbor)

    def __str__(self) -> str:
        str_list = []
        pin_index = self.pin.pin_index_in_net if self.is_pin else -1
        str_list.append(
            f"ConverterNode(id: {self.index}, x:{self.x}, y:{self.y}, is_pin:{self.is_pin}, pin_index: {pin_index})")
        str_list.append("Right Neighbors:")
        for neighbor in self.right_neighbors:
            str_list.append(f"  {neighbor.index}: {neighbor.x}, {neighbor.y}")
        str_list.append("Left Neighbors:")
        for neighbor in self.left_neighbors:
            str_list.append(f"  {neighbor.index}: {neighbor.x}, {neighbor.y}")
        str_list.append("Up Neighbors:")
        for neighbor in self.up_neighbors:
            str_list.append(f"  {neighbor.index}: {neighbor.x}, {neighbor.y}")
        str_list.append("Down Neighbors:")
        for neighbor in self.down_neighbors:
            str_list.append(f"  {neighbor.index}: {neighbor.x}, {neighbor.y}")
        return "\n".join(str_list)

    def get_pin(self) -> Pin:
        if not self.is_pin:
            raise ValueError("Node is not a pin")
        return self.pin

    def initialize_neighbors(self,
                             h2v_nodes: List["ConverterNode"],
                             v2h_nodes: List["ConverterNode"]) -> None:
        for node in h2v_nodes:
            if node.x >= self.x:
                self.right_neighbors.append(node)
            else:
                self.left_neighbors.append(node)
        for node in v2h_nodes:
            if node.y >= self.y:
                self.up_neighbors.append(node)
            else:
                self.down_neighbors.append(node)
        self.right_neighbors.sort(key=lambda node: node.x)
        self.left_neighbors.sort(key=lambda node: node.x, reverse=True)
        self.up_neighbors.sort(key=lambda node: node.y)
        self.down_neighbors.sort(key=lambda node: node.y, reverse=True)
        
    def add_horizontal_neighbor(self, neighbor: "ConverterNode") -> None:
        if neighbor.x > self.x:
            self.add_right_neighbor(neighbor)
        else:
            self.add_left_neighbor(neighbor)
            
    def add_vertical_neighbor(self, neighbor: "ConverterNode") -> None:
        if neighbor.y > self.y:
            self.add_up_neighbor(neighbor)
        else:
            self.add_down_neighbor(neighbor)

    def add_right_neighbor(self, neighbor: "ConverterNode") -> None:
        if neighbor.x < self.x:
            raise ValueError("Neighbor is not to the right")
        assert neighbor not in self.right_neighbors
        for i in range(len(self.right_neighbors) - 1, -1, -1):
            if self.right_neighbors[i].x <= neighbor.x:
                self.right_neighbors.insert(i + 1, neighbor)
                return
        # If the neighbor is the first right neighbor
        self.right_neighbors.insert(0, neighbor)
    
    def add_left_neighbor(self, neighbor: "ConverterNode") -> None:
        if neighbor.x > self.x:
            raise ValueError("Neighbor is not to the left")
        assert neighbor not in self.left_neighbors
        for i in range(len(self.left_neighbors) - 1, -1, -1):
            if self.left_neighbors[i].x >= neighbor.x:
                self.left_neighbors.insert(i + 1, neighbor)
                return
        # If the neighbor is the first left neighbor
        self.left_neighbors.insert(0, neighbor)
    
    def add_up_neighbor(self, neighbor: "ConverterNode") -> None:
        if neighbor.y < self.y:
            raise ValueError("Neighbor is not to the up")
        assert neighbor not in self.up_neighbors
        for i in range(len(self.up_neighbors) - 1, -1, -1):
            if self.up_neighbors[i].y <= neighbor.y:
                self.up_neighbors.insert(i + 1, neighbor)
                return
        # If the neighbor is the first up neighbor
        self.up_neighbors.insert(0, neighbor)
            
    def add_down_neighbor(self, neighbor: "ConverterNode") -> None:
        if neighbor.y > self.y:
            raise ValueError("Neighbor is not to the down")
        assert neighbor not in self.down_neighbors
        for i in range(len(self.down_neighbors) - 1, -1, -1):
            if self.down_neighbors[i].y >= neighbor.y:
                self.down_neighbors.insert(i + 1, neighbor)
                return
        # If the neighbor is the first down neighbor
        self.down_neighbors.insert(0, neighbor)
        

class EdgeType(Enum):
    H2V_RIGHT = 0
    H2V_LEFT = 1
    V2H_UP = 2
    V2H_DOWN = 4
    UNKNOW = 5


class SteinerCandidate:
    def __init__(self,
                 gain: int=0,
                 x: int=0,
                 y: int=0,
                 node: ConverterNode=None,
                 op_node1: ConverterNode=None,
                 op_node2: ConverterNode=None,
                 edge_type: EdgeType=EdgeType.UNKNOW):
        self.update(gain, x, y, node, op_node1, op_node2, edge_type)

    def update(self,
               gain: int,
               x: int,
               y: int,
               node: ConverterNode,
               op_node1: ConverterNode,
               op_node2: ConverterNode,
               edge_type: EdgeType):
        self.gain = gain
        self.x = x
        self.y = y
        self.node = node
        self.op_node1 = op_node1
        self.op_node2 = op_node2
        self.edge_type = edge_type

class TreeConverter:
    def __init__(self, restree: RESTree):
        self.restree: RESTree = restree
        
    def initialize_nodes(self) -> None:
        self.nodes: List[ConverterNode] = []
        for i in range(self.restree.n_pins):
            self.nodes.append(
                ConverterNode(i, 
                              self.restree.x(i), 
                              self.restree.y(i), 
                              True, 
                              self.restree.pins[i]))
            
    def initialize_edges(self) -> None:
        h2v_nodes_list = [[] for _ in range(self.restree.n_pins)]
        v2h_nodes_list = [[] for _ in range(self.restree.n_pins)]
        for nv, nh in self.restree.res:
            h2v_nodes_list[nh].append(self.nodes[nv])
            v2h_nodes_list[nv].append(self.nodes[nh])
        for i in range(self.restree.n_pins):
            self.nodes[i].initialize_neighbors(
                h2v_nodes_list[i], v2h_nodes_list[i])
            
    def convert_to_steiner_restree(self) -> RESTree:
        self.initialize_nodes()
        self.initialize_edges()
        self.steinerize()
        
        res = []
        pins: Pin = []
        for node in self.nodes:
            if node.is_pin:
                pins.append(node.get_pin())
            else:
                pins.append(Pin(-1, node.index, node.x, node.y, 0, 0, False, 0, 0, "", ""))
            for neighbor in node.up_neighbors:
                res.append([node.index, neighbor.index])
            for neighbor in node.down_neighbors:
                res.append([node.index, neighbor.index])
        
        return RESTree(0, pins, RES(res))
        
    def convert_to_steiner_graph(self) -> SteinerGraph:
        self.initialize_nodes()
        self.initialize_edges()
        self.steinerize()
        steiner_graph = self.to_steiner_graph()
        return steiner_graph
    
    def convert_to_steiner_tree(self) -> SteinerTree:
        steiner_graph = self.convert_to_steiner_graph()
        steiner_graph = self.split_degree_4_nodes(steiner_graph)
        parent_map: Dict[int, int] = {}
        start_node = steiner_graph[self.restree.driver_index]
        parent_map[start_node.index] = start_node.index
        length = self.run_dfs(start_node, parent_map)
        branches: List[SteinerTreeBranch] = []
        for node in steiner_graph:
            branches.append(SteinerTreeBranch(node.x, node.y, parent_map[node.index]))
        return SteinerTree(self.restree.n_pins, length, branches)
        
    def run_dfs(self, node: SteinerNode, parent_map: Dict[int, int]) -> int:
        length = 0
        for neighbor in node.neighbors:
            if neighbor.index in parent_map:
                continue
            parent_map[neighbor.index] = node.index
            length += abs(node.x - neighbor.x) + abs(node.y - neighbor.y)
            length += self.run_dfs(neighbor, parent_map)
        return length        

    def best_steiner_for_node(self, node: ConverterNode) -> SteinerCandidate:
        best_gain = 0
        best = SteinerCandidate()
        
        if len(node.right_neighbors) >= 2:
            n1 = node.right_neighbors[-1]
            n2 = node.right_neighbors[-2]
            gain = n2.x - node.x
            if gain > best_gain:
                best_gain = gain
                best.update(gain, n2.x, node.y, node, n1, n2, EdgeType.H2V_RIGHT)
                
        if len(node.left_neighbors) >= 2:
            n1 = node.left_neighbors[-1]
            n2 = node.left_neighbors[-2]
            gain = node.x - n2.x
            if gain > best_gain:
                best_gain = gain
                best.update(gain, n2.x, node.y, node, n1, n2, EdgeType.H2V_LEFT)
                
        if len(node.up_neighbors) >= 2:
            n1 = node.up_neighbors[-1]
            n2 = node.up_neighbors[-2]
            gain = n2.y - node.y
            if gain > best_gain:
                best_gain = gain
                best.update(gain, node.x, n2.y, node, n1, n2, EdgeType.V2H_UP)
                
        if len(node.down_neighbors) >= 2:
            n1 = node.down_neighbors[-1]
            n2 = node.down_neighbors[-2]
            gain = node.y - n2.y
            if gain > best_gain:
                best_gain = gain
                best.update(gain, node.x, n2.y, node, n1, n2, EdgeType.V2H_DOWN)
        return best

    def steinerize(self) -> None:
        from allrest.utils.priorityqueue import PriorityQueue
        pq: PriorityQueue = PriorityQueue()
        node2steiner = {}
        
        for node in self.nodes:
            best = self.best_steiner_for_node(node)
            pq.add_task(node, -best.gain)
            node2steiner[node] = best
            
        while not pq.empty():
            best: SteinerCandidate = node2steiner[pq.pop_task()]
            
            if best.gain <= 0:
                break
            
            node: ConverterNode = best.node
            op1 = best.op_node1
            op2 = best.op_node2
            
            new_node = False
            steiner_node = None

            if best.x == op1.x and best.y == op1.y:
                steiner_node = op1
            elif best.x == op2.x and best.y == op2.y:
                steiner_node = op2
            else:
                steiner_node = ConverterNode(len(self.nodes), best.x, best.y, False, None)
                self.nodes.append(steiner_node)
                new_node = True
            
            if best.edge_type == EdgeType.V2H_UP or best.edge_type == EdgeType.V2H_DOWN:
                if steiner_node != op1:
                    op1.remove_neighbor(node)
                    op1.add_horizontal_neighbor(steiner_node)
                    steiner_node.add_vertical_neighbor(op1)
                    node.remove_neighbor(op1)
                if steiner_node != op2:
                    op2.remove_neighbor(node)
                    op2.add_horizontal_neighbor(steiner_node)
                    steiner_node.add_vertical_neighbor(op2)
                    node.remove_neighbor(op2)
                if new_node:
                    node.add_vertical_neighbor(steiner_node)
                    steiner_node.add_horizontal_neighbor(node)
                    new_best_steiner = self.best_steiner_for_node(steiner_node)
                    node2steiner[steiner_node] = new_best_steiner
                    pq.add_task(steiner_node, -new_best_steiner.gain)
            else:
                if steiner_node != op1:
                    op1.remove_neighbor(node)
                    op1.add_vertical_neighbor(steiner_node)
                    steiner_node.add_horizontal_neighbor(op1)
                    node.remove_neighbor(op1)
                if steiner_node != op2:
                    op2.remove_neighbor(node)
                    op2.add_vertical_neighbor(steiner_node)
                    steiner_node.add_horizontal_neighbor(op2)
                    node.remove_neighbor(op2)
                if new_node:
                    node.add_horizontal_neighbor(steiner_node)
                    steiner_node.add_vertical_neighbor(node)
                    new_best_steiner = self.best_steiner_for_node(steiner_node)
                    node2steiner[steiner_node] = new_best_steiner
                    pq.add_task(steiner_node, -new_best_steiner.gain)
                    
            new_best_nd = self.best_steiner_for_node(node)
            node2steiner[node] = new_best_nd
            pq.add_task(node, -new_best_nd.gain)
            
            new_best_op1 = self.best_steiner_for_node(op1)
            node2steiner[op1] = new_best_op1
            pq.add_task(op1, -new_best_op1.gain)
            
            new_best_op2 = self.best_steiner_for_node(op2)
            node2steiner[op2] = new_best_op2
            pq.add_task(op2, -new_best_op2.gain)
            
    def to_steiner_graph(self) -> SteinerGraph:
        graph_nodes: List[SteinerNode] = []
        node_map: Dict[ConverterNode, SteinerNode] = {}
        for node in self.nodes:
            graph_node = SteinerNode(node.index, node.x, node.y, node.is_pin, node.pin)
            graph_nodes.append(graph_node)
            node_map[node] = graph_node
            
        for convnode, graphnode in zip(self.nodes, graph_nodes):
            for neighbor in convnode.up_neighbors:
                graphnode.add_neighbor(node_map[neighbor])
            for neighbor in convnode.down_neighbors:
                graphnode.add_neighbor(node_map[neighbor])
            for neighbor in convnode.left_neighbors:
                graphnode.add_neighbor(node_map[neighbor])
            for neighbor in convnode.right_neighbors:
                graphnode.add_neighbor(node_map[neighbor])
        return SteinerGraph(graph_nodes)
    
    def split_degree_4_nodes(self, steiner_graph: SteinerGraph) -> SteinerGraph:
        from collections import deque
        queue = deque()
        for node in steiner_graph:
            queue.append(node)
        
        while len(queue) > 0:
            node: SteinerNode = queue.popleft()
            if len(node.neighbors) <= 3:
                continue
            new_node = SteinerNode(len(steiner_graph), node.x, node.y, False, None)
            steiner_graph.add_node(new_node)
            
            next_neighbor_nodes = []
            for idx, neighbor_node in enumerate(node.neighbors):
                if idx <= 1:
                    next_neighbor_nodes.append(neighbor_node)
                    continue
                if node in neighbor_node.neighbors:
                    neighbor_node.neighbors.remove(node)
                neighbor_node.neighbors.append(new_node)
                new_node.neighbors.append(neighbor_node)
            node.neighbors = next_neighbor_nodes
            node.neighbors.append(new_node)
            new_node.neighbors.append(node)
            queue.append(new_node)
        return steiner_graph
    
def convert_to_steiner_graph(restree: RESTree) -> SteinerGraph:
    return TreeConverter(restree).convert_to_steiner_graph()


if __name__ == "__main__":
    from allrest.res import RES
    from allrest.pin import Pin
    from allrest.utils.test import generate_random_restree
    restree = generate_random_restree()
    from allrest.utils.render import render_RES
    render_RES(restree.res.to_1d(), restree.x_list(), restree.y_list(),
               driver_index=restree.driver_index, filepath="test.png")
    restree2 = TreeConverter(restree).convert_to_steiner_restree()
    render_RES(restree2.res.to_1d(), restree2.x_list(), restree2.y_list(),
               driver_index=restree2.driver_index, filepath="test2.png")
    

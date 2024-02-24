from allrest.restreeabstractevaluator import RESTreeAbstractEvaluator
from allrest.restree import RESTree
from allrest.utils.nearestneighbors import get_nearest_neighbors
from typing import List, Callable, Tuple
from allrest.utils.unionfind import UnionFind
import copy


class RESTreeOptimizer:
    def __init__(self, evaluator: RESTreeAbstractEvaluator):
        self.evaluator: RESTreeAbstractEvaluator = evaluator
        
    def get_nearest_neighbor(self, restree: RESTree) -> List[List[int]]:
        x = restree.x_list()
        y = restree.y_list()
        return get_nearest_neighbors(x, y)
    
    def optimize(self, restree: RESTree) -> Tuple[RESTree, float]:
        prev_cost = self.evaluator.get_cost(restree)
        N = restree.n_pins
        best_RES = copy.deepcopy(restree.res)
        nearest_neighbors = self.get_nearest_neighbor(restree)
        
        best_cost = prev_cost
        best_delete = None
        best_add = None
        
        while True:
            prev_cost = best_cost
            for elem in best_RES:
                new_res = copy.deepcopy(best_RES)
                new_res.remove(elem)
                
                dv, dh = elem
                
                # Initialize segments
                x = restree.x_list()
                y = restree.y_list()
                x_low = copy.copy(x)
                x_high = copy.copy(x)
                y_low = copy.copy(y)
                y_high = copy.copy(y)
                
                unionfind = UnionFind(N)
                
                for nv, nh in new_res:
                    x_low[nh] = min(x_low[nh], x[nv])
                    x_high[nh] = max(x_high[nh], x[nv])
                    y_low[nv] = min(y_low[nv], y[nh])
                    y_high[nv] = max(y_high[nv], y[nh])
                    unionfind.union(nv, nh)
                    
                for nv in range(N):
                    for nh in nearest_neighbors[nv]:
                        if unionfind.connected(nv, nh):
                            continue
                        new_res.append([nv, nh])
                        new_restree = RESTree(restree.net_id, restree.pins, new_res)
                        new_cost = self.evaluator.get_cost(new_restree)
                        if new_cost < best_cost:
                            best_cost = new_cost
                            best_delete = elem
                            best_add = [nv, nh]
                        new_res.pop()
            if best_cost < prev_cost:
                best_RES.remove(best_delete)
                best_RES.append(best_add)
            else:
                break
        return RESTree(restree.net_id, restree.pins, best_RES), best_cost


class MessageHandler:
    def __init__(self):
        self.message = []
        
    def callback(self, name, cost, msg):
        self.message.append((name, cost, msg))
        
    def get_message(self):
        message_strs = []
        name_length = 0
        for name, cost, msg in self.message:
            name_length = max(name_length, len(name))
        
        for name, cost, msg in self.message:
            message_strs.append(f"{name:<{name_length}}: {cost:.3g} {msg}")
            
        return "\n".join(message_strs)

if __name__ == "__main__":
    from allrest.utils.test import generate_random_restree
    from allrest.restreelengthevaluator import RESTreeLengthEvaluator
    from allrest.restreedetourevaluator import RESTreeDetourEvaluator
    from allrest.restreeoverflowevaluator import RESTreeOverflowEvaluator
    from allrest.restreeweightedevaluator import RESTreeWeightedEvaluator
    from allrest.restreecompositeevaluator import RESTreeCompositeEvaluator
    from allrest.overflowmanager import OverflowManager
    from allrest.utils.test import generate_random_restree, generate_random_overflow_manager
    from allrest.utils.render import render_RESTree
    
    nx = 20
    ny = 10
    
    for i in range(1):
        ofm: OverflowManager = generate_random_overflow_manager(nx=nx, ny=ny)
        restree: RESTree = generate_random_restree(ny=ny, nx=nx, slack_mean=0, slack_std=10e-12)
        evaluators = [RESTreeLengthEvaluator(), RESTreeDetourEvaluator(), RESTreeOverflowEvaluator(ofm)]
        weights = [0.1, 1.0, 0.5]
        weighted_evaluators = [RESTreeWeightedEvaluator(evaluator, weight) for evaluator, weight in zip(evaluators, weights)]
            
        composite_evaluator = RESTreeCompositeEvaluator(evaluators=weighted_evaluators)
        message_handler = MessageHandler()
        composite_evaluator.get_cost(restree, message_handler.callback)
        render_RESTree(restree, message_handler.get_message(), f"restree{i}_a.png", overflow_manager=ofm)
        
        
        restree_new = RESTreeOptimizer(composite_evaluator).optimize(restree)
        message_handler = MessageHandler()
        composite_evaluator.get_cost(restree_new, message_handler.callback)
        render_RESTree(restree_new, message_handler.get_message(), f"restree{i}_b.png", overflow_manager=ofm)
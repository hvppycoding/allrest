from typing import List


class SteinerTreeBranch:
    def __init__(self, x, y, n):
        self.x = x
        self.y = y
        self.n = n
        
class SteinerTree:
    def __init__(self, deg: int, length: int, branch: List[SteinerTreeBranch]):
        self.deg: int = deg
        self.length: int = length
        self.branch: List[SteinerTreeBranch] = branch
        
    def branchCount(self) -> int:
        return len(self.branch)
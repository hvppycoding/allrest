from typing import List, Tuple, Union


class RES:
    def __init__(self, RES: List[Union[list, tuple, int]]=None) -> None:
        if not isinstance(RES, list):
            raise TypeError("RES must be a list")
        if not all(isinstance(i, (list, tuple, int)) for i in RES):
            raise TypeError("RES must be a list of lists or integers")
        
        self.RES: List[List[int]] = []
        
        if all(isinstance(i, int) for i in RES):
            self.initialize_from_1d(RES)
        elif all(isinstance(i, (list, tuple)) for i in RES):
            self.initialize_from_2d(RES)
        else:
            # RES not initialized
            pass
        
    def check_type(self, value: List[int]) -> None:
        if not isinstance(value, list):
            raise TypeError("value must be a list")
        if not all(isinstance(i, int) for i in value):
            raise TypeError("value must be a list of integers")
        if not len(value) == 2:
            raise ValueError("value must be a list of length 2")
        
    def __getitem__(self, index: int) -> List[int]:
        return self.RES[index]
    
    def __setitem__(self, index: int, value: List[int]) -> None:
        self.check_type(value)
        self.RES[index] = value
        
    def pop(self, index: int=-1) -> List[int]:
        return self.RES.pop(index)
        
    def remove(self, value: List[int]) -> None:
        self.check_type(value)
        self.RES.remove(value)
        
    def insert(self, index: int, value: List[int]) -> None:
        self.check_type(value)
        self.RES.insert(index, value)
        
    def remove_index(self, index: int) -> None:
        del self.RES[index]
        
    def __delitem__(self, index: int) -> None:
        del self.RES[index]
        
    def __len__(self) -> int:
        return len(self.RES)
    
    def __iter__(self) -> List[int]:
        return iter(self.RES)
    
    def append(self, value: List[int]) -> None:
        self.check_type(value)
        self.RES.append(value)
    
    def initialize_from_1d(self, RES: List[int]) -> None:
        if not isinstance(RES, list):
            raise TypeError("RES must be a list")
        if not all(isinstance(i, int) for i in RES):
            raise TypeError("RES must be a list of lists or integers")
        self.RES = []
        for nv, nh in zip(RES[::2], RES[1::2]):
            self.append([nv, nh])
        
    def initialize_from_2d(self, RES: List[List[int]]) -> None:
        if not isinstance(RES, list):
            raise TypeError("RES must be a list")
        if not all(isinstance(i, (list, tuple)) for i in RES):
            raise TypeError("RES must be a list of lists or integers")
        self.RES = []
        for nv, nh in RES:
            self.append([nv, nh])
            
    def to_1d(self) -> List[int]:
        return [i for sublist in self.RES for i in sublist]
from allrest.res import RES
from allrest.pin import Pin
from typing import List


class RESTree:
    def __init__(self, net_id: int, pins: List[Pin], res: RES):    
        if len(pins) != len(res) + 1:
            raise ValueError("Number of pins and number of res do not match")
        for i, pin in enumerate(pins):
            if pin.pin_index_in_net != i:
                raise ValueError("Pin index does not match index")
        
        self.driver_index = -1
        for i, pin in enumerate(pins):
            if pin.is_driver:
                if self.driver_index != -1:
                    raise ValueError("More than one driver")
                self.driver_index = i
            
        self.net_id = net_id
        self.n_pins = len(pins)
        self.pins: List[Pin] = pins
        self.res = res
        self._x: List[int] = []
        self._y: List[int] = []
        self._x_low: List[int] = []
        self._x_high: List[int] = []
        self._y_low: List[int] = []
        self._y_high: List[int] = []
        self._length: int = 0
        self.initialize()
        
    def initialize(self) -> None:
        self._x = [pin.x for pin in self.pins]
        self._y = [pin.y for pin in self.pins]
        self._x_low = self._x.copy()
        self._x_high = self._x.copy()
        self._y_low = self._y.copy()
        self._y_high = self._y.copy()
        
        for nv, nh in self.res:
            self._x_low[nh] = min(self._x_low[nh], self._x[nv])
            self._x_high[nh] = max(self._x_high[nh], self._x[nv])
            self._y_low[nv] = min(self._y_low[nv], self._y[nh])
            self._y_high[nv] = max(self._y_high[nv], self._y[nh])
        
        self._length = 0
        for i in range(self.n_pins):
            self._length += self._x_high[i] - self._x_low[i] + self._y_high[i] - self._y_low[i]
        
    def x_low(self, index: int) -> int:
        return self._x_low[index]
    
    def x_high(self, index: int) -> int:
        return self._x_high[index]
    
    def y_low(self, index: int) -> int:
        return self._y_low[index]
    
    def y_high(self, index: int) -> int:
        return self._y_high[index]
    
    def length(self) -> int:
        return self._length

    def x(self, index: int) -> int:
        return self.pins[index].x
    
    def y(self, index: int) -> int:
        return self.pins[index].y
    
    def x_list(self) -> List[int]:
        return [pin.x for pin in self.pins]
    
    def y_list(self) -> List[int]:
        return [pin.y for pin in self.pins]
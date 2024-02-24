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
        
    def x(self, index: int) -> int:
        return self.pins[index].x
    
    def y(self, index: int) -> int:
        return self.pins[index].y
    
    def x_list(self) -> List[int]:
        return [pin.x for pin in self.pins]
    
    def y_list(self) -> List[int]:
        return [pin.y for pin in self.pins]
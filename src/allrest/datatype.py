from typing import List, Dict, Set, Tuple
from numpy.typing import NDArray
from allrest.utils import outputmanager
from allrest.datatype import *
from allrest.restree import RESTree
import copy


class TDCell:
    def __init__(self):
        self.cell_id = 0
        self.is_sequential: bool = False
        self.fanin_pins: List[int] = []
        self.fanout_pins: List[int] = []

class TDPin:
    def __init__(self):
        self.pin_id = 0
        self.x = 0
        self.y = 0
        self.arriaval_time = 0
        self.slack = 0
        self.net_id = 0
        self.cell_id = 0
        self.cell_name = ""
        self.pin_name = ""
        self.is_driver: bool = False

class TDNet:
    def __init__(self, net_id: int, driver_index: int):
        self.net_id: int = net_id
        self.driver_index: int = driver_index
        self.pins: List[TDPin] = []
        self.RES: List[int] = []
        
    def add_pin(self, pin: TDPin):
        self.pins.append(pin)
        
    def get_pin_by_id(self, pin_id: int):
        for pin in self.pins:
            if pin.pin_id == pin_id:
                return pin
        return None
    
    def get_pin_index(self, pin_id: int):
        for i, pin in enumerate(self.pins):
            if pin.pin_id == pin_id:
                return i
        return -1

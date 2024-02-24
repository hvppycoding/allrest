from allrest.forestoptimizer import ForestOptimizer
from allrest.res import RES
from allrest.overflowmanager import OverflowManager
import numpy as np
from numpy.typing import NDArray
from typing import Dict
from allrest.datatype import *
import os


class ForestOptimizerBuilder:
    def read_vcapacity(self, input_file: str) -> NDArray:
        with open(input_file, 'r') as f:
            lines = f.readlines()
            i = 0
            while i < len(lines):
                line = lines[i].strip().upper()
                if line.startswith("VCAP"):
                    ny = int(line.split()[1])
                    nx = int(line.split()[2])
                    vcap = np.zeros((ny, nx), dtype=np.int32)
                    
                    for y in range(ny):
                        i += 1
                        for x, token in enumerate(lines[i].strip().split()):
                            v = int(token)
                            vcap[y, x] = v
                            
                    return vcap
                else:
                    i += 1
        raise ValueError("VCAP not found")
    
    def read_hcapacity(self, input_file: str) -> NDArray:
        with open(input_file, 'r') as f:
            lines = f.readlines()
            i = 0
            while i < len(lines):
                line = lines[i].strip().upper()
                if line.startswith("HCAP"):
                    ny = int(line.split()[1])
                    nx = int(line.split()[2])
                    hcap = np.zeros((ny, nx), dtype=np.int32)
                    
                    for y in range(ny):
                        i += 1
                        for x, token in enumerate(lines[i].strip().split()):
                            v = int(token)
                            hcap[y, x] = v
                            
                    return hcap
                else:
                    i += 1
        raise ValueError("HCAP not found")
    
    def read_netlist(self, input_file: str):
        nets: Dict[int, TDNet] = {}
        cells: Dict[int, TDCell] = {}
        pins: Dict[int, TDPin] = {}
        
        with open(input_file, 'r') as f:
            lines = f.readlines()
            i = 0
            while i < len(lines):
                line = lines[i].strip().upper()
                if line.startswith("VCAP"):
                    i += 1
                    ny = int(line.split()[1])
                    i += ny
                elif line.startswith("HCAP"):
                    i += 1
                    ny = int(line.split()[1])
                    i += ny
                elif line.startswith("NET"):
                    net_id = int(line.split()[1])
                    npins = int(line.split()[3])
                    drv_idx = -1
                    if len(line.split()) > 5:
                        drv_idx = int(line.split()[5])
                    net = TDNet(net_id, driver_index=drv_idx)
                    for j in range(npins):
                        i += 1
                        tokens = lines[i].split()
                        # ID X Y IS_DRIVER ARRIVAL_TIME SLACK CELL_ID IS_SEQUENTIAL PIN_NAME CELL_NAME
                        # 1563 25 13 0 1.59701e-10 2.55974e-10 269 1 D _561_
                        pin_id = int(tokens[0])
                        x = int(tokens[1])
                        y = int(tokens[2])
                        is_driver = tokens[3] == "1"
                        arrival_time = float(tokens[4])
                        slack = float(tokens[5])
                        cell_id = int(tokens[6])
                        is_sequential = tokens[7] == "1"
                        pin_name = tokens[8]
                        cell_name = tokens[9]
                        if cell_id not in cells:
                            cell = TDCell()
                            cell.cell_id = cell_id
                            cells[cell_id] = cell
                            cell.is_sequential = is_sequential
                        cell = cells[cell_id]
                        if is_driver:
                            cell.fanout_pins.append(pin_id)
                        else:
                            cell.fanin_pins.append(pin_id)
                        
                        pin = TDPin()
                        pin.pin_id = pin_id
                        pin.x = x
                        pin.y = y
                        pin.is_driver = is_driver
                        pin.arriaval_time = arrival_time
                        pin.slack = slack
                        pin.cell_id = cell_id
                        pin.cell_name = cell_name
                        pin.pin_name = pin_name
                        pin.net_id = net_id
                        pins[pin_id] = pin
                        net.add_pin(pin)
                    i += 1
                    nets[net_id] = net
                else:
                    print("Unknown line:", line)
                    i += 1
        return nets, cells, pins
    
    def create_restrees(self, input_file: str, res_file: str=None) -> List[RESTree]:
        from allrest.pin import Pin
        self.input_file = input_file
        nets, cells, pins = self.read_netlist(input_file)
        
        restree_infos = []

        rest_inputs: List[List[List[int]]] = []
        for net_id, net in nets.items():
            pins: List[Pin] = []
            rest_input = []
            for pin_index, tdpin in enumerate(net.pins):
                pin_id = tdpin.pin_id
                pin = Pin(pin_id, 
                          pin_index, 
                          tdpin.x, 
                          tdpin.y, 
                          tdpin.arriaval_time, 
                          tdpin.slack, 
                          tdpin.is_driver, 
                          tdpin.net_id, 
                          tdpin.cell_id,
                          tdpin.cell_name, 
                          tdpin.pin_name)
                pins.append(pin)
                rest_input.append([pin.x, pin.y])
            restree_info = (net_id, pins)
            restree_infos.append(restree_info)
            rest_inputs.append(rest_input)
        
        res_list: List[List[int]] = []
        if res_file and os.path.exists(res_file):
            outputmanager.info("Reading res file:", res_file)
            with open(res_file, 'r') as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    line = line.strip()
                    net_id, res_1d_str = line.split(":")
                    net_id = int(net_id)
                    res_1d = [int(x) for x in res_1d_str.split()]
                    if net_id != restree_infos[i][0]:
                        raise ValueError("Net ID mismatch")
                    if len(res_1d) != 2 * len(restree_infos[i][1]) - 2:
                        raise ValueError("RES length mismatch")
                    res_list.append(res_1d)
        else:
            outputmanager.info("Running REST")
            from allrest.rest.wrapper import run_rest
            res_list = run_rest(input_data=rest_inputs, heuristic_2pin=True)
            
        restrees: List[RESTree] = []
        for restree_info, res_1d in zip(restree_infos, res_list):
            res = RES(res_1d)
            restree = RESTree(restree_info[0], restree_info[1], res)
            restrees.append(restree)
        
        return restrees
    
    def create_overflow_manager(self, input_file: str) -> OverflowManager:
        hcapacity = self.read_hcapacity(input_file)
        vcapacity = self.read_vcapacity(input_file)
        ofm = OverflowManager(hcapacity=hcapacity, vcapacity=vcapacity)
        return ofm
    
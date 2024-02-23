import numpy as np
from numpy.typing import NDArray
from allrest.utils import outputmanager


class OverflowManager:
    def __init__(self, vcapacity: NDArray, hcapacity: NDArray):
        self.nx = max(vcapacity.shape[1], hcapacity.shape[1])
        self.ny = max(vcapacity.shape[0], hcapacity.shape[0])
        self.vcapacity_map: NDArray = np.zeros((self.ny, self.nx))
        self.hcapacity_map: NDArray = np.zeros((self.ny, self.nx))
        self.vusage_map: NDArray = np.zeros((self.ny, self.nx))
        self.husage_map: NDArray = np.zeros((self.ny, self.nx))
        self.vcapacity_map[:vcapacity.shape[0], :vcapacity.shape[1]] = vcapacity
        self.hcapacity_map[:hcapacity.shape[0], :hcapacity.shape[1]] = hcapacity
        self.hoverflow_count_sum = None
        self.voverflow_count_sum = None
        self.is_dirty = False
        
    @staticmethod
    def cumsum_pad(arr, axis: int=0):
        csum = np.insert(arr, obj=0, values=0, axis=axis)
        csum.cumsum(out=csum, axis=axis)
        return csum
        
    def update_overflows(self):
        outputmanager.info("CongestionManager: Updating overflows")
        hoverflow_map = np.zeros_like(self.husage_map, dtype=np.int32)
        hoverflow_map[self.husage_map > self.hcapacity_map] = 1
        voverflow_map = np.zeros_like(self.vusage_map, dtype=np.int32)
        voverflow_map[self.vusage_map > self.vcapacity_map] = 1
        
        self.hoverflow_count_sum = OverflowManager.cumsum_pad(hoverflow_map, axis=1)
        self.voverflow_count_sum = OverflowManager.cumsum_pad(voverflow_map, axis=0)
        self.is_dirty = False
    
    def count_voverflow(self, x: int, yl: int, yh: int):
        if self.voverflow_count_sum is None:
            self.update_overflows()
        if self.is_dirty:
            self.update_overflows()
        return self.voverflow_count_sum[yh, x] - self.voverflow_count_sum[yl, x]
    
    def count_hoverflow(self, y: int, xl: int, xh: int):
        if self.hoverflow_count_sum is None:
            self.update_overflows()
        if self.is_dirty:
            self.update_overflows()
        return self.hoverflow_count_sum[y, xh] - self.hoverflow_count_sum[y, xl]
    
    def change_vusage(self, x: int, yl: int, yh: int, usage: int=1):
        self.vusage_map[yl:yh, x] += usage
        self.is_dirty = True
        
    def change_husage(self, y: int, xl: int, xh: int, usage: int=1):
        self.husage_map[y, xl:xh] += usage
        self.is_dirty = True
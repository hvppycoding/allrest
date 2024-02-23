from typing import List
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from allrest.overflowmanager import OverflowManager
from allrest.restree import RESTree


def line_collection_from_overflows(overflow_manager: OverflowManager, lx: int, rx: int, ly: int, ry: int):
    rx = min(overflow_manager.nx, rx)
    ry = min(overflow_manager.ny, ry)
    lx = max(0, lx)
    ly = max(0, ly)
    
    lines = []
    colors = []
    
    for x in range(lx, rx + 1):
        for y in range(ly, ry + 1):
            lines.append(((x + 0.5, y - 0.5), (x + 0.5, y + 0.5)))
            if overflow_manager.husage_map[y, x] > overflow_manager.hcapacity_map[y, x]:
                colors.append("red")
            else:
                colors.append("black")
            
            lines.append(((x - 0.5, y + 0.5), (x + 0.5, y + 0.5)))
            if overflow_manager.vusage_map[y, x] > overflow_manager.vcapacity_map[y, x]:
                colors.append("red")
            else:
                colors.append("black")
    
    return LineCollection(lines, linewidths=1, colors=colors, linestyle='solid')


def render_RES(RES1D: List[int], 
               x: List[int],
               y: List[int],
               driver_index: int, 
               critical_index: List[int]=None,
               filepath: str=None,
               overflow_manager: OverflowManager=None):
    fig, ax = plt.subplots(figsize=(8, 8))
    
    if critical_index is None:
        critical_index = []
    
    min_x = min(x)
    max_x = max(x)
    min_y = min(y)
    max_y = max(y)
    
    if overflow_manager is not None:
        ax.add_collection(line_collection_from_overflows(overflow_manager, min_x, max_x, min_y, max_y))
    
    res_lines = []
    for nv, nh in zip(RES1D[::2], RES1D[1::2]):
        x1 = x[nv]
        x2 = x[nh]
        y1 = y[nv]
        y2 = y[nh]

        res_lines.append(((x1, y1), (x1, y2)))
        res_lines.append(((x1, y2), (x2, y2)))
    
    res_line_segments = LineCollection(res_lines, linewidths=1, colors='blue', linestyle='solid')
    ax.add_collection(res_line_segments)
    
    driver_xs = []
    driver_ys = []    
    critical_xs = []
    critical_ys = []
    pin_xs = []
    pin_ys = []
    for idx, (x, y) in enumerate(zip(x, y)):    
        if idx == driver_index:
            driver_xs.append(x)
            driver_ys.append(y)
        elif idx in critical_index:
            critical_xs.append(x)
            critical_ys.append(y)
        else:
            pin_xs.append(x)
            pin_ys.append(y)
        ax.text(x, y, f"{idx}", fontsize=16, zorder=20)
    ax.scatter(pin_xs, pin_ys, color="black", s=16, marker="s", linewidths=1, edgecolors="black", zorder=10)
    ax.scatter(critical_xs, critical_ys, color="red", s=16, marker="s", linewidths=1, edgecolors="black", zorder=11)
    ax.scatter(driver_xs, driver_ys, color="yellow", s=16, marker="s", linewidths=1, edgecolors="black", zorder=12)
    
    ax.set_xlim(min_x - 1, max_x + 1)
    ax.set_ylim(min_y - 1, max_y + 1)
    # ax.set_title(f"RES: {res_tree.RES}\nWL: {res_tree.real_wirelength:.2f}")
    
    # filepath = outputmanager.get_output_path(filename)
    fig.savefig(filepath)
    fig.clf()
    plt.close(fig)
    
def render_RESTree(restree: RESTree, filepath: str=None, overflow_manager: OverflowManager=None):
    critical_index = []
    for pin in restree.pins:
        if pin.slack < 0:
            critical_index.append(pin.pin_index_in_net)
    render_RES(restree.res.to_1d(), restree.x_list(), restree.y_list(),
               driver_index=restree.driver_index, critical_index=critical_index,
               filepath=filepath, overflow_manager=overflow_manager)
    
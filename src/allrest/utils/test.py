from typing import List, Dict
from allrest.res import RES
from allrest.pin import Pin
from allrest.restree import RESTree


def generate_random_restree(n_pins: int=10, nx: int=10, ny: int=10, slack_mean: float=0, slack_std: float=0) -> RESTree:
    from allrest.rest.wrapper import run_rest
    import numpy as np
    
    x = np.random.randint(low=0, high=nx, size=(n_pins, 1))
    y = np.random.randint(low=0, high=ny, size=(n_pins, 1))
    xy = np.concatenate((x, y), axis=1)
    points = xy.tolist()
    res1d = run_rest([points])[0]
    driver_index = np.random.randint(low=0, high=n_pins)
    pins = []
    
    driver_slack = float("inf")
    for i in range(n_pins):
        if i == driver_index:
            slack = 0
        else:
            slack = np.random.normal(slack_mean, slack_std)
            driver_slack = min(driver_slack, slack)
            
        pins.append(Pin(i, i, points[i][0], points[i][1], 0,
                    slack, i == driver_index, 0, 0, "cell0", f"pin{i}"))
    
    pins[driver_index].slack = driver_slack
    
    res = RES(res1d)
    return RESTree(0, pins, res)

def generate_my_restree() -> RESTree:
    pin_infos = [
        # (id, idx, x, y, at, sl, drv, net_id, cell_id, cell_name, pin_name)
        (100, 0, 105, 35, 0, 0, False, 0, 0, "cell0", "pin0"),
        (101, 1, 115, 30, 0, 0, False, 0, 0, "cell0", "pin1"),
        (102, 2, 100, 10, 0, 0, True, 0, 0, "cell0", "pin2"),
        (103, 3, 103, 30, 0, 0, False, 0, 0, "cell0", "pin3"),
        (103, 4, 110, 15, 0, 0, False, 0, 0, "cell0", "pin4"),
        (103, 5, 105, 20, 0, 0, False, 0, 0, "cell0", "pin5"),
        (103, 6, 105,  9, 0, 0, False, 0, 0, "cell0", "pin6"),
    ]
    pins = []
    for pin_info in pin_infos:
        pins.append(Pin(*pin_info))

    res = RES(
        [[2, 4],
         [3, 4],
         [3, 0],
         [4, 5],
         [4, 1],
         [5, 6]]
    )
    return RESTree(0, pins, res)
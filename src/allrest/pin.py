class Pin:
    def __init__(self, 
                 pin_id: int, 
                 pin_index_in_net: int, 
                 x: int, 
                 y: int, 
                 arrival_time: float, 
                 slack: float, 
                 is_driver: bool, 
                 net_id: int, 
                 cell_id: int, 
                 cell_name: str, 
                 pin_name: str):
        self.pin_id: int = pin_id
        self.pin_index_in_net: int = pin_index_in_net
        self.x: int = x
        self.y: int = y
        self.arrival_time: float = arrival_time
        self.slack: float = slack
        self.is_driver: bool = is_driver
        self.net_id: int = net_id
        self.cell_id: int = cell_id
        self.cell_name: str = cell_name
        self.pin_name: str = pin_name
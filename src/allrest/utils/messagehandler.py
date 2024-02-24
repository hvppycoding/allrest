from typing import Dict


class MessageHandler:
    def __init__(self):
        self.message = []
        
    def callback(self, name, cost, msg):
        self.message.append((name, cost, msg))
        
    def get_message(self):
        message_strs = []
        name_length = 0
        for name, cost, msg in self.message:
            name_length = max(name_length, len(name))
        
        for name, cost, msg in self.message:
            message_strs.append(f"{name:<{name_length}}: {cost:.3g} {msg}")
            
        return "\n".join(message_strs)
    

class MessageAggregateHandler:
    def __init__(self):
        self.cur_net_id = -1
        self.eval_names = []
        self.net_ids = []
        self.score_map: Dict[str, Dict[int, float]] = {}
        
    def set_net_id(self, net_id):
        if net_id not in self.net_ids:
            self.net_ids.append(net_id)
        self.cur_net_id = net_id

    def callback(self, name, cost, msg):
        if name not in self.eval_names:
            self.eval_names.append(name)
            self.score_map[name] = {}
        self.score_map[name][self.cur_net_id] = cost
        
    def get_message(self):
        line = ", ".join(["net_id"] + self.eval_names)
        message_strs = [line]
        
        for net_id in self.net_ids:
            line = [str(net_id)]
            for eval_name in self.eval_names:
                line.append(f"{self.score_map[eval_name][net_id]:.3g}")
            message_strs.append(",".join(line))
        
        for name in self.eval_names:
            line = f"{name}: {sum(self.score_map[name].values()):.3g}"
            message_strs.append(line)
        return "\n".join(message_strs)
        
        
            
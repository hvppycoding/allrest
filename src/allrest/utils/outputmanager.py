import os
import logging
import datetime


class OutputManager:
    def __init__(self):
        self.output_dir = None
        self.log_file_name: str = None
        self.log_level: int = logging.DEBUG
        self.initialized = False
        self.output_dir_created = False
        
    def initialize(self):
        if self.initialized:
            return
        
        if self.output_dir is None:
            name = "output"
            datetime_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            self.output_dir = f"{name}_{datetime_str}"
        
        if self.log_file_name is not None:
            log_file_path = os.path.join(self.output_dir, self.log_file_name)
            self.make_output_dir()
            # create formatter
            fotmat = "%(asctime)s;%(levelname)s;%(message)s"
            datefmt = "%Y-%m-%d %H:%M:%S"
            logging.basicConfig(filename=log_file_path,
                                level=self.log_level,
                                format=fotmat,
                                datefmt=datefmt)
        
        self.initialized = True
        
    def make_output_dir(self):
        if self.output_dir_created:
            return
        os.makedirs(self.output_dir, exist_ok=True)
        self.output_dir_created = True
        
    def get_subfile_path(self, file_name: str = "") -> str:
        self.initialize()
        if not file_name:
            return self.output_dir
        return os.path.join(self.output_dir, file_name)
        
    def write_file(self, file_name: str, content: str):
        self.initialize()
        file_path = os.path.join(self.output_dir, file_name)
        with open(file_path, 'w') as f:
            f.write(content)
        
    def set_output_dir(self, output_dir: str):
        self.output_dir = output_dir
        
    def set_log_level(self, log_level: int):
        self.log_level = log_level
        
    def set_log_file_name(self, log_file_name: str):
        self.log_file_name = log_file_name

    def debug(self, *msg):
        self.initialize()
        s = " ".join([str(x) for x in msg])
        logging.debug(s)
        
    def info(self, *msg):
        self.initialize()
        s = " ".join([str(x) for x in msg])
        logging.info(s)
    
    def warning(self, *msg):
        self.initialize()
        s = " ".join([str(x) for x in msg])
        logging.warning(s)
        
    def error(self, *msg):
        self.initialize()
        s = " ".join([str(x) for x in msg])
        logging.error(s)
        
    def critical(self, *msg):
        self.initialize()
        s = " ".join([str(x) for x in msg])
        logging.critical(s)


root = OutputManager()

def basicConfig(**kwargs):
    output_dir = kwargs.pop("output_dir", None)
    if output_dir is not None:
        root.set_output_dir(output_dir)
       
    log_level = kwargs.pop("log_level", None) 
    if log_level is not None:
        root.set_log_level(log_level)
        
    log_file_name = kwargs.pop("log_file_name", None)
    if log_file_name is not None:
        root.set_log_file_name(log_file_name)

def debug(*msg):
    root.debug(*msg)
    
def info(*msg):
    root.info(*msg)
    
def warning(*msg):
    root.warning(*msg)
    
def error(*msg):
    root.error(*msg)
    
def critical(*msg):
    root.critical(*msg)
    
def get_output_path(file_name: str = "") -> str:
    return root.get_subfile_path(file_name)

def write_file(file_name: str, content: str):
    root.write_file(file_name, content)

import time
from .transport import Transport
from .config import Config
from loguru import logger

class Base(Transport):
    """Base class for all VecDB utilities
    """
    config: Config = Config()
    logger = logger
    def __init__(self, 
        project: str, api_key: str, 
        base_url: str):
        self.project = project
        self.api_key = api_key
        self.base_url = base_url

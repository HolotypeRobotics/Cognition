import os

from .block import Block  # Use relative import for clarity
from .scheduler import Scheduler
from .utils import configurator, files  # Import specific utility functions

class Agent:
    def __init__(self):
        self.initialized = False
        self.hierarchy = None
        self.scheduler = Scheduler()  # Initialize scheduler here
        
    def configure(self, config_path):
        try:
            config_data = files.load_yaml(config_path)
            self.hierarchy.configure(config_data)
            self.scheduler.set_hierarchy(self.hierarchy)
            return True
        except Exception as e:
            print(f"Failed to configure agent: {e}")
            return False
        

    def initialize(self, config_path):

        if not self.configure(config_path):
            raise ValueError("Failed to load configuration")

        self.scheduler = Scheduler(self.hierarchy)

        print("Initializing Cognition")
        # Initialize blocks if necessary

        self.initialized = True

    def run(self):
        """
        Starts the agent's execution loop.
        """
        if not self.initialized:
            raise RuntimeError("Agent not initialized")

        self.scheduler.run()

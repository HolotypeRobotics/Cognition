import os

from .block import Block  # Use relative import for clarity
from .scheduler import Scheduler
from .utils import configurator, files  # Import specific utility functions

class Agent:
    def __init__(self):
        self.initialized = False
        self.config = None
        self.blocks = []
        self.scheduler = None  # Initialize scheduler here
        
    def configure(self, config_path):
        """
        Configures the agent using a configuration file path.

        Args:
            config_path (str): Path to the configuration directory.
        """
        try:
            config_data = configurator.load_configuration(config_path)
            configurator.configure_agent(self, config_data)
            return True
        except Exception as e:
            print(f"Failed to configure agent: {e}")
            return False

    def process_data(self, data):
        """
        Processes sensory data and updates blocks accordingly.

        Args:
            data (object): Sensory data to process.
        """
        # Implement data processing logic, iterating through blocks and calling their process_data methods

    def initialize(self, config_path):
        """
        Initializes the agent after configuration.

        Args:
            config_path (str): Path to the configuration directory.
        """
        if not self.configure(config_path):
            raise ValueError("Failed to load configuration")

        # Create scheduler after configuration
        self.scheduler = Scheduler(self.blocks)

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

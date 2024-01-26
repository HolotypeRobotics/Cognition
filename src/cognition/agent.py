import os
import yaml
from yamlinclude import YamlIncludeConstructor
from cognition.scheduler import Scheduler
from cognition.hierarchy import Hierarchy

class Agent:
    def __init__(self):
        self.initialized = False
        self.hierarchy = Hierarchy()  # Initialize hierarchy here
        self.scheduler = Scheduler()  # Initialize scheduler here
        
    def configure(self, config_path):
        print(f"Using configuration file {config_path}")
        try:
            # Load the configuration file
            print(f"Configuring Agent")
            YamlIncludeConstructor.add_to_loader_class(loader_class=yaml.FullLoader, base_dir=os.path.dirname(config_path))
            config_data = None
            with open(config_path, 'r') as f:
                config_data = yaml.load(f, yaml.FullLoader)
            if config_data is None:
                raise RuntimeError("Failed to load configuration file")
            
            # print(f"Config data: {config_data}")
            self.hierarchy.configure(config_data)
            print(f"Successfully configured agent")
            self.scheduler.set_hierarchy(self.hierarchy)

        except Exception as e:
            print(f"Failed to configure agent: {e}")
            return False
        
        self.scheduler = Scheduler(self.hierarchy)

        self.initialized = True
        
    def run(self):
        """
        Starts the agent's execution loop.
        """
        if not self.initialized:
            print("Please call agent.configure() before calling agent.run()")
            raise RuntimeError("Agent not initialized")

        self.scheduler.run()

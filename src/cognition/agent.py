from cognition.hierarchy import Hierarchy

"""
example config:
 - add_input:
    topic: deg_rotation
    data_type: float
    min: 0
    max: 360
    block: "SensoryInputBlock"

- add_output:
    action_topic

"""

class Agent:
    def __init__(self, hierarchy):
        self.hierarchy = hierarchy
        self.environment = None
        self.input_mapping = None
        self.output_mapping = None

    def set_environment(self, environment):
        self.environment = environment

    def configure(self, config):
        self.input_mapping = config['input_mapping']
        self.output_mapping = config['output_mapping']
    
    def get_inputs(self):
        inputs = {}
        for input in self.input_mapping:
            inputs[input] = self.environment.get_input(input)
            self.hierarchy.set_input(input, inputs[input])
        return inputs
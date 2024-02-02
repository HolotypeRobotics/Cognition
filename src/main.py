import numpy as np
from cognition.hierarchy import Hierarchy
import logging
import yaml
import os
from yamlinclude import YamlIncludeConstructor
from htm.bindings.sdr import SDR
#  Attempting to get a feel of what I need to do to set up the hierarchy to work with the robot, so that I know what to automate with the agent class
#  E.g. I need the agent to be able to calculate the size of the inputs and outputs, based on the type of data it is receiving from sensors
#  I need write this code for the node here, and then try to create functions to get rid of hard coded values.
#  The values that I cannot get rid of are the ones that will need to be placed in the agents config, and then loaded by the agent class.

logging.basicConfig(level=logging.INFO)


callbacks = None


# Initialize the hierarchy
hierarchy = Hierarchy()
interface_config_file = 'configs/interface_config.yml'
agent_config_file = 'configs/agent_config.yml'
# depends on the type of data the robot is receiving from the sensors
# SDR sensory_input = SDR(2048)
def get_input_sizes(sensors_to_blocks: dict):
    # sensors_to_blocks is a dictionary that maps the sensor data to the blocks in the hierarchy
    # I need to get the size of the input data for each block
    # returns a map of input sizes for each block
    input_sizes = {}
    for block, sensor in sensors_to_blocks.items():

def generate_callbacks(sensors_to_blocks: dict):
    # sensors_to_blocks is a dictionary that maps the sensor data to the blocks in the hierarchy
    # I need to generate a callback function for each sensor
    # returns a map of callback functions for each sensor
    # The callback function will be called when the sensor data is updated
    # and will update the input to the block
    # Specified in the interface config:
    # - The sensor data type
    # - The block name

def configure_interface(config):
    # convert the yaml file to a dictionary
    config_data = None
    with open(config, 'r') as f:
        config_data = yaml.load(f, yaml.FullLoader)
    get_input_sizes(config_data['sensors_to_blocks'])

def configure_agent(config: dict):
    get_input_sizes(config['sensors_to_blocks'])

def configure():
    # Load the config for the interface and the agent
    interface_config = None
    agent_config = None
    with open(interface_config_file, 'r') as f:
        interface_config = yaml.load(f, yaml.FullLoader)
    with open(agent_config_file, 'r') as f:
        agent_config = yaml.load(f, yaml.FullLoader)
    configure_interface(interface_config)
    configure_agent(agent_config)


def connect_sensor(topic, data_type, block_name: str):
    # Creates a callback, and subscribes to the sensor data
    # The callback will update the input to the block
    # The callback will be generated based on the data type and the block name
    pass

def connect_output(topic, data_type, block_name: str):
    # Publishes the output of the agent
    # The output is the concatenated matrix
    pass

def publish_concatenated_matrix(concatenated_matrix: np.ndarray):
    """
    Publish the concatenated matrix.
    """
    # Your code here to publish the concatenated matrix
    pass


def spin():
    """
    Main processing loop.
    """
    try:
        hierarchy.process_data()
        action_matrix = hierarchy.get_output(block_name='action_matrix')
        focus_matrix = hierarchy.get_output(block_name='focus_matrix')
        concatenated_matrix = np.concatenate((action_matrix, focus_matrix), axis=1)
        publish_concatenated_matrix(concatenated_matrix)
    except Exception as e:
        logging.error(f"Error in main loop: {e}")

if __name__ == "__main__":
    # Initialize the hierarchy
    config_path = 'configs/agent.yml'
    hierarchy = Hierarchy()
    YamlIncludeConstructor.add_to_loader_class(loader_class=yaml.FullLoader, base_dir=os.path.dirname(config_path))
    config_data = None
    with open(config_path, 'r') as f:
        config_data = yaml.load(f, yaml.FullLoader)
    hierarchy.configure(config_data)
    spin()

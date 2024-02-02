import numpy as np
from cognition.hierarchy import Hierarchy
import logging
import yaml
import os
from yamlinclude import YamlIncludeConstructor

logging.basicConfig(level=logging.INFO)

# Initialize the hierarchy
hierarchy = Hierarchy()

def publish_concatenated_matrix(concatenated_matrix: np.ndarray):
    """
    Publish the concatenated matrix.
    """
    # Your code here to publish the concatenated matrix
    pass

def gyro_callback(gyro_data: float):
    """
    Callback function for gyro data.
    """
    try:
        hierarchy.set_input(block_name='gyro', data=gyro_data)
    except Exception as e:
        logging.error(f"Error in gyro_callback: {e}")

def accelerometer_callback(accelerometer_data: float):
    """
    Callback function for accelerometer data.
    """
    try:
        hierarchy.set_input(block_name='accelerometer', data=accelerometer_data)
    except Exception as e:
        logging.error(f"Error in accelerometer_callback: {e}")

def magnetometer_callback(magnetometer_data: float):
    """
    Callback function for magnetometer data.
    """
    try:
        hierarchy.set_input(block_name='magnetometer', data=magnetometer_data)
    except Exception as e:
        logging.error(f"Error in magnetometer_callback: {e}")

def tof1_callback(tof1_data: float):
    """
    Callback function for tof1 data.
    """
    try:
        hierarchy.set_input(block_name='tof1', data=tof1_data)
    except Exception as e:
        logging.error(f"Error in tof1_callback: {e}")

def tof2_callback(tof2_data: float):
    """
    Callback function for tof2 data.
    """
    try:
        hierarchy.set_input(block_name='tof2', data=tof2_data)
    except Exception as e:
        logging.error(f"Error in tof2_callback: {e}")

def encoder1_callback(encoder1_data: float):
    """
    Callback function for encoder1 data.
    """
    try:
        hierarchy.set_input(block_name='encoder1', data=encoder1_data)
    except Exception as e:
        logging.error(f"Error in encoder1_callback: {e}")

def encoder2_callback(encoder2_data):
    """
    Callback function for encoder2 data.
    """
    try:
        hierarchy.set_input(block_name='encoder2', data=encoder2_data)
    except Exception as e:
        logging.error(f"Error in encoder2_callback: {e}")


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

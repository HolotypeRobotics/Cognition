import rclpy
from rclpy.node import Node
from std_msgs.msg import String  # Adjust this to the message type you're using
from cognition.hierarchy import Hierarchy
import random

class Agent(Node):
    def __init__(self):
        super().__init__('agent_node')
        self.configured = False
        self.hierarchy = Hierarchy()  # Initialize hierarchy here
        self.environment = None

        # Set up a subscription to receive sensor data
        self.subscription = self.create_subscription(
            String,  # Adjust this to the message type you're using
            'sensor_topic',  # Adjust this to the name of your sensor topic
            self.sensor_callback,
            10
        )

        # Set up a publisher to publish actions
        self.publisher = self.create_publisher(
            String,  # Adjust this to the message type you're using
            'action_topic',  # Adjust this to the name of your action topic
            10
        )

    def sensor_callback(self, msg):
        # This method is called whenever a message is received on the sensor topic
        # The received message is passed in as the `msg` parameter

        # Get the sensor data from the message
        sensor_data = msg.data  # Adjust this to match the structure of your messages

        # Set the input data for the agent
        self.hierarchy.set_input_data(sensor_data)

        # Process the data
        self.hierarchy.run()

        # Get the actions from the agent
        actions = self.hierarchy.get_output_data()

        # Publish the actions
        action_msg = String()  # Adjust this to the message type you're using
        action_msg.data = actions  # Adjust this to match the structure of your messages
        self.publisher.publish(action_msg)



def generate_random_data():
    # This function generates a list of 10 random floating-point numbers
    # between 0 and 1. Adjust this to generate the type of data you need.
    return [random.random() for _ in range(10)]

def main(args=None):
    rclpy.init(args=args)

    agent = Agent()

    # Generate some random sensor data
    sensor_data = generate_random_data()

    # Create a message with the sensor data
    sensor_msg = String()  # Adjust this to the message type you're using
    sensor_msg.data = sensor_data  # Adjust this to match the structure of your messages

    # Manually call the sensor_callback method with the sensor data
    agent.sensor_callback(sensor_msg)

    rclpy.spin(agent)

    agent.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
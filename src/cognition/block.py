from htm.bindings.engine_internal import Network,Region
from connection import Connection
import yaml

class Block(Network):
    def __init__(self, name, type, params):
        """
        Initializes a new instance of the Network class.

        Args:
            name: The name of the network.
            type: The type of the network.
            params: The parameters for the network.
        """
        self.name = name
        self.type = type
        self.params = params
        self.regions = {}
        self.links = {}

    def configure(self, params):
        block_params = params.get('block', None)
        if block_params is None:
            raise Exception("Block configuration missing")
        self.name = block_params.get('name', None)
        if self.name is None:
            raise Exception("Block name missing")
        network_params = params.get('network', None)
        if network_params is None:
            raise Exception("Network configuration missing")
        return super().configure(network_params)
    
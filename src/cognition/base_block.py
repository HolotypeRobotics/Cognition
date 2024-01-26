from cognition.block_impl_factory import BlockImplFactory
from htm.bindings.engine_internal import Network
import yaml
"""
Usage:
from base_block import BaseBlock

class Myblock(BaseBlock):
    def __init__(self, name: str, params: str):
        super().__init__('my_block', name, params)

...

/configs/agents/my_agent.yaml:

blocks:
    - name: my_block_1
        type: my_block
        params: ... # extra params for my_block
        block:
            name: my_block
        network: ... # params for blocks network

"""
     

class BaseBlock(metaclass=BlockImplFactory):

    def __init__(self, block_type: str = None, name: str = None, params: dict = None):
        if block_type is None:
            block_type  = self.__class__.__name__ #the name of the subclass
        else:
            self.block_type  = block_type
        print(f"BaseBlock.__init__({block_type})")

        self.name = name
        self.params = params
        self.network = Network()


    # def configure(self, name: str, params: dict, network: dict):
    #     print(f"BaseBlock.configure({name},{params})")
    #     block_params = params.get('block', None)
    #     if block_params is None:
    #         raise Exception("Block configuration missing")
    #     self.name = block_params.get('name', None)
    #     if self.name is None:
    #         raise Exception("Block name missing")
    #     network_params = block_params.get('network', None)
    #     if network_params is None:
    #         raise Exception("Network configuration missing")
    #     # Configure the block's network
    #     return super().configure(network_params)

    def configure(self, name: str, params: dict, network_config: dict):
        print(f"BaseBlock.configure({name},{params}, {network_config})")
        self.name = name
        self.params = params
        network_config_str = yaml.dump({"network":network_config})
        print(f"network_config_str: {network_config_str}")
        self.network.configure(network_config_str)
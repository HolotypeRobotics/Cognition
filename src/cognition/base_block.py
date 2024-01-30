from cognition.block_impl_factory import BlockImplFactory
from htm.bindings.engine_internal import Network
from htm.bindings.sdr import SDR
import enum
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
        self.network.initialize()
        self.input_region = None
        self.output_region = None
        self.encoding_type = None
        self.decoding_type = None
        self.links = []
        self.configured = False

    def add_output_link(self, next_block, src_region, src_output, dest_region, dest_input):
        # Add a link as a dictionary with all necessary information
        print(f"    {self.name}.add_output_link({next_block}, {src_region}, {src_output}, {dest_region}, {dest_input})")
        self.links.append({
            'block': next_block,
            'src_region': src_region,
            'src_output': src_output,
            'dest_region': dest_region,
            'dest_input': dest_input,
        })

    def run(self):
        print(f"calling {self.name}.run()")
        if self.configured is False:
            raise Exception(f"Block {self.name} not configured before calling run")

        self.network.run(1)

        for link in self.links:
            print(f"{self.name}.run() sending output from {link['src_region']} to {link['dest_region']}")
            output = self.network.getRegion(link['src_region']).getOutputData(link['src_output'])
            link['block'].network.getRegion(link['dest_region']).setInputData(link['dest_input'], output)

    def configure(self, name: str, params: dict, role, network_config: dict):
        print(f"{self.name}.configure({name},{params})")
        self.name = name
        self.params = params
        network_config_str = yaml.dump(network_config)  # Remove the {"network": network_config}
        self.network.configure(network_config_str)
        regions = self.network.getRegions()
        print(f"block {self.name} created network with {len(regions)} regions:")
        for name, region in regions:
            region_type = region.getType()
            print(f"    Region {name} is of type {region_type}")
        print()
        self.configured = True

    def set_encoding_type(self, encoding_type: str):
        self.encoding_type = encoding_type
        print(f"{self.name}.set_encoding_type({encoding_type})")

    def set_decoding_type(self, decoding_type: str):
        self.decoding_type = decoding_type
        print(f"{self.name}.set_decoding_type({decoding_type})")

    def set_input_region(self, region_name: str):
        if self.configured is False:
            raise Exception(f"Block {self.name} not configured before calling set_input_region")
        self.input_region = self.network.getRegion(region_name)
        if self.input_region is None:
            raise Exception(f"Region {region_name} does not exist")
        print(f"{self.name}.set_input_region({region_name})")

    def set_output_region(self, region_name: str):
        if self.configured is False:
            raise Exception(f"Block {self.name} not configured before calling set_output_region")
        self.output_region = self.network.getRegion(region_name)
        if self.output_region is None:
            raise Exception(f"Region {region_name} does not exist")
        print(f"{self.name}.set_output_region({region_name})")

def set_input_data(self, input_data):
    if self.configured is False:
        raise Exception(f"Block {self.name} not configured before calling set_input_data")
    assert self.input_region is not None, "Input region not set"
    print(f"{self.name}.set_input_data({input_data})")

    if self.input_region.getType() == 'ScalarEncoderRegion':
        self.input_region.setParameterReal64("sensedValue", input_data)
    else:
        # Convert the input data to an HTM.core SDR object
        input_data = SDR(input_data)

        # Set the input data for the specified region
        self.input_region.setInputData("bottomUpIn", input_data)


def get_output_data(self):
    if self.configured is False:
        raise Exception(f"Block {self.name} not configured before calling get_output_data")
    assert self.output_region is not None, "Output region not set"
    print(f"{self.name}.get_output_data()")

    # Get the output data from the output region
    output_data = self.output_region.getOutputData("bottomUpOut")
    return output_data

    
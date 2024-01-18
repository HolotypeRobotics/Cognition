import yaml
from block import Block
import threading

class Hierarchy():
    def __init__(self):
        self.initialized = False
        self.phase_info = {}
        self.max_enabled_phase = 0
        self.min_enabled_phase = float('inf')
        self.name   = ""
        self.config = None
        self.blocks = {} # dictionary of {block name : block object}
        self.links  = []

    def initialize(self):
        self.initialized = True
        
    def set_phases(self, block: str, phases: list):
        """
        Sets the phases for a block.

        Args:
            block: The name of the block.
            phases: The phases for the block.
        """
        if block not in self.blocks:
            raise Exception(f"Block {block} not found in hierarchy {self.name}")
        for phase in phases:
            self.phase_info[phase].append(block)
            self.max_enabled_phase = max(self.max_enabled_phase, phase)
            self.min_enabled_phase = min(self.min_enabled_phase, phase)


    def add_block(self, name: str, type: str, params: dict, phases: list):
        """
        Adds a network to the hierarchy.

        Args:
            name: The name of the network.
            type: The type of the network.
            params: The parameters for the network.
            phases: The phases for the network.
        """
        if name in self.blocks:
            raise Exception(f"Block {name} already exists in hierarchy {self.name}")

        block = Block(name, type, params, phases)
        self.blocks[name] = block

        phases = phases or [0]  # If no phases are specified, add the block to phase 0
        self.set_phases(block, phases)

        return block
            
    def link(self, src_block, dest_block, src_region, dest_region, src_output, dest_input):
            """
            Links the output of a region in one block to the input of a region in another block.

            Args:
                src_block: The block that contains the source region.
                dest_block: The block that contains the destination region.
                src_region: The name of the region in the source block.
                dest_region: The name of the region in the destination block.
                src_output: The name of the output in the source region.
                dest_input: The name of the input in the destination region.
            """
            # This is a simple example and assumes that the blocks have 'get_region' methods and the regions have 'get_output' and 'set_input' methods.
            # You may need to adjust this code to match the actual interface of your block and Region classes.
            src_region_obj = src_block.get_region(src_region)
            dest_region_obj = dest_block.get_region(dest_region)

            output_value = src_region_obj.get_output(src_output)
            dest_region_obj.set_input(dest_input, output_value)

    def link(self, src_block: Block, dest_block: Block, src_region_name: str, dest_region_name: str, src_output:str, dest_input:str):
        src_region = src_block.get_region(src_region_name)
        dest_region = dest_block.get_region(dest_region_name)
        src_region.link(src_output, dest_region, dest_input)
    


    def run(self, n: int, phases: [int] = None):

        if not self.initialized:
            self.initialize()

        if not self.phase_info:
            raise Exception("No phases defined in hierarchy")

        assert self.max_enabled_phase < len(self.phase_info), f"maxphase: {self.max_enabled_phase} size: {len(self.phase_info)}"

        for _ in range(n):
            threads = []
            if phases:
                for phase in phases:
                    assert phase < len(self.phase_info), f"Phase ID {phase} specified in run() is out of range."
                    for block in self.phase_info[phase]:
                        t = threading.Thread(target=block.run, args=(1,))
                        t.start()
                        threads.append(t)
            else:
                for current_phase in range(self.min_enabled_phase, self.max_enabled_phase + 1):
                    for block in self.phase_info[current_phase]:
                        t = threading.Thread(target=block.run, args=(1,))
                        t.start()
                        threads.append(t)

            # Wait for all threads to complete
            for t in threads:
                t.join()
    
    def configure(self, yaml_config: str):
        """
        Configures the hierarchy based on a YAML configuration string.

        Args:
            yaml_config: The YAML configuration string.
        """
        self.config = yaml.safe_load(yaml_config)
            
        if self.config is None:
            raise Exception("YAML configuration string is empty.")
        
        assert 'hierarchy' in self.config, "Expected yaml string to start with 'hierarchy:'."

        for command in self.config['hierarchy']:
            if 'add_block' in command:
                name = command['add_block']['name']
                type = command['add_block']['type']
                params = command['add_block'].get('params', {})
                phases = command['add_block'].get('phase', [])
                self.add_block(name, type, params, phases)

            elif 'add_link' in command:
                src = command['add_link']['src']
                dest = command['add_link']['dest']

                # Split the source and destination strings into block and region parts
                src_block, src_region, src_output = src.split('.')
                dest_block, dest_region, dest_input = dest.split('.')

                # Get the source and destination networks
                src_net = self.networks[src_block]
                dest_net = self.networks[dest_block]

                self.link(src_net, dest_net, src_region, dest_region, src_output, dest_input)

        # ------------------------------------------------------------
                
        self.name = self.config['name']
        substituted_regions = []
        number_of_blocks = 0
        for block_config in self.config['blocks']:
            block = Block()
            block_phase = block_config.get('phase', number_of_blocks)
            number_of_blocks += 1

            # Get substitutions for this block, if any
            # Replace the region name with the block_config['name']/region name
            # to avoid naming conflicts, then add the substitution to the list
            substitutions = block_config.get('substitutions', [])
            for sub in substitutions:
                sub['region'] = f"{block_config['name']}/{sub['region']}"
                substituted_regions.append(sub['region'])

            number_of_regions = 0
            # Add the block's regions
            for item in block_config["block"]:

                if "Region" in item:
                    region_info = item["Region"]
                    # Only add the region if it's not being substituted
                    if region_info["name"] not in substituted_regions:
                        # Change the region name to be the block name / region name, 
                        # so that we can have many regions with the same name from different blocks
                        # e.g. when we have duplicate blocks in the hierarchy
                        region_name = f"{block_config['name']}/{region_info['name']}"
                        # Change the region phase to be the block phase * region phase
                        # This allows us to specify a phase for the block, and then a phase for each region in the block
                        region_info["phase"] = block_phase * region_info.get("phase", number_of_regions)
                        number_of_regions += 1
                        # Add the region to the block
                        block.addRegion(region_name, region_info["type"], yaml.dump(region_info["params"]))

                # Add the block to the hierarchy        
                self.blocks.append(block)


            # Link all the regions together
            for item in block_config["network"]:
                if "Link" in item:
                    link_info = item["Link"]
                    # Change the region names to be the block name / region name,
                    link_info["source"] = f"{block_config['name']}/{link_info['source']}"
                    link_info["destination"] = f"{block_config['name']}/{link_info['destination']}"

                    # If the region is being substituted, replace it with the substitution
                    link_info["source"] =  substituted_regions.get(link_info["source"], link_info["source"])
                    link_info["destination"] =  substituted_regions.get(link_info["destination"], link_info["destination"])

                    # Add the link
                    block.link(link_info["source"], link_info["destination"], link_info["type"], yaml.dump(link_info["params"]))

        return True



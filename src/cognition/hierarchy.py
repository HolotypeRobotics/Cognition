import os
from cognition.block_impl_factory import BlockImplFactory
import pkgutil
import cognition.blocks
import threading

# Import all modules in the cognition.blocks package
for loader, module_name, is_pkg in pkgutil.walk_packages(cognition.blocks.__path__):
    module = loader.find_module(module_name).load_module(module_name)


class Hierarchy():
    def __init__(self):
        self.phase_info = {}
        self.max_enabled_phase = 0
        self.min_enabled_phase = float('inf')
        self.name   = ""
        self.config = None
        self.blocks = {} # dictionary of {block name : block object}
        self.links  = []

    def set_phases(self, block_name: str, phases: [int]):
        block = self.blocks.get(block_name)
        if not block:
            raise Exception(f"Block {block_name} not found")

        for phase in phases:
            if phase not in self.phase_info:
                self.phase_info[phase] = []

            if block_name not in self.phase_info[phase]:
                self.phase_info[phase].append(block_name)
                self.max_enabled_phase = max(self.max_enabled_phase, phase)
                self.min_enabled_phase = min(self.min_enabled_phase, phase)

    def add_block(self, name: str, block_type: str, params: dict, network: dict, phases: list):

        if name in self.blocks:
            raise Exception(f"Block {name} already exists in hierarchy {self.name}")

        print(f"Adding block {name} of type {block_type} to hierarchy {self.name}")
        block = BlockImplFactory.createBlockImpl(block_type)
        if block is None:
            raise Exception(f"Unable to create block of type {block_type}")
        block.configure(name=name, params=params, network_config=network)
        print(f"    Block {name} configured")
        print(f"adding block {name} to hierarchy {self.name}")
        self.blocks[name] = block
        print(f"setting phases {phases} to block {block}, with name {name}")
        phases = phases or [0]  # If no phases are specified, add the block to phase 0
        self.set_phases(name, phases)
        print(f"succesfully set phases {phases} for block {name}")

        return block
            
    # def add_link(self, src_block, dest_block, src_region, dest_region, src_output, dest_input):
    #         # This is a simple example and assumes that the blocks have 'get_region' methods and the regions have 'get_output' and 'set_input' methods.
    #         # You may need to adjust this code to match the actual interface of your block and Region classes.
    #         src_region_obj = src_block.network.get_region(src_region)
    #         dest_region_obj = dest_block.network.get_region(dest_region)

    #         output_value = src_region_obj.get_output(src_output)
    #         dest_region_obj.set_input(dest_input, output_value)

    def add_link(self, src_block, dest_block, src_region_name: str, dest_region_name: str, src_output:str, dest_input:str):
        try:
            src_region = src_block.network.getRegion(src_region_name)
        except Exception as e:
            src_block.network.addRegion("region1", "SPRegion", "{columnCount: 1024}")
            regions = src_block.network.getRegions()
            print(f"Regions:{regions}")
            print(f"{len(regions)} regions found in block {src_block.name}")

            raise Exception(f"Failed to get links source region {src_region_name} from block {src_block.name}") from e
        src_region = src_block.network.getRegion(src_region_name)
        try:
            dest_region = dest_block.network.getRegion(dest_region_name)
        except Exception as e:
            regions = dest_block.network.getRegions()
            for region in regions:
                print(regions)
            raise Exception(f"Failed to get links destination region {dest_region_name} from block {dest_block.name}") from e
        
        src_region.link(src_output, dest_region, dest_input)
    

    def run(self, n: int, phases: [int] = None):

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
    
    def configure(self, yaml_config):
        print(f"    Configuring hierarchy")    
        if yaml_config is None:
            raise Exception("YAML configuration string is empty.")
        
        if not isinstance(yaml_config, dict):
            raise ValueError("config_data must be a dictionary")
        
        self.config = yaml_config.get('hierarchy', None)

        if self.config is None:
            raise Exception("Hierarchy configuration missing")
        
        for command in self.config:
            if 'add_block' in command:
                for block in command['add_block']:
                    name = block.get('name', None)
                    block_type = block.get('block_type', 'Block')
                    params = block.get('params', {})
                    phases = block.get('phase', [])
                    network = block.get('network', {})
                    print(f"    Block params: {params}")
                    self.add_block(name=name, block_type=block_type, params=params, network=network, phases=phases)
                    print(f"    Added block {name}")

        for command in self.config:
            if 'add_link' in command:
                add_link = command.get('add_link', None)
                if add_link is None:
                    raise Exception("Link configuration missing")
                src = command['add_link'].get('src', None)
                dest = command['add_link'].get('dest', None)
                print(f"Adding link {src} -> {dest}")

                # Split the source and destination strings into block and region parts
                src = src.split('.')
                dest = dest.split('.')
                if len(src) != 3:
                    raise Exception(f"Invalid source: {src}, must be in the form block.region.output")
                if len(dest) != 3:
                    raise Exception(f"Invalid destination: {dest}, must be in the form block.region.input")
                
                src_block, src_region, src_output = src
                dest_block, dest_region, dest_input = dest

                # Get the source and destination networks
                src_net = self.blocks[src_block]
                dest_net = self.blocks[dest_block]
                self.add_link(src_net, dest_net, src_region, dest_region, src_output, dest_input)

        # # ------------------------------------------------------------
                
        # self.name = self.config['name']
        # substituted_regions = []
        # number_of_blocks = 0
        # for block_config in self.config['blocks']:
        #     block = Block()
        #     block_phase = block_config.get('phase', number_of_blocks)
        #     number_of_blocks += 1

        #     # Get substitutions for this block, if any
        #     # Replace the region name with the block_config['name']/region name
        #     # to avoid naming conflicts, then add the substitution to the list
        #     substitutions = block_config.get('substitutions', [])
        #     for sub in substitutions:
        #         sub['region'] = f"{block_config['name']}/{sub['region']}"
        #         substituted_regions.append(sub['region'])

        #     number_of_regions = 0
        #     # Add the block's regions
        #     for item in block_config["block"]:

        #         if "Region" in item:
        #             region_info = item["Region"]
        #             # Only add the region if it's not being substituted
        #             if region_info["name"] not in substituted_regions:
        #                 # Change the region name to be the block name / region name, 
        #                 # so that we can have many regions with the same name from different blocks
        #                 # e.g. when we have duplicate blocks in the hierarchy
        #                 region_name = f"{block_config['name']}/{region_info['name']}"
        #                 # Change the region phase to be the block phase * region phase
        #                 # This allows us to specify a phase for the block, and then a phase for each region in the block
        #                 region_info["phase"] = block_phase * region_info.get("phase", number_of_regions)
        #                 number_of_regions += 1
        #                 # Add the region to the block
        #                 block.addRegion(region_name, region_info["type"], yaml.dump(region_info["params"]))

        #         # Add the block to the hierarchy        
        #         self.blocks.append(block)


        #     # Link all the regions together
        #     for item in block_config["network"]:
        #         if "Link" in item:
        #             link_info = item["Link"]
        #             # Change the region names to be the block name / region name,
        #             link_info["source"] = f"{block_config['name']}/{link_info['source']}"
        #             link_info["destination"] = f"{block_config['name']}/{link_info['destination']}"

        #             # If the region is being substituted, replace it with the substitution
        #             link_info["source"] =  substituted_regions.get(link_info["source"], link_info["source"])
        #             link_info["destination"] =  substituted_regions.get(link_info["destination"], link_info["destination"])

        #             # Add the link
        #             block.link(link_info["source"], link_info["destination"], link_info["type"], yaml.dump(link_info["params"]))

        return True



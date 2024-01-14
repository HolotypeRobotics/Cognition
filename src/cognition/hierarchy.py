import yaml
from block import Block
from htm.bindings.engine_internal import Network

class Hierarchy():
    def __init__(self):
        self.name   = ""
        self.config = None
        self.network = Network()
        self.blocks = []

    def configure(self, config):
        # Load the hierarchy's configuration from its YAML file
        with open(config, 'r') as file:
            self.config = yaml.safe_load(file)
            
        if self.config is None:
            return False
        
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
            for item in block_config["network"]:

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
                        # Add the region to the network
                        region = self.network.addRegion(region_name, region_info["type"], yaml.dump(region_info["params"]))
                        # Add the region object, and info to the block 
                        block.addRegion(region, region_info)

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
                    self.network.link(link_info["source"], link_info["destination"], link_info["type"], yaml.dump(link_info["params"]))

        return True
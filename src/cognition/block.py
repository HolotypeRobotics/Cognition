from htm.bindings.engine_internal import Region
from connection import Connection
import yaml

class Block():
    def __init__(self):
        super().__init__()
        self.output_data = None
        self.input_data = None
        self.regions = []
        self.connections = []

    def add_region(self, region: Region, region_info: dict):
        self.regions.append(region)
        # Sortregions in order to call each regions compute function in order of the regions phase
        self.regions.sort(key=lambda region: region_info["phase"])
        

    def compute(self):
        for r in self.regions:
            r.compute()
            r.pushOutputsOverLinks() #TODO: may need to call network.run(1) instead


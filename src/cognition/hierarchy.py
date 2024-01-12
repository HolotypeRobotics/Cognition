from block import Block
from module import Module
# from utils.configurator import Configurator

class Hierarchy():
    def __init__(self, config):
        self.config = config
        self.blocks = []

    def configure(self):

        for block_config in self.config:
            # go to path in block_config
            # get config file
            # create block
            # configure block
            path = block_config['path']
            block = Block()
            block.configure(path)
            if block is None:
                raise Exception(f'Unable to configure block [{path}] in hierarchy')
            self.blocks.append(block)
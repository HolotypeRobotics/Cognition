import numpy as np

class Connection:
    def __init__(self, source_block, destination_block):
        self.source_block = source_block
        self.destination_block = destination_block
        self.data = None

    def transfer_data(self, data):
        self.data = self.modulate(data)
        self.destination_block.input_data = self.data

    def modulate(self, data):
        raise NotImplementedError("The 'modulate' method must be implemented in the child class")

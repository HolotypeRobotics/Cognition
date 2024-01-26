from src.cognition.block import Block

class CustomBlock(Block):
    def __init__(self, name, params):
        super().__init__(name, params)

    def run(self):
        # Your custom logic goes here
        pass
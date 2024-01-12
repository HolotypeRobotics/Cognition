from htm.bindings.engine_internal import Network

class Block(Network):
    def __init__(self):
        super().__init__()

    def process_data(self, data):
        encoded_data = self.encoder.encode(data)
        self.sp.compute(encoded_data)
        self.tm.compute()

    def configure(self, path):
        with open(path, 'r') as file:
            content = file.read()
            config = content.replace('\n', '')
            # check if config is valid
            if config is None:
                raise Exception('Invalid config file for Block')
            super().configure(config['network'])
            return True

    

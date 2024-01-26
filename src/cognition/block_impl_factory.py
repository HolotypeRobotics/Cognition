class BlockImplFactory(type):
    registry = {}

    def __init__(cls, name, bases, attrs):
        if name != 'BaseBlock':
            BlockImplFactory.registry[name] = cls
            print(f"Registered block type {name}")
        else:
            print(f"Skipped registration of {name}")
        super().__init__(name, bases, attrs)

    @classmethod
    def createBlockImpl(cls, block_type: str):
        print(f"Current registry: {BlockImplFactory.registry}")
        if block_type not in cls.registry:
            raise Exception(f"Block type {block_type} not found in Block Registry: {BlockImplFactory.registry}")
        return cls.registry[block_type]()
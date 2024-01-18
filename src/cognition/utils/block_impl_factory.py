class BlockImplFactory:
    """
    A factory class for creating instances of BlockImpl and their specifications.
    """

    _instance = None

    @staticmethod
    def getInstance():
        """
        Returns the singleton instance of the BlockImplFactory class.
        """
        if BlockImplFactory._instance is None:
            BlockImplFactory._instance = BlockImplFactory()
        return BlockImplFactory._instance

    def __init__(self, params):
        """
        Initializes a new instance of the MyNetworkImpl class.

        Args:
            params: The parameters for the network.
        """
        self.params = params
        self.Block_types = {}

    def registerBlockType(self, type, Block_class, spec):
        """
        Registers a Block type with the factory.

        Args:
            type: The type of the Block.
            Block_class: The class that implements the Block.
            spec: The specification for the Block.
        """
        self.Block_types[type] = (Block_class, spec)

    def getSpec(self, type):
        """
        Returns the specification for a Block type.

        Args:
            type: The type of the Block.

        Returns:
            The specification for the Block type.
        """
        assert type in self.Block_types, f"Block type {type} is not registered."
        return self.Block_types[type][1]

    def createBlockImpl(self, type, params):
        """
        Creates a new instance of a Block implementation.

        Args:
            type: The type of the Block.
            params: The parameters for the Block.

        Returns:
            A new instance of the Block implementation.
        """
        assert type in self.Block_types, f"Block type {type} is not registered."
        Block_class = self.Block_types[type][0]
        return Block_class(params)
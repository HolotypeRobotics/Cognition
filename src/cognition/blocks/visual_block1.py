from cognition.base_block import BaseBlock

class VisualBlock1(BaseBlock):
    def __init__(self, name: str, params: str):
        super().__init__('visual_block2',name, params)

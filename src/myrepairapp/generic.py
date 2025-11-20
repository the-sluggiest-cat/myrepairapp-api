class GenericItem:
    ITEM_TYPE = None

    def __init__(self, item_type: str):
        super().__init__()
        self.ITEM_TYPE = item_type
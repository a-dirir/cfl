
class Resource:
    def __init__(self, value: str, holders: list):
        self.idn = value
        self.value = value
        self.holders = holders
        self.type = "resource"
        self.children = []

    def get_holders(self):
        return self.holders


    def __repr__(self):
        return f"Resource(idn={self.idn}, value={self.value}, holders={self.holders})"

class SettlementStorage:

    def __init__(self):
        self._items = []

    def add(self, settlement):
        if self.find_by_name(settlement.get_name()) is not None:
            raise ValueError("Город с таким именем уже есть")
        self._items.append(settlement)

    def get_all(self):
        return self._items

    def find_by_name(self, name):
        for settlement in self._items:
            if settlement.get_name() == name:
                return settlement
        return None

    def remove_by_name(self, name):
        settlement = self.find_by_name(name)
        if settlement is None:
            return None
        self._items.remove(settlement)
        return settlement

    def clear(self):
        self._items = []

    def count(self):
        return len(self._items)

    def is_empty(self):
        return len(self._items) == 0
class ProvinceStorage:

    def __init__(self, max_provinces):
        self._items = []
        self._max = max_provinces

    def add(self, province):
        if self.find_by_name(province.get_name()) is not None:
            raise ValueError("Провинция с таким именем уже существует")
        if len(self._items) >= self._max:
            raise ValueError("Достигнут лимит провинций: " + str(self._max))
        self._items.append(province)

    def get_all(self):
        return self._items

    def find_by_name(self, name):
        for province in self._items:
            if province.get_name() == name:
                return province
        return None

    def remove_by_name(self, name):
        province = self.find_by_name(name)
        if province is None:
            return None
        self._items.remove(province)
        return province

    def clear(self):
        self._items = []

    def count(self):
        return len(self._items)

    def is_empty(self):
        return len(self._items) == 0

    def get_max(self):
        return self._max

    def is_full(self):
        return len(self._items) >= self._max
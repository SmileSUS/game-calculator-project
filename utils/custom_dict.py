class CustomDict:

    def __init__(self):
        self._keys = []
        self._values = []

    def set(self, key, value):
        index = self._find_index(key)
        if index == -1:
            self._keys.append(key)
            self._values.append(value)
        else:
            self._values[index] = value

    def get(self, key, default=None):
        index = self._find_index(key)
        if index == -1:
            return default
        return self._values[index]

    def has(self, key):
        return self._find_index(key) != -1

    def remove(self, key):
        index = self._find_index(key)
        if index == -1:
            return None
        value = self._values[index]
        self._keys.pop(index)
        self._values.pop(index)
        return value

    def keys(self):
        return list(self._keys)

    def values(self):
        return list(self._values)

    def items(self):
        result = []
        for index in range(len(self._keys)):
            result.append((self._keys[index], self._values[index]))
        return result

    def count(self):
        return len(self._keys)

    def clear(self):
        self._keys = []
        self._values = []

    def _find_index(self, key):
        for index in range(len(self._keys)):
            if self._keys[index] == key:
                return index
        return -1

    def __len__(self):
        return len(self._keys)

    def __contains__(self, key):
        return self.has(key)

    def __str__(self):
        parts = []
        for index in range(len(self._keys)):
            parts.append(str(self._keys[index]) + "=" + str(self._values[index]))
        return "{" + ", ".join(parts) + "}"

    def __repr__(self):
        return "CustomDict(" + self.__str__() + ")"

    def __eq__(self, other):
        if not isinstance(other, CustomDict):
            return NotImplemented
        if self.count() != other.count():
            return False
        for key in self._keys:
            if self.get(key) != other.get(key):
                return False
        return True
from models.action import Action


class ActionStorage:

    def __init__(self):
        self._items = []

    def add(self, action):
        if not isinstance(action, Action):
            raise ValueError("Можно добавить только объект Action")
        self._items.append(action)

    def create(self, description, time_in):
        action = Action(description, time_in)
        self._items.append(action)
        return action

    def get_all(self):
        return self._items

    def clear(self):
        self._items = []

    def count(self):
        return len(self._items)

    def close_last_by_prefix(self, prefix, time_out):
        for index in range(len(self._items) - 1, -1, -1):
            action = self._items[index]
            if action.get_description().startswith(prefix) and action.get_time_out() == "":
                action.close(time_out)
                return action
        return None

    def close_all_open(self, time_out):
        for action in self._items:
            if action.get_time_out() == "":
                action.close(time_out)

    def to_file_lines(self):
        lines = []
        for action in self._items:
            lines.append(action.to_file_string())
        return lines
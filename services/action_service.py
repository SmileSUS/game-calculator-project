from datetime import datetime

from storage.action_storage import ActionStorage


class ActionService:

    def __init__(self, report_writer):
        self._storage = ActionStorage()
        self._report_writer = report_writer

    def now_string(self):
        return datetime.now().strftime("%d.%m.%y %H:%M:%S")

    def get_all(self):
        return self._storage.get_all()

    def count(self):
        return self._storage.count()

    def clear(self):
        self._storage.clear()

    def log(self, description):
        time_in = self.now_string()
        action = self._storage.create(description, time_in)
        return action

    def close_by_prefix(self, prefix):
        time_out = self.now_string()
        return self._storage.close_last_by_prefix(prefix, time_out)

    def close_all_open(self):
        time_out = self.now_string()
        self._storage.close_all_open(time_out)

    def write_report(self):
        time_out = self.now_string()
        self._storage.close_all_open(time_out)
        self._report_writer.write(self._storage)

    def to_file_lines(self):
        return self._storage.to_file_lines()

    def dump(self):
        lines = []
        for action in self._storage.get_all():
            lines.append({
                "description": action.get_description(),
                "time_in": action.get_time_in(),
                "time_out": action.get_time_out()
            })
        return lines

    def restore(self, data):
        self._storage.clear()
        for item in data:
            action = self._storage.create(item["description"], item["time_in"])
            action.set_time_out(item["time_out"])
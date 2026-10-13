from models.base import BaseEntity


class Action(BaseEntity):

    def __init__(self, description, time_in):
        self._description = None
        self._time_in = None
        self._time_out = ""
        self.set_description(description)
        self.set_time_in(time_in)

    def get_description(self):
        return self._description

    def set_description(self, value):
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("Описание действия не может быть пустым")
        self._description = value.strip()

    def get_time_in(self):
        return self._time_in

    def set_time_in(self, value):
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("Время начала должно быть непустой строкой")
        self._time_in = value.strip()

    def get_time_out(self):
        return self._time_out

    def set_time_out(self, value):
        if not isinstance(value, str):
            raise ValueError("Время окончания должно быть строкой")
        self._time_out = value

    def close(self, time_out):
        self._time_out = time_out

    def __str__(self):
        return self._description + " (" + self._time_in + " - " + (self._time_out if self._time_out else "...") + ")"

    def __repr__(self):
        return "Action('" + self._description + "', '" + self._time_in + "', '" + self._time_out + "')"

    def __eq__(self, other):
        if not isinstance(other, Action):
            return NotImplemented
        return self._description == other._description and self._time_in == other._time_in

    def get_info(self):
        return self.__str__()

    def to_file_string(self):
        desc = self._description.ljust(28)
        t_in = self._time_in.ljust(19)
        t_out = (self._time_out if self._time_out else "").ljust(20)
        return "| " + desc + " | " + t_in + " | " + t_out + " |"
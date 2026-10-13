from models.base import BaseEntity
from models.settlement import Settlement
from storage.settlement_storage import SettlementStorage


class Province(BaseEntity):

    def __init__(self, name):
        self._name = None
        self._settlements = SettlementStorage()
        self.set_name(name)

    def get_name(self):
        return self._name

    def set_name(self, value):
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("Имя провинции не может быть пустым")
        self._name = value.strip()

    def get_settlements(self):
        return self._settlements

    def add_settlement(self, settlement):
        if not isinstance(settlement, Settlement):
            raise ValueError("Можно добавить только объект Settlement")
        self._settlements.add(settlement)

    def find_settlement(self, name):
        return self._settlements.find_by_name(name)

    def remove_settlement(self, name):
        return self._settlements.remove_by_name(name)

    def get_total_population(self):
        total = 0
        for settlement in self._settlements.get_all():
            total = total + settlement.get_total_population()
        return total

    def get_total_employed(self):
        total = 0
        for settlement in self._settlements.get_all():
            total = total + settlement.get_employed()
        return total

    def __str__(self):
        return ("Провинция " + self._name + ": " +
                str(self._settlements.count()) + " городов, " +
                str(self.get_total_population()) + " жителей")

    def __repr__(self):
        return "Province('" + self._name + "')"

    def __eq__(self, other):
        if not isinstance(other, Province):
            return NotImplemented
        return self._name == other._name

    def get_info(self):
        return self.__str__()

    def to_file_string(self):
        return ("Провинция: " + self._name + "\n" +
                "Городов: " + str(self._settlements.count()) + "\n" +
                "Жителей: " + str(self.get_total_population()) + "\n" +
                "Занято: " + str(self.get_total_employed()) + "\n")
from models.settlement import Settlement


class SettlementService:

    def __init__(self, action_service):
        self._action_service = action_service

    def create(self, province, name, total_population):
        name = name.strip()
        if name == "":
            raise ValueError("Имя города не может быть пустым")

        if total_population <= 0:
            raise ValueError("Число жителей должно быть больше нуля")

        if province.find_settlement(name) is not None:
            raise ValueError("Город с таким именем уже есть в провинции " + province.get_name())

        settlement = Settlement(name, total_population)
        province.add_settlement(settlement)

        description = ("Создан город " + name + " (" + str(total_population) + " жителей) в " +
                       province.get_name())
        self._action_service.log(description)

        return settlement

    def remove(self, province, name):
        settlement = province.find_settlement(name)
        if settlement is None:
            return None

        province.remove_settlement(name)

        description = ("Создан город " + name + " (" + str(settlement.get_total_population()) +
                       " жителей) в " + province.get_name())
        self._action_service.close_by_prefix(description)

        self._action_service.log("Удалён город " + name + " из " + province.get_name())

        return settlement

    def get_all(self, province):
        return province.get_settlements().get_all()

    def find(self, province, name):
        return province.find_settlement(name)
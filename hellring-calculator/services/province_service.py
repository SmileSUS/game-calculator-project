from models.province import Province


class ProvinceService:

    def __init__(self, action_service, province_storage):
        self._action_service = action_service
        self._storage = province_storage

    def create(self, name):
        name = name.strip()
        if name == "":
            raise ValueError("Имя провинции не может быть пустым")

        if self._storage.is_full():
            raise ValueError("Достигнут лимит провинций: " + str(self._storage.get_max()))

        if self._storage.find_by_name(name) is not None:
            raise ValueError("Провинция с таким именем уже существует")

        province = Province(name)
        self._storage.add(province)

        self._action_service.log("Создана провинция " + name)

        return province

    def remove(self, name):
        province = self._storage.find_by_name(name)
        if province is None:
            return None

        self._storage.remove_by_name(name)

        self._action_service.close_by_prefix("Создана провинция " + name)
        self._action_service.log("Удалена провинция " + name)

        return province

    def get_all(self):
        return self._storage.get_all()

    def find(self, name):
        return self._storage.find_by_name(name)

    def count(self):
        return self._storage.count()

    def max_count(self):
        return self._storage.get_max()
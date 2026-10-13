from models.province import Province
from storage.province_storage import ProvinceStorage
from storage.save_manager import SaveManager
from storage.report_writer import ReportWriter

from services.action_service import ActionService
from services.job_service import JobService
from services.settlement_service import SettlementService
from services.province_service import ProvinceService

from utils import CustomDict


class AppService:

    def __init__(self):
        self._report_writer = ReportWriter("report.txt")
        self._save_manager = SaveManager("save.txt")

        self._action_service = ActionService(self._report_writer)

        self._province_storage = ProvinceStorage(100)
        self._province_service = ProvinceService(self._action_service, self._province_storage)

        self._job_service = JobService(self._action_service)
        self._settlement_service = SettlementService(self._action_service)

    # ---------- Провинции ----------

    def create_province(self, name):
        return self._province_service.create(name)

    def remove_province(self, name):
        return self._province_service.remove(name)

    def get_provinces(self):
        return self._province_service.get_all()

    def find_province(self, name):
        return self._province_service.find(name)

    def count_provinces(self):
        return self._province_service.count()

    def max_provinces(self):
        return self._province_service.max_count()

    # ---------- Города ----------

    def create_settlement(self, province_name, settlement_name, total_population):
        province = self._province_service.find(province_name)
        if province is None:
            raise ValueError("Провинция не найдена: " + province_name)
        return self._settlement_service.create(province, settlement_name, total_population)

    def remove_settlement(self, province_name, settlement_name):
        province = self._province_service.find(province_name)
        if province is None:
            raise ValueError("Провинция не найдена: " + province_name)
        return self._settlement_service.remove(province, settlement_name)

    def get_settlements(self, province_name):
        province = self._province_service.find(province_name)
        if province is None:
            return []
        return self._settlement_service.get_all(province)

    def find_settlement(self, province_name, settlement_name):
        province = self._province_service.find(province_name)
        if province is None:
            return None
        return self._settlement_service.find(province, settlement_name)

    # ---------- Работы ----------

    def assign_job(self, province_name, settlement_name, job_type, workers):
        settlement = self.find_settlement(province_name, settlement_name)
        if settlement is None:
            raise ValueError("Город не найден: " + settlement_name)
        return self._job_service.assign(settlement, job_type, workers)

    def remove_job(self, province_name, settlement_name, job_type):
        settlement = self.find_settlement(province_name, settlement_name)
        if settlement is None:
            raise ValueError("Город не найден: " + settlement_name)
        return self._job_service.remove(settlement, job_type)

    def get_jobs(self, province_name, settlement_name):
        settlement = self.find_settlement(province_name, settlement_name)
        if settlement is None:
            return []
        return self._job_service.get_all(settlement)

    # ---------- Сводка провинции ----------

    def get_province_summary(self, province_name):
        province = self._province_service.find(province_name)
        if province is None:
            return None

        summary = CustomDict()
        summary.set("name", province.get_name())
        summary.set("settlements", province.get_settlements().count())
        summary.set("population", province.get_total_population())
        summary.set("employed", province.get_total_employed())
        return summary

    # ---------- Журнал ----------

    def get_actions(self):
        return self._action_service.get_all()

    def count_actions(self):
        return self._action_service.count()

    # ---------- Сохранение / Загрузка / Новая игра ----------

    def save_game(self):
        provinces = self._province_storage.get_all()
        actions = self._action_service.get_all()
        self._save_manager.save(provinces, actions)

    def load_game(self):
        state = self._save_manager.load()
        if state is None:
            return False

        try:
            self._restore_provinces(state.get("provinces", []))
            self._action_service.restore(state.get("actions", []))
            return True
        except (KeyError, ValueError, TypeError):
            self.new_game()
            return False

    def new_game(self):
        self._save_manager.delete()
        self._province_storage.clear()
        self._action_service.clear()

    def write_report(self):
        self._action_service.write_report()

    # ---------- Внутреннее: восстановление ----------

    def _restore_provinces(self, data):
        from models.settlement import Settlement
        from models.job import Job

        self._province_storage.clear()

        for province_data in data:
            province = Province(province_data.get("name"))

            settlements = province_data.get("settlements", [])
            if settlements is None:
                settlements = []

            for settlement_data in settlements:
                settlement = Settlement(
                    settlement_data.get("name"),
                    settlement_data.get("population")
                )

                jobs = settlement_data.get("jobs", [])
                if jobs is None:
                    jobs = []

                for job_data in jobs:
                    job = Job(
                        job_data.get("job_type"),
                        job_data.get("workers"),
                        job_data.get("time_in")
                    )
                    settlement.get_jobs().add(job)

                province.add_settlement(settlement)

            self._province_storage.add(province)
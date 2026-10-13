from models.base import BaseEntity
from models.job import Job
from storage.job_storage import JobStorage


class Settlement(BaseEntity):

    def __init__(self, name, total_population):
        self._name = None
        self._total_population = None
        self._jobs = JobStorage()
        self.set_name(name)
        self.set_total_population(total_population)

    def get_name(self):
        return self._name

    def set_name(self, value):
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("Имя города не может быть пустым")
        self._name = value.strip()

    def get_total_population(self):
        return self._total_population

    def set_total_population(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Число жителей должно быть положительным целым числом")
        self._total_population = value

    def get_jobs(self):
        return self._jobs

    def get_employed(self):
        return self._jobs.total_workers()

    def get_free(self):
        return self._total_population - self.get_employed()

    def assign_job(self, job_type, workers, time_in):
        job_type = job_type.strip()
        if job_type == "":
            raise ValueError("Укажите тип работы")

        if workers <= 0:
            raise ValueError("Количество должно быть больше нуля")

        if workers > self.get_free():
            raise ValueError("Недостаточно свободных жителей. Свободно: " + str(self.get_free()))

        existing = self._jobs.find_by_type(job_type)
        if existing is not None:
            existing.set_workers(existing.get_workers() + workers)
            return existing

        new_job = Job(job_type, workers, time_in)
        self._jobs.add(new_job)
        return new_job

    def remove_job(self, job_type):
        job = self._jobs.find_by_type(job_type)
        if job is None:
            return None
        self._jobs.remove_by_type(job_type)
        return job

    def __str__(self):
        return ("Город " + self._name + ": " +
                str(self._total_population) + " жителей, занято " +
                str(self.get_employed()))

    def __repr__(self):
        return "Settlement('" + self._name + "', " + str(self._total_population) + ")"

    def __eq__(self, other):
        if not isinstance(other, Settlement):
            return NotImplemented
        return self._name == other._name

    def get_info(self):
        return self.__str__()

    def to_file_string(self):
        return ("Город: " + self._name + "\n" +
                "Всего жителей: " + str(self._total_population) + "\n" +
                "Занято: " + str(self.get_employed()) + "\n" +
                "Свободно: " + str(self.get_free()) + "\n")
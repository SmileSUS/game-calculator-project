from models.base import BaseEntity


class Job(BaseEntity):

    def __init__(self, job_type, workers, time_in):
        self._job_type = None
        self._workers = None
        self._time_in = None
        self.set_job_type(job_type)
        self.set_workers(workers)
        self.set_time_in(time_in)

    def get_job_type(self):
        return self._job_type

    def set_job_type(self, value):
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("Тип работы должен быть непустой строкой")
        self._job_type = value.strip()

    def get_workers(self):
        return self._workers

    def set_workers(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Количество работников должно быть целым неотрицательным числом")
        self._workers = value

    def get_time_in(self):
        return self._time_in

    def set_time_in(self, value):
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("Время назначения должно быть непустой строкой")
        self._time_in = value.strip()

    def __str__(self):
        return self._job_type + ": " + str(self._workers) + " чел."

    def __repr__(self):
        return "Job('" + self._job_type + "', " + str(self._workers) + ")"

    def __eq__(self, other):
        if not isinstance(other, Job):
            return NotImplemented
        return self._job_type == other._job_type

    def get_info(self):
        return self.__str__()

    def to_file_string(self):
        return self._job_type + " - " + str(self._workers) + " чел."
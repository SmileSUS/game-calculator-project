class JobService:

    def __init__(self, action_service):
        self._action_service = action_service

    def assign(self, settlement, job_type, workers):
        job_type = job_type.strip()
        if job_type == "":
            raise ValueError("Укажите тип работы")

        if workers <= 0:
            raise ValueError("Количество должно быть больше нуля")

        if workers > settlement.get_free():
            raise ValueError("Недостаточно свободных жителей. Свободно: " + str(settlement.get_free()))

        time_in = self._action_service.now_string()
        job = settlement.assign_job(job_type, workers, time_in)

        description = "Назначен " + job_type + " x" + str(workers) + " в " + settlement.get_name()
        self._action_service.log(description)

        return job

    def remove(self, settlement, job_type):
        job = settlement.find_job(job_type)
        if job is None:
            return None

        settlement.remove_job(job_type)

        description = "Назначен " + job_type + " x" + str(job.get_workers()) + " в " + settlement.get_name()
        self._action_service.close_by_prefix(description)

        self._action_service.log("Убран " + job_type + " в " + settlement.get_name())

        return job

    def get_all(self, settlement):
        return settlement.get_jobs().get_all()
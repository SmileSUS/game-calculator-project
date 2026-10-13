class JobStorage:

    def __init__(self):
        self._items = []

    def add(self, job):
        self._items.append(job)

    def get_all(self):
        return self._items

    def find_by_type(self, job_type):
        for job in self._items:
            if job.get_job_type() == job_type:
                return job
        return None

    def remove_by_type(self, job_type):
        new_list = []
        for job in self._items:
            if job.get_job_type() != job_type:
                new_list.append(job)
        self._items = new_list

    def clear(self):
        self._items = []

    def count(self):
        return len(self._items)

    def total_workers(self):
        total = 0
        for job in self._items:
            total = total + job.get_workers()
        return total
import os

from utils import CustomDict


class SaveManager:

    def __init__(self, filename):
        self._filename = filename

    def get_filename(self):
        return self._filename

    def exists(self):
        return os.path.exists(self._filename)

    def delete(self):
        if self.exists():
            os.remove(self._filename)

    def save(self, provinces, actions):
        with open(self._filename, "w", encoding="utf-8") as file:
            for province in provinces:
                file.write("PROVINCE\t" + province.get_name() + "\n")

                for settlement in province.get_settlements().get_all():
                    line = ("SETTLEMENT\t" + province.get_name() +
                            "\t" + settlement.get_name() +
                            "\t" + str(settlement.get_total_population()) + "\n")
                    file.write(line)

                    for job in settlement.get_jobs().get_all():
                        job_line = ("JOB\t" + province.get_name() +
                                    "\t" + settlement.get_name() +
                                    "\t" + job.get_job_type() +
                                    "\t" + str(job.get_workers()) +
                                    "\t" + job.get_time_in() + "\n")
                        file.write(job_line)

            for action in actions:
                action_line = ("ACTION\t" + action.get_description() +
                               "\t" + action.get_time_in() +
                               "\t" + action.get_time_out() + "\n")
                file.write(action_line)

    def load(self):
        if not self.exists():
            return None

        provinces = []
        actions = []
        current_province = None

        with open(self._filename, "r", encoding="utf-8") as file:
            for raw_line in file:
                line = raw_line.rstrip("\n")
                if line == "":
                    continue

                parts = line.split("\t")
                kind = parts[0]

                if kind == "PROVINCE":
                    data = CustomDict()
                    data.set("name", parts[1])
                    current_province = data
                    provinces.append(data)

                elif kind == "SETTLEMENT":
                    data = CustomDict()
                    data.set("province_name", parts[1])
                    data.set("name", parts[2])
                    data.set("population", int(parts[3]))
                    data.set("jobs", [])
                    if current_province is not None:
                        current_province.get("settlements", None)
                        settlements = current_province.get("settlements")
                        if settlements is None:
                            settlements = []
                            current_province.set("settlements", settlements)
                        settlements.append(data)

                elif kind == "JOB":
                    data = CustomDict()
                    data.set("province_name", parts[1])
                    data.set("settlement_name", parts[2])
                    data.set("job_type", parts[3])
                    data.set("workers", int(parts[4]))
                    data.set("time_in", parts[5])

                    if current_province is not None:
                        settlements = current_province.get("settlements", [])
                        for settlement in settlements:
                            if settlement.get("name") == parts[2]:
                                jobs = settlement.get("jobs")
                                jobs.append(data)

                elif kind == "ACTION":
                    data = CustomDict()
                    data.set("description", parts[1])
                    data.set("time_in", parts[2])
                    data.set("time_out", parts[3] if len(parts) > 3 else "")
                    actions.append(data)

        if len(provinces) == 0 and len(actions) == 0:
            return None

        result = CustomDict()
        result.set("provinces", provinces)
        result.set("actions", actions)
        return result
class ReportWriter:

    def __init__(self, filename):
        self._filename = filename

    def get_filename(self):
        return self._filename

    def write(self, action_storage):
        separator = "+------------------------------+---------------------+----------------------+"
        header = "| login                        | time_in             | time_out             |"

        with open(self._filename, "w", encoding="utf-8") as file:
            file.write(separator + "\n")
            file.write(header + "\n")
            file.write("|------------------------------|---------------------|----------------------|\n")

            for line in action_storage.to_file_lines():
                file.write(line + "\n")

            file.write(separator + "\n")
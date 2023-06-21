import csv
import atexit
from datetime import datetime


class CSVLogger:
    def __init__(self):
        self.running = True
        atexit.register(self.stop)

    def write_log(self, queue, experiment_name):
        self.running = True
        print(experiment_name)
        file_name = datetime.now().strftime(
            "logs/" + experiment_name + "_log-%Y-%m-%d-%H-%M.csv"
        )
        with open(file_name, "a+") as self.f:
            writer = csv.writer(self.f, delimiter=",", quoting=csv.QUOTE_NONE)
            writer.writerow(
                (
                    "time",
                    "C0_ppb",
                    "current_north_m",
                    "current_east_m",
                    "current_down_m",
                    "desired_north_m",
                    "desired_east_m",
                    "desired_down_m",
                )
            )
            print("writing to file")
            while self.running:
                if queue.empty():
                    continue
                csv_line = queue.get()
                writer.writerow(csv_line)
            self.f.close()

    def stop(self):
        self.running = False
        # if hasattr(self, "f"):
        #     self.f.close()

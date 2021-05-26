import os
from datetime import datetime


class CsvSaver:
    @staticmethod
    def save(filename, wallet_stats):
        if not os.path.exists(filename):
            with open(filename, "w") as file:
                file.write("time,")
                for stat in wallet_stats:
                    file.write(f"{stat},")
                file.write("\n")
        with open(filename, "a") as file:
            file.write(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')},")
            for stat in wallet_stats:
                file.write(f"{round(wallet_stats[stat], 3)},")
            file.write("\n")

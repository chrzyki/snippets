import csv
from collections import defaultdict
from pathlib import Path

from dbfpy3 import dbf


DBF_PATHS = (Path.cwd() / "dbf_files").glob("**/*")

DBF_FILES = sorted([str(f.resolve()) for f in DBF_PATHS if f.is_file()])


def get_year(s):
    i = s.find("DATA")
    return s[71:i]


# A nested structure to store the result of iterating over the dbf files.
# Basically something like this: {"FAMILY" : {"COUNT": []}, {"AREA": []}, {"MEAN": []}}
d = defaultdict(lambda: defaultdict(list))


for f in DBF_FILES:
    db = dbf.Dbf(f)
    year = int(get_year(f))  # Not used, but could be/should be used for verification.

    for record in db:
        current_record = record.asDict()
        family = current_record["ETHNIC_GRO"]
        count = current_record["COUNT"]
        area = current_record["AREA"]
        mean = current_record["MEAN"]

        d[family]["COUNT"].append(count)
        d[family]["AREA"].append(area)
        d[family]["MEAN"].append(mean)


headers = ["Family"]
headers.extend(["COUNT_" + str(x) for x in range(2000, 2016)])
headers.extend(["AREA_" + str(x) for x in range(2000, 2016)])
headers.extend(["MEAN_" + str(x) for x in range(2000, 2016)])


with open("out.csv", "w", newline="") as csvfile:
    db_writer = csv.writer(csvfile, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)

    db_writer.writerow(headers)

    for key, value in sorted(d.items()):
        row = [key]
        row.extend(value["COUNT"])
        row.extend(value["AREA"])
        row.extend(value["MEAN"])
        db_writer.writerow(row)

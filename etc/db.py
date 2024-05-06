import logging
from pathlib import Path
from typing import Any, Dict
from tinydb import TinyDB, Query
from tinydb.storages import Storage
import csv
import os
import hashlib

logger = logging.getLogger(__name__)
CSV_FILE = os.environ.get("CSV_FILE", "etc.csv")


class CsvStorage(Storage):
    def __init__(self, filename):
        self.rows = []
        self.fieldnames = []
        if Path(filename).exists():
            reader = csv.DictReader(open(filename, encoding="utf-8"))
            self.fieldnames = reader.fieldnames or []
            self.rows = list(reader)
        self.file = open(filename, "w+", encoding="utf-8")
        self.last_data = {
            TinyDB.default_table_name: {str(i): row for i, row in enumerate(self.rows)}
        }

    def read(self):
        return self.last_data

    def write(self, data: Dict[str, Dict[str, Any]]):
        if not self.fieldnames:
            self.fieldnames = list(
                list(data[TinyDB.default_table_name].values())[0].keys()
            )
        self.last_data = data

    def close(self):
        writer = csv.DictWriter(self.file, self.fieldnames)
        writer.writeheader()
        for row in self.last_data[TinyDB.default_table_name].values():
            writer.writerow(row)
        self.file.close()


db = TinyDB(CSV_FILE, storage=CsvStorage)


# unique key is 利用年月日（自）+ 時分（自）+ 利用年月日（至）+ 時分（至）
def get_unique_key(row):
    payload = ",".join(
        [
            row["利用年月日（自）"],
            row["時分（自）"],
            row["利用年月日（至）"],
            row["時分（至）"],
        ]
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def insert(row) -> bool:
    """
    result: True if insert new row, False if update exist row
    """
    # check if exist
    row["unique_key"] = get_unique_key(row)
    Record = Query()
    result = db.search(Record["unique_key"] == row["unique_key"])
    if result:
        exist_row = result[0]
        if exist_row != row:
            logger.info(f"update row: {row}")
            db.update(row, Record["unique_key"] == row["unique_key"])
        return False
    db.insert(row)
    return True


def close():
    db.close()

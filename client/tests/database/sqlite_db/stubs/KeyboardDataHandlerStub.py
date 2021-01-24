import json
import os
import pathlib
from src.database.sqlite_db.SqliteDataHandler import SqliteDataHandler


class KeyboardDataHandlerStub(SqliteDataHandler):

    def __init__(self, name, path=""):
        super().__init__(path)
        test_dir = pathlib.Path(__file__).parent.parent.parent.parent.absolute()
        if not os.path.isdir("../test_output"):
            os.mkdir("../test_output")
        if not os.path.isdir("../test_output/kb"):
            os.mkdir("../test_output/kb")
        self.out_path = os.path.join(test_dir, 'test_output', 'kb')
        self.create_table()
        self.name = name

    def save(self, data):
        with open(f"{self.out_path}\\{self.name}_kb.json", 'w+') as features_file:
            json.dump(data, features_file)

    def create_table(self):
        pass

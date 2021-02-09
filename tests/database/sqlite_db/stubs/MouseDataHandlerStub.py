import os
import json
import pathlib
from oratio.database.sqlite_db.SqliteDataHandler import SqliteDataHandler


class MouseDataHandlerStub(SqliteDataHandler):

    def __init__(self, name, path=""):
        super().__init__(path)
        test_dir = pathlib.Path(__file__).parent.parent.parent.parent.absolute()
        self.out_path = os.path.join(test_dir, 'test_output')
        if not os.path.isdir(self.out_path):
            os.mkdir(self.out_path)
        self.out_path = os.path.join(self.out_path, 'mouse')
        if not os.path.isdir(self.out_path):
            os.mkdir(self.out_path)

        self.name = name

    def save(self, data):
        with open(f"{self.out_path}\\{self.name}_mouse.json", 'w+') as features_file:
            json.dump(data, features_file)

    def create_data_holder(self):
        pass

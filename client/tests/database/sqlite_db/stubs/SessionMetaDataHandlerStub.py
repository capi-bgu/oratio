import os
import json
import pathlib
from src.database.sqlite_db.SqliteDataHandler import SqliteDataHandler


class SessionMetaDataHandlerStub(SqliteDataHandler):

    def __init__(self, name, path=""):
        super().__init__(path)
        test_dir = pathlib.Path(__file__).parent.parent.parent.parent.absolute()
        self.out_path = os.path.join(test_dir, 'test_output')
        if not os.path.isdir(self.out_path):
            os.mkdir(self.out_path)
        self.out_path = os.path.join(self.out_path, 'session')
        if not os.path.isdir(self.out_path):
            os.mkdir(self.out_path)

        self.name = name

    def save(self, data):
        with open(f"{self.out_path}\\{self.name}_meta.json", 'w') as features_file:
            json.dump(data, features_file)

    def create_data_holder(self):
        pass

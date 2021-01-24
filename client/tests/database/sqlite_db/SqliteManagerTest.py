import os
import pathlib
import unittest
from src.database.sqlite_db.SqliteManager import SqliteManager


class SqliteManagerTest(unittest.TestCase):
    def test(self):
        test_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
        if not os.path.isdir("../test_output"):
            os.mkdir("../test_output")
        if not os.path.isdir("../test_output/img"):
            os.mkdir("../test_output/img")
        self.out_path = os.path.join(test_dir, 'test_output', 'img')
        self.db_path = os.path.join(self.out_path, 'data.db')

        assert not os.path.isfile(self.db_path)
        manager = SqliteManager(path=self.out_path)
        manager.create_database()
        assert os.path.isfile(self.db_path)


if __name__ == '__main__':
    unittest.main()

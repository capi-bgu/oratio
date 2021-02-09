import os
import pathlib
import unittest
from oratio.database.sqlite_db.SqliteManager import SqliteManager


class SqliteManagerTest(unittest.TestCase):
    def test(self):
        test_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
        self.out_path = os.path.join(test_dir, 'test_output')
        if not os.path.isdir(self.out_path):
            os.mkdir(self.out_path)
        self.db_path = os.path.join(self.out_path, 'capi_client.db')

        self.assertFalse(os.path.isfile(self.db_path))
        manager = SqliteManager(path=self.out_path)
        manager.create_data_holder()
        self.assertTrue(os.path.isfile(self.db_path))
        res = manager.ask("SELECT name FROM sqlite_master WHERE type='table' AND name='Session';")
        self.assertIn(("Session",), res)


if __name__ == '__main__':
    unittest.main()

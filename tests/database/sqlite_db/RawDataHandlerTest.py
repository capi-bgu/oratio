import os
import pickle
import pathlib
import unittest
from oratio.database.sqlite_db.SqliteManager import SqliteManager
from oratio.database.sqlite_db.RawDataHandler import RawDataHandler


class CameraDataHandlerTest(unittest.TestCase):

    def test(self):
        name = "RawDataTest"
        data = [1, 2, 3, {'a': 1, 'b': 2}]

        test_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
        self.out_path = os.path.join(test_dir, 'test_output')
        if not os.path.isdir(self.out_path):
            os.mkdir(self.out_path)

        manager = SqliteManager(path=self.out_path)
        manager.create_data_holder()

        res = manager.ask(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{name}';")
        self.assertNotIn((name,), res)

        self.data_handler = RawDataHandler(name=name, path=self.out_path)
        self.data_handler.create_data_holder()
        res = manager.ask(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{name}';")
        self.assertIn((name,), res)

        res = manager.ask(f"SELECT * FROM {name} WHERE session='{name}'")
        self.assertEqual(len(res), 0)

        self.data_handler.save((name, data))
        res = manager.ask(f"SELECT * FROM {name} WHERE session='{name}'")
        self.assertEqual(len(res), 1)
        key = res[0][0]
        res_data = res[0][1]
        res_data = pickle.loads(res_data)
        self.assertEqual(key, name)
        self.assertEqual(data, res_data)


if __name__ == '__main__':
    unittest.main()

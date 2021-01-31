import os
import pathlib
import unittest
from threading import Thread

from src.database.sqlite_db.SqliteManager import SqliteManager
from src.database.sqlite_db.KeyboardDataHandler import KeyboardDataHandler
from tests.processing.stubs.KeyboardProcessorStub import KeyboardProcessorStub


class KeyboardDataHandlerTest(unittest.TestCase):
    def test(self):
        keyboard_processor = KeyboardProcessorStub()
        processor = Thread(target=keyboard_processor.process_data, args=(None, None))
        processor.start()
        processor.join()

        test_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
        self.out_path = os.path.join(test_dir, 'test_output')
        if not os.path.isdir(self.out_path):
            os.mkdir(self.out_path)

        manager = SqliteManager(path=self.out_path)
        manager.create_database()

        res = manager.ask("SELECT name FROM sqlite_master WHERE type='table' AND name='Keyboard';")
        self.assertNotIn("Keyboard", res)

        self.data_handler = KeyboardDataHandler(path=self.out_path)
        self.data_handler.create_data_holder()
        res = manager.ask("SELECT name FROM sqlite_master WHERE type='table' AND name='Keyboard';")
        self.assertIn(("Keyboard",), res)

        res = manager.ask("SELECT * FROM Keyboard WHERE session='KeyboardHandlerTest'")
        self.assertTrue(len(res) == 0)

        self.data_handler.save(("KeyboardHandlerTest", keyboard_processor.features))
        res = manager.ask("SELECT * FROM Keyboard WHERE session='KeyboardHandlerTest'")
        self.assertTrue(len(res) == 1)
        key = res[0][0]
        self.assertEqual(key, 'KeyboardHandlerTest')
        for i, val in enumerate(list(keyboard_processor.features.values())):
            self.assertEqual(val, res[0][i+1])



if __name__ == '__main__':
    unittest.main()

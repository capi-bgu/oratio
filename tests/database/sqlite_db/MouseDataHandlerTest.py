import os
import pathlib
import unittest
from threading import Thread
from src.database.sqlite_db.SqliteManager import SqliteManager
from src.database.sqlite_db.MouseDataHandler import MouseDataHandler
from tests.processing.stubs.MouseProcessorStub import MouseProcessorStub


class MouseDataHandlerTest(unittest.TestCase):
    def test(self):
        mouse_processor = MouseProcessorStub()
        processor = Thread(target=mouse_processor.process_data, args=(None, None))
        processor.start()
        processor.join()

        test_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
        self.out_path = os.path.join(test_dir, 'test_output')
        if not os.path.isdir(self.out_path):
            os.mkdir(self.out_path)

        manager = SqliteManager(path=self.out_path)
        manager.create_data_holder()
        
        res = manager.ask("SELECT name FROM sqlite_master WHERE type='table' AND name='Mouse';")
        self.assertNotIn(("Mouse",), res)

        self.data_handler = MouseDataHandler(path=self.out_path)
        self.data_handler.create_data_holder()
        res = manager.ask("SELECT name FROM sqlite_master WHERE type='table' AND name='Mouse';")
        self.assertIn(("Mouse",), res)

        res = manager.ask("SELECT session FROM Mouse WHERE session='MouseHandlerTest'")
        self.assertEqual(len(res), 0)

        self.data_handler.save(("MouseHandlerTest", mouse_processor.features))
        res = manager.ask("SELECT * FROM Mouse WHERE session='MouseHandlerTest'")
        self.assertEqual(len(res), 1)
        key = res[0][0]
        self.assertEqual(key, 'MouseHandlerTest')
        for i, val in enumerate(list(mouse_processor.features.values())):
            self.assertEqual(val, res[0][i + 1])


if __name__ == '__main__':
    unittest.main()

import os
import pathlib
import unittest
from src.database.sqlite_db.SqliteManager import SqliteManager
from src.database.sqlite_db.MouseDataHandler import MouseDataHandler
from tests.processing.stubs.MouseProcessorStub import MouseProcessorStub


class MouseDataHandlerTest(unittest.TestCase):
    def test(self):
        mouse_processor = MouseProcessorStub()
        mouse_processor.set_arguements(None, None)
        mouse_processor.start()
        mouse_processor.join()

        test_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
        self.out_path = os.path.join(test_dir, 'test_output')
        if not os.path.isdir(self.out_path):
            os.mkdir(self.out_path)

        manager = SqliteManager(path=self.out_path)
        manager.create_database()
        
        res = manager.ask("SELECT name FROM sqlite_master WHERE type='table' AND name='Mouse';")
        self.assertNotIn("Mouse", res)

        self.data_handler = MouseDataHandler(path=self.out_path)
        res = manager.ask("SELECT name FROM sqlite_master WHERE type='table' AND name='Mouse';")
        self.assertIn(("Mouse",), res)

        res = manager.ask("SELECT session FROM Mouse WHERE session='MouseHandlerTest'")
        self.assertTrue(len(res) == 0)

        self.data_handler.save(("MouseHandlerTest", mouse_processor.features))
        res = manager.ask("SELECT * FROM Mouse WHERE session='MouseHandlerTest'")
        self.assertTrue(len(res) == 1)
        key = res[0][0]
        self.assertEqual(key, 'MouseHandlerTest')
        for i, val in enumerate(list(mouse_processor.features.values())):
            self.assertEqual(val, res[0][i + 1])


if __name__ == '__main__':
    unittest.main()

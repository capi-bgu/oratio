import os
import pathlib
import unittest
from src.database.sqlite_db.SqliteManager import SqliteManager
from src.database.sqlite_db.KeyboardDataHandler import KeyboardDataHandler
from tests.processing.stubs.KeyboardProcessorStub import KeyboardProcessorStub


class KeyboardDataHandlerTest(unittest.TestCase):
    def test(self):
        keyboard_processor = KeyboardProcessorStub()
        keyboard_processor.set_arguements(None, None)
        keyboard_processor.start()
        keyboard_processor.join()

        test_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
        self.out_path = os.path.join(test_dir, 'test_output')
        if not os.path.isdir(self.out_path):
            os.mkdir(self.out_path)

        manager = SqliteManager(path=self.out_path)
        manager.create_database()
        data_handler = KeyboardDataHandler(path=self.out_path)
        data_handler.save(("KeyboardHandlerTest", keyboard_processor.features))


if __name__ == '__main__':
    unittest.main()

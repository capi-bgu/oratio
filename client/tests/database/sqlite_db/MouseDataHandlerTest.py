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
        data_handler = MouseDataHandler(path=self.out_path)
        data_handler.save(("MouseHandlerTest", mouse_processor.features))


if __name__ == '__main__':
    unittest.main()

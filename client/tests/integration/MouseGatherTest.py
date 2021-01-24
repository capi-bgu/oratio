import os
import pathlib
import time
import unittest
from tests.SessionStub import SessionStub
from src.collection.MouseCollector import MouseCollector
from src.processing.MouseProcessor import MouseProcessor
from tests.database.sqlite_db.stubs.MouseDataHandlerStub import MouseDataHandlerStub


class MouseGatherTest(unittest.TestCase):
    def test(self):
        mouse_processor = MouseProcessor()
        mouse_collector = MouseCollector()

        self.st = time.time()
        session = SessionStub(1, 5, self.st)

        st = time.time()
        mouse_collector.start()
        time.sleep(session.session_duration)
        data = mouse_collector.stop_collect()
        mouse_collector.join()
        print(time.time() - st)

        st = time.time()
        mouse_processor.set_arguements(data, session)
        mouse_processor.start()
        mouse_processor.join()
        features = mouse_processor.features
        print(time.time() - st)

        data_handler = MouseDataHandlerStub(name="gathered")
        data_handler.save(features)

    def save_data(self, data):
        test_dir = pathlib.Path(__file__).parent.parent.absolute()
        output_path = os.path.join(test_dir, 'test_output', 'mouse')

        f = open(f"{output_path}\\_mouse.txt", "w+")
        f.write(str(self.st) + '\n')
        for i, e in enumerate(data):
            f.write(str(i) + '. ' + str(e.__dict__) + '\n')
        f.close()


if __name__ == '__main__':
    unittest.main()

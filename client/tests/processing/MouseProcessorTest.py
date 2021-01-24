import time
import unittest
from tests.SessionStub import SessionStub
from src.processing.MouseProcessor import MouseProcessor
from tests.collection.stubs.MouseCollectorStub import MouseCollectorStub
from tests.database.sqlite_db.stubs.MouseDataHandlerStub import MouseDataHandlerStub


class MouseProcessorTest(unittest.TestCase):
    def test(self):
        mouse_collector = MouseCollectorStub()
        mouse_collector.start()
        mouse_collector.join()
        start_time, data = mouse_collector.stop_collect()

        self.mpt = MouseProcessor()
        session_duration = 5
        session = SessionStub(0, session_duration, start_time)
        self.mpt.set_arguements(data, session)

        st = time.time()
        self.mpt.start()
        self.mpt.join()
        features = self.mpt.features
        print(time.time() - st)

        data_handler = MouseDataHandlerStub(name="processed")
        data_handler.save(features)


if __name__ == '__main__':
    unittest.main()

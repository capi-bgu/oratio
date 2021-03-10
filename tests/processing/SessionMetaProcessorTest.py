import time
import logging
import unittest
from threading import Thread
from tests.SessionStub import SessionStub
from oratio.processing.SessionMetaProcessor import SessionMetaProcessor
from tests.collection.stubs.SessionMetaCollectorStub import SessionMetaCollectorStub
from tests.database.sqlite_db.stubs.SessionMetaDataHandlerStub import SessionMetaDataHandlerStub


class SessionMetaProcessorTest(unittest.TestCase):

    def test(self):
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')

        session_collector = SessionMetaCollectorStub()
        session_collector.start_collect()
        data = session_collector.stop_collect()

        self.session_processor = SessionMetaProcessor()
        session_duration = 5
        start_time = time.time()
        session = SessionStub("SessionMetaProcessingTest", session_duration, start_time)
        processor = Thread(target=self.session_processor.process_data, args=(data, session))
        processor.start()
        processor.join()
        features = self.session_processor.features
        logging.debug(time.time() - start_time)
        self.assertEqual(features['dominate_window'], "pycharm64.exe")
        self.assertEqual(features['dominate_task'], "writing")
        self.assertEqual(features['window_switches'], 4)
        self.assertEqual(features['task_switches'], 0)
        self.assertEqual(features['window_count'], 4)
        self.assertEqual(features['task_count'], 1)

        data_handler = SessionMetaDataHandlerStub(name="processed")
        data_handler.save(features)


if __name__ == '__main__':
    unittest.main()

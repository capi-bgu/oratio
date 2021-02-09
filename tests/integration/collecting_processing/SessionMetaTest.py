import time
import logging
import unittest
from threading import Thread
from tests.SessionStub import SessionStub
from oratio.collection.SessionMetaCollector import SessionMetaCollector
from oratio.processing.SessionMetaProcessor import SessionMetaProcessor
from tests.database.sqlite_db.stubs.SessionMetaDataHandlerStub import SessionMetaDataHandlerStub


class SessionMetaTest(unittest.TestCase):

    def test(self):
        self.session_collector = SessionMetaCollector(record_window=1)
        self.session_processor = SessionMetaProcessor()
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')


        start_time = time.time()
        session = SessionStub("SessionMetaCollectingProcessingTest", duration=5, start_time=start_time)

        # collecting
        start_time = time.time()
        collector = Thread(target=self.session_collector.start_collect)
        collector.start()
        time.sleep(session.duration)
        data = self.session_collector.stop_collect()
        collector.join()
        logging.debug(time.time() - start_time)

        # processing
        start_time = time.time()
        processor = Thread(target=self.session_processor.process_data, args=(data, session))
        processor.start()
        processor.join()
        features = self.session_processor.features
        logging.debug(time.time() - start_time)

        data_handler = SessionMetaDataHandlerStub(name="gathered")
        data_handler.save(features)


if __name__ == '__main__':
    unittest.main()

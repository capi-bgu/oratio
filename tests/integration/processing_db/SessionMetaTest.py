import os
import time
import logging
import pathlib
import unittest
from threading import Thread
from tests.SessionStub import SessionStub
from oratio.database.sqlite_db.SqliteManager import SqliteManager
from oratio.processing.SessionMetaProcessor import SessionMetaProcessor
from oratio.database.sqlite_db.SessionMetaDataHandler import SessionMetaDataHandler
from tests.collection.stubs.SessionMetaCollectorStub import SessionMetaCollectorStub


class SessionMetaTest(unittest.TestCase):

    def test(self):
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')

        self.session_collector = SessionMetaCollectorStub()
        self.session_processor = SessionMetaProcessor()

        start_time = time.time()
        session = SessionStub("SessionMetaIntegrationDBTest", duration=5, start_time=start_time)

        # collecting
        self.session_collector.start_collect()
        data = self.session_collector.stop_collect()

        # processing
        start_time = time.time()
        processor = Thread(target=self.session_processor.process_data, args=(data, session))
        processor.start()
        processor.join()
        features = self.session_processor.features
        logging.debug(time.time() - start_time)

        # database
        test_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
        self.out_path = os.path.join(test_dir, 'test_output')

        manager = SqliteManager(path=self.out_path)
        manager.create_data_holder()

        start_time = time.time()
        data_handler = SessionMetaDataHandler(path=self.out_path)
        data_handler.create_data_holder()
        data_handler.save((session.id, self.session_processor.features))
        logging.debug(time.time() - start_time)
        res = manager.ask(f"SELECT * FROM SessionMeta WHERE session='{session.id}'")
        self.assertEqual(len(res), 1)
        key = res[0][0]
        self.assertEqual(key, session.id)
        for i, val in enumerate(list(self.session_processor.features.values())):
            self.assertEqual(val, res[0][i + 1])


if __name__ == '__main__':
    unittest.main()
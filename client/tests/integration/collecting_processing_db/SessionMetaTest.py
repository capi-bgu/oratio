import os
import pathlib
import time
import unittest
from threading import Thread

from src.collection.SessionMetaCollector import SessionMetaCollector
from src.database.sqlite_db.SessionMetaDataHandler import SessionMetaDataHandler
from src.database.sqlite_db.SqliteManager import SqliteManager
from src.processing.SessionMetaProcessor import SessionMetaProcessor
from tests.SessionStub import SessionStub


class SessionMetaTest(unittest.TestCase):

    def test(self):
        self.session_collector = SessionMetaCollector(record_window=1)
        self.session_processor = SessionMetaProcessor()

        start_time = time.time()
        session = SessionStub("SessionMetaFullTest", session_duration=5, session_start_time=start_time)

        # collecting
        start_time = time.time()
        collector = Thread(target=self.session_collector.start_collect)
        collector.start()
        time.sleep(session.session_duration)
        data = self.session_collector.stop_collect()
        collector.join()
        print(f"collection runtime: {time.time() - start_time}")

        # processing
        start_time = time.time()
        processor = Thread(target=self.session_processor.process_data, args=(data, session))
        processor.start()
        processor.join()
        features = self.session_processor.features
        print(f"processing time: {time.time() - start_time}")

        # database
        test_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
        self.out_path = os.path.join(test_dir, 'test_output')

        manager = SqliteManager(path=self.out_path)
        manager.create_database()

        start_time = time.time()
        data_handler = SessionMetaDataHandler(path=self.out_path)
        data_handler.create_data_holder()
        data_handler.save((session.session_name, self.session_processor.features))
        print(f"database save time: {time.time() - start_time}")
        res = manager.ask(f"SELECT * FROM SessionMeta WHERE session='{session.session_name}'")
        self.assertEqual(len(res), 1)
        key = res[0][0]
        self.assertEqual(key, session.session_name)
        for i, val in enumerate(list(self.session_processor.features.values())):
            self.assertEqual(val, res[0][i + 1])


if __name__ == '__main__':
    unittest.main()

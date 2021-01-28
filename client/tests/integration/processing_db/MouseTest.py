import os
import time
import pathlib
import unittest
from tests.SessionStub import SessionStub
from src.processing.MouseProcessor import MouseProcessor
from src.database.sqlite_db.SqliteManager import SqliteManager
from src.database.sqlite_db.MouseDataHandler import MouseDataHandler
from tests.collection.stubs.MouseCollectorStub import MouseCollectorStub


class KeyboardTest(unittest.TestCase):
    def test(self):
        # collecting
        mouse_collector = MouseCollectorStub()
        mouse_collector.start()
        mouse_collector.join()
        start_time, data = mouse_collector.stop_collect()

        # processing
        self.mpt = MouseProcessor()
        session_duration = 5
        session = SessionStub("MouseIntegrationTest", session_duration, start_time)
        self.mpt.set_arguements(data, session)
        st = time.time()
        self.mpt.start()
        self.mpt.join()
        print(time.time() - st)

        # database
        test_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
        self.out_path = os.path.join(test_dir, 'test_output')

        manager = SqliteManager(path=self.out_path)
        manager.create_database()

        st = time.time()
        data_handler = MouseDataHandler(path=self.out_path)
        data_handler.create_data_holder()
        data_handler.save(("MouseIntegrationTest", self.mpt.features))
        print(time.time() - st)
        res = manager.ask(f"SELECT * FROM Mouse WHERE session='{session.session_name}'")
        self.assertTrue(len(res) == 1)
        key = res[0][0]
        self.assertEqual(key, session.session_name)
        for i, val in enumerate(list(self.mpt.features.values())):
            self.assertEqual(val, res[0][i + 1])


if __name__ == '__main__':
    unittest.main()

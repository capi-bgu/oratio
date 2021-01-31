import os
import pathlib
import unittest
from threading import Thread
from src.database.sqlite_db.SqliteManager import SqliteManager
from src.database.sqlite_db.SessionMetaDataHandler import SessionMetaDataHandler
from tests.processing.stubs.SessionMetaProcessorStub import SessionMetaProcessorStub


class SessionMetaDataHandlerTest(unittest.TestCase):

    def test(self):
        session_processor = SessionMetaProcessorStub()
        processor = Thread(target=session_processor.process_data, args=(None, None))
        processor.start()
        processor.join()

        test_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
        self.out_path = os.path.join(test_dir, 'test_output')

        manager = SqliteManager(path=self.out_path)
        manager.create_database()

        res = manager.ask("SELECT name FROM sqlite_master WHERE type='table' AND name='SessionMeta';")
        self.assertNotIn(("SessionMeta",), res)

        self.data_handler = SessionMetaDataHandler(path=self.out_path)
        self.data_handler.create_data_holder()

        res = manager.ask("SELECT name FROM sqlite_master WHERE type='table' AND name='SessionMeta';")
        self.assertIn(("SessionMeta",), res)

        res = manager.ask("SELECT * from SessionMeta WHERE session='SessionMetaHandlerTest'")
        self.assertEqual(len(res), 0)

        self.data_handler.save(('SessionMetaHandlerTest', session_processor.features))
        res = manager.ask("SELECT * from SessionMeta WHERE session='SessionMetaHandlerTest'")
        self.assertEqual(len(res), 1)

        key = res[0][0]
        self.assertEqual(key, 'SessionMetaHandlerTest')
        for i, val in enumerate(list(session_processor.features.values())):
            self.assertEqual(val, res[0][i + 1])


if __name__ == '__main__':
    unittest.main()
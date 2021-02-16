import os
import time
import pickle
import logging
import pathlib
import unittest
from threading import Thread
from pynput.mouse import Button
from tests.SessionStub import SessionStub
from pynput.mouse import Controller as MouseController
from oratio.collection.PynputMouseCollector import PynputMouseCollector
from oratio.processing.IdentityProcessor import IdentityProcessor
from oratio.database.sqlite_db.SqliteManager import SqliteManager
from oratio.database.sqlite_db.RawDataHandler import RawDataHandler


class PynputMouseRawTest(unittest.TestCase):
    def test(self):
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')

        st = time.time()
        session = SessionStub("MouseFullTest", 5, st)
        self.mouse_controller = MouseController()

        # collecting
        self.mouse_collector = PynputMouseCollector()
        collector = Thread(target=self.mouse_collector.start_collect)
        user = Thread(target=self.simulate_user)
        st = time.time()
        collector.start()
        user.start()
        time.sleep(session.duration)
        data = self.mouse_collector.stop_collect()
        collector.join()
        logging.debug(time.time() - st)
        user.join()

        # processing
        self.mouse_processor = IdentityProcessor()
        processor = Thread(target=self.mouse_processor.process_data, args=(data, session))
        processor.start()
        processor.join()
        logging.debug(time.time() - st)

        # database
        test_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
        self.out_path = os.path.join(test_dir, 'test_output')

        manager = SqliteManager(path=self.out_path)
        manager.create_data_holder()

        st = time.time()
        data_handler = RawDataHandler(name="PynputMouseRawData", path=self.out_path)
        data_handler.create_data_holder()
        data_handler.save((session.id, self.mouse_processor.features))
        logging.debug(time.time() - st)
        res = manager.ask(f"SELECT * FROM PynputMouseRawData WHERE session='{session.id}'")
        self.assertEqual(len(res), 1)
        key = res[0][0]
        data = res[0][1]
        data = pickle.loads(data)
        self.assertEqual(key, session.id)
        self.assertEqual(len(data), len(self.mouse_processor.features))
        for ret, expected in zip(data, self.mouse_processor.features):
            self.assertEqual(ret.__dict__, expected.__dict__)

    def simulate_user(self):
        time.sleep(1.5)
        self.mouse_controller.press(Button.right)
        time.sleep(0.05)
        self.mouse_controller.release(Button.right)
        time.sleep(0.3)
        self.mouse_controller.move(-20, 20)
        time.sleep(0.01)
        self.mouse_controller.press(Button.left)
        time.sleep(0.05)
        self.mouse_controller.release(Button.left)
        time.sleep(0.7)
        self.mouse_controller.click(Button.left, 3)
        time.sleep(0.3)
        self.mouse_controller.scroll(0, 5)
        time.sleep(0.3)
        self.mouse_controller.scroll(0, -5)


if __name__ == '__main__':
    unittest.main()

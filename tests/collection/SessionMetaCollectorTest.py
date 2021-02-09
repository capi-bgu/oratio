import os
import json
import time
import pathlib
import logging
import unittest
from threading import Thread
from src.collection.SessionMetaCollector import SessionMetaCollector


def process_data(data):
    test_dir = pathlib.Path(__file__).parent.parent.absolute()
    output_path = os.path.join(test_dir, 'test_output')
    if not os.path.isdir(output_path):
        os.mkdir(output_path)

    output_path = os.path.join(output_path, 'session')
    if not os.path.isdir(output_path):
        os.mkdir(output_path)

    output_path = os.path.join(output_path, 'raw_meta.json')
    with open(output_path, 'w') as test_out:
        json.dump(data, test_out)


class SessionMetaCollectorTest(unittest.TestCase):

    def test(self):
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')
        self.session_meta_collector = SessionMetaCollector(record_window=1)
        collector = Thread(target=self.session_meta_collector.start_collect)
        collector.start()
        self.session_duration = 5
        time.sleep(self.session_duration)
        data = self.session_meta_collector.stop_collect()

        self.assertEqual(len(data), self.session_duration / self.session_meta_collector.record_window)

        process_data(data)


if __name__ == '__main__':
    unittest.main()

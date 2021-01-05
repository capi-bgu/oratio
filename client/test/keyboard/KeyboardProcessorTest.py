import unittest
from src.Session import Session
from src.collection.KeyboardCollector import KeyboardCollector
from src.processing.KeyboardProcessor import KeyboardProcessor


class KeyboardProcessorTest(unittest.TestCase):
    def test(self):
        self.keyboard_processor = KeyboardProcessor("")
        self.session = Session(0, 10)
        self.keyboard_collector = KeyboardCollector(self.session, self.keyboard_processor)
        self.keyboard_collector.start_collect()


if __name__ == '__main__':
    unittest.main()

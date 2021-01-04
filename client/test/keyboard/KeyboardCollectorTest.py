import unittest
from src.Session import Session
from src.collection.KeyboardCollector import KeyboardCollector
from KeyboardProcessorStub import KeyboardProcessorStub


class KeyboardCollectorTest(unittest.TestCase):
    def test(self):
        self.keyboard_processor_stub = KeyboardProcessorStub()
        self.session = Session(1, 5)
        self.keyboard_collector = KeyboardCollector(self.session, self.keyboard_processor_stub)
        self.keyboard_collector.start_collect()


if __name__ == '__main__':
    unittest.main()

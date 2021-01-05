import unittest
from src.Session import Session
from src.collection.MouseCollector import MouseCollector
from src.processing.MouseProcessor import MouseProcessor


class MouseProcessorTest(unittest.TestCase):
    def test(self):
        self.mouse_processor = MouseProcessor("")
        self.session = Session(0, 5)
        self.mouse_collector = MouseCollector(self.session, self.mouse_processor)
        self.mouse_collector.start_collect()


if __name__ == '__main__':
    unittest.main()

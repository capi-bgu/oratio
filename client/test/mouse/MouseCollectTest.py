import unittest
from src.Session import Session
from src.collection.MouseCollector import MouseCollector
from MouseProcessorStub import MouseProcessorStub


class MouseCollectorTest(unittest.TestCase):
    def test(self):
        self.mouse_processor_stub = MouseProcessorStub()
        self.session = Session(1, 10)
        self.mouse_collector = MouseCollector(self.session, self.mouse_processor_stub)
        self.mouse_collector.start_collect()


if __name__ == '__main__':
    unittest.main()

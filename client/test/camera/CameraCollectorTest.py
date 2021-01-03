import unittest
from src.Session import Session
from src.collection.CameraCollector import CameraCollector
from CameraProcessorStub import CameraProcessorStub


class CameraCollectorTest(unittest.TestCase):
    def test(self):
        self.camera_processor_stub = CameraProcessorStub()
        self.session = Session(0, 5)
        self.camera_collector = CameraCollector(self.session, self.camera_processor_stub, 2)
        self.camera_collector.start_collect()


if __name__ == '__main__':
    unittest.main()

from src.Session import Session
from src.collection.MouseCollector import MouseCollector
from src.processing.MouseProcessor import MouseProcessor
from src.collection.CameraCollector import CameraCollector
from src.processing.CameraProcessor import CameraProcessor
from src.collection.KeyboardCollector import KeyboardCollector
from src.processing.KeyboardProcessor import KeyboardProcessor

class Core:
    def __init__(self, data_gatherers):
        self.data_gatherers = data_gatherers

    def run(self):
        session = Session(0, 10, data_gatherers)


# {collectorclass1: [*processingclasses1], collectorclass2: [*processingclasses2]}

if __name__ == '__main__':
    data_gatherers = {KeyboardCollector: [KeyboardProcessor],
                      CameraCollector: [CameraProcessor],
                      MouseCollector: [MouseProcessor]}
    core = Core(data_gatherers)

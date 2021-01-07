from src.Session import Session
from src.collection.MouseCollector import MouseCollector
from src.processing.MouseProcessor import MouseProcessor
from src.collection.CameraCollector import CameraCollector
from src.processing.CameraProcessor import CameraProcessor
from src.collection.KeyboardCollector import KeyboardCollector
from src.processing.KeyboardProcessor import KeyboardProcessor

class Core:
    def __init__(self, data_gatherers):
        """

        :param data_gatherers: dictionary of collectors classes and the list of all related processors classes
            in the format: {CollectorClass: [*(ProcessorClass, out_path]}
        """
        self.data_gatherers = dict()
        for collector_class, processors_class in zip(data_gatherers.keys(), data_gatherers.values()):
            collector = collector_class()
            self.data_gatherers[collector] = list()
            for processor_class in processors_class:
                self.data_gatherers[collector].append(processor_class())
        print()



if __name__ == '__main__':
    data_gatherers = {KeyboardCollector: [KeyboardProcessor],
                      CameraCollector: [CameraProcessor],
                      MouseCollector: [MouseProcessor]}
    core = Core(data_gatherers)

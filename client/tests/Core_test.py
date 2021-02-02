import os
import pathlib
import unittest
from src.Core import Core
from src.processing.MouseProcessor import MouseProcessor
from src.collection.MouseCollector import MouseCollector
from src.collection.CameraCollector import CameraCollector
from src.processing.CameraProcessor import CameraProcessor
from src.database.sqlite_db.SqliteManager import SqliteManager
from src.collection.KeyboardCollector import KeyboardCollector
from src.processing.KeyboardProcessor import KeyboardProcessor
from src.processing.IdentityProcessor import IdentityProcessor
from src.gui.VadSamRadioLabelingUI import VadSamRadioLabelingUI
from src.gui.CategoricalLabelingUI import CategoricalLabelingUI
from src.database.sqlite_db.RawDataHandler import RawDataHandler
from src.database.sqlite_db.MouseDataHandler import MouseDataHandler
from src.database.sqlite_db.CameraDataHandler import CameraDataHandler
from src.database.sqlite_db.SessionDataHandler import SessionDataHandler
from src.database.sqlite_db.KeyboardDataHandler import KeyboardDataHandler


class CoreTest(unittest.TestCase):
    def test(self):
        test_dir = pathlib.Path(__file__).parent.absolute()
        out_path = os.path.join(test_dir, 'test_output')

        data_gatherers = {CameraCollector(fps=5, camera=0): {CameraProcessor(): [CameraDataHandler(out_path)]},
                          KeyboardCollector(): {KeyboardProcessor(): [KeyboardDataHandler(out_path)],
                                                IdentityProcessor(): [RawDataHandler("KeyboardRawData", out_path)]},
                          MouseCollector(): {MouseProcessor(): [MouseDataHandler(out_path)],
                                             IdentityProcessor(): [RawDataHandler("MouseRawData", out_path)]}}
        label_methods = [CategoricalLabelingUI, VadSamRadioLabelingUI]
        session_data_handlers = [SessionDataHandler(out_path)]
        database_managers = [SqliteManager(out_path)]
        core = Core(data_gatherers, out_path, num_sessions=20, session_duration=1,
                    session_data_handlers=session_data_handlers, labeling_methods=label_methods,
                    database_managers=database_managers, ask_freq=10)
        core.run()


if __name__ == '__main__':
    unittest.main()

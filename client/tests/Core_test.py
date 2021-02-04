import os
import logging
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
from src.labeling.ConstantLabelManager import ConstantLabelManager
from src.database.sqlite_db.MouseDataHandler import MouseDataHandler
from src.database.sqlite_db.CameraDataHandler import CameraDataHandler
from src.database.sqlite_db.SessionDataHandler import SessionDataHandler
from src.database.sqlite_db.KeyboardDataHandler import KeyboardDataHandler


# from src.collection.SessionMetaCollector import SessionMetaCollector
# from src.processing.SessionMetaProcessor import SessionMetaProcessor
# from src.database.sqlite_db.SessionMetaDataHandler import SessionMetaDataHandler


class CoreTest(unittest.TestCase):
    def test(self):
        test_dir = pathlib.Path(__file__).parent.absolute()
        out_path = os.path.join(test_dir, 'test_output')

        # logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s',
        #                     datefmt='%m/%d/%Y %I:%M:%S %p')

        logging.basicConfig(level=logging.DEBUG, format='%(message)s')

        data_gatherers = {
            CameraCollector(fps=1, camera=0): {CameraProcessor(): [CameraDataHandler(out_path)]},
            KeyboardCollector(): {KeyboardProcessor(): [KeyboardDataHandler(out_path)],
                                  IdentityProcessor(): [RawDataHandler("KeyboardRawData", out_path)]},
            MouseCollector(): {MouseProcessor(): [MouseDataHandler(out_path)],
                               IdentityProcessor(): [RawDataHandler("MouseRawData", out_path)]},
            # SessionMetaCollector(): {SessionMetaProcessor(): [SessionMetaDataHandler(out_path)],
            #                         IdentityProcessor(): [RawDataHandler("MetaRawData", out_path)]}
        }
        label_methods = [
            CategoricalLabelingUI,
            # VadSamRadioLabelingUI
        ]

        constant_labeler = ConstantLabelManager(label_methods, ask_freq=2)
        session_data_handlers = [SessionDataHandler(out_path)]
        database_managers = [SqliteManager(out_path)]
        core = Core(data_gatherers, out_path, num_sessions=5, session_duration=10,
                    session_data_handlers=session_data_handlers,
                    database_managers=database_managers, label_manager=constant_labeler)
        core.run()


if __name__ == '__main__':
    unittest.main()

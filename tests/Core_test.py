import os
import logging
import pathlib
import unittest
from oratio.Core import Core
from oratio.collection.MouseCollector import MouseCollector
from oratio.processing.MouseProcessor import MouseProcessor
from oratio.collection.CameraCollector import CameraCollector
from oratio.processing.CameraProcessor import CameraProcessor
from oratio.processing.KeyboardProcessor import KeyboardProcessor
from oratio.collection.KeyboardCollector import KeyboardCollector
from oratio.processing.IdentityProcessor import IdentityProcessor
from oratio.database.sqlite_db.SqliteManager import SqliteManager
from oratio.database.sqlite_db.RawDataHandler import RawDataHandler
from oratio.labeling.ConstantLabelManager import ConstantLabelManager
from oratio.collection.SessionMetaCollector import SessionMetaCollector
from oratio.processing.SessionMetaProcessor import SessionMetaProcessor
from oratio.database.sqlite_db.MouseDataHandler import MouseDataHandler
from oratio.database.sqlite_db.CameraDataHandler import CameraDataHandler
from oratio.database.sqlite_db.KeyboardDataHandler import KeyboardDataHandler
from oratio.database.sqlite_db.SessionMetaDataHandler import SessionMetaDataHandler
from oratio.labeling.labeling_method.tk_labeling.CategoricalLabelingUI import CategoricalLabelingUI
from oratio.labeling.labeling_method.tk_labeling.VadSamRadioLabelingUI import VadSamRadioLabelingUI


class CoreTest(unittest.TestCase):
    def test(self):
        test_dir = pathlib.Path(__file__).parent.absolute()
        out_path = os.path.join(test_dir, 'test_output')

        logging.basicConfig(level=logging.INFO, format='%(asctime)s.%(msecs)03d - %(levelname)s: %(message)s',
                            datefmt='%m/%d/%Y %H:%M:%S')

        data_gatherers = {
            CameraCollector(fps=2, camera=0): {CameraProcessor(): [CameraDataHandler(out_path)]},
            KeyboardCollector(): {KeyboardProcessor(): [KeyboardDataHandler(out_path)],
                                  IdentityProcessor(): [RawDataHandler("KeyboardRawData", out_path)]},
            MouseCollector(): {MouseProcessor(): [MouseDataHandler(out_path)],
                               IdentityProcessor(): [RawDataHandler("MouseRawData", out_path)]},
            SessionMetaCollector(): {SessionMetaProcessor(): [SessionMetaDataHandler(out_path)],
                                     IdentityProcessor(): [RawDataHandler("MetaRawData", out_path)]}
        }
        label_methods = [
            CategoricalLabelingUI(),
            # VadSamRadioLabelingUI()
        ]

        constant_labeler = ConstantLabelManager(label_methods, ask_freq=30)
        database_managers = [SqliteManager(out_path)]
        core = Core(data_gatherers, out_path, num_sessions=-1, session_duration=1,
                    database_managers=database_managers, label_manager=constant_labeler)
        core.run()


if __name__ == '__main__':
    unittest.main()

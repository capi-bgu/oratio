import os
import pathlib
import cv2
from src.database.sqlite_db.SqliteDataHandler import SqliteDataHandler


class CameraDataHandlerStub(SqliteDataHandler):

    def __init__(self, name, path=""):
        super().__init__(path)
        test_dir = pathlib.Path(__file__).parent.parent.parent.parent.absolute()
        if not os.path.isdir("../test_output"):
            os.mkdir("../test_output")
        if not os.path.isdir("../test_output/img"):
            os.mkdir("../test_output/img")
        self.out_path = os.path.join(test_dir, 'test_output', 'img')
        self.create_table()
        self.name = name

    def save(self, data):
        for i, img in enumerate(data):
            cv2.imwrite(f"{self.out_path}\\{self.name}_image_{i}.jpg", img)

    def create_table(self):
        pass

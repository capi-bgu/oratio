from src.processing.DataProcessor import DataProcessor


class KeyboardProcessorStub(DataProcessor):
    def __init__(self):
        super().__init__(output_path=r"..\test_output\img\kb")

    def process_data(self, data, session):
        f = open(str(session.session_name)+"_kb.txt", "w+")
        for i, e in enumerate(data):
            f.write(str(i)+'. '+str(e.__dict__)+'\n')

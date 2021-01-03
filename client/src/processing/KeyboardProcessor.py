from src.processing.DataProcessor import DataProcessor


class KeyboardProcessor(DataProcessor):
    def __init__(self, output_path):
        super().__init__(output_path)

    def process_data(self, data, session):
        KB = {}
        features = KeyboardProcessor.__init_features(session)
        for event in data:
            if event.Message == 256:  # key press
                if event.Key not in KB.keys():
                    KB[event.Key] = {'last_press_time': 0,
                                     'press_count': 0,
                                     'total_press_time': 0}
                if KB[event.Key]['last_press_time'] == 0:
                    KB[event.Key]['last_press_time'] = event.Time
            elif event.Message == 257:  # key release
                KB[event.Key]['total_press_time'] += event.Time - KB[event.Key]['last_press_time']
                KB[event.Key]['press_count'] += 1
                KB[event.Key]['last_press_time'] = 0

        for key in KB:
            features['typing_speed'] += KB[key]['total_press_time']
            features['average_press_duration'] += KB[key]['total_press_time'] / KB[key]['press_count']
            features['idle_time'] -=  KB[key]['total_press_time']

        features['typing_speed'] /= session.session_duration
        features['average_press_duration'] /= len(KB)

    @staticmethod
    def __init_features(session):
        features = {'typing_speed': 0,  # V
                    'average_press_duration': 0,  # V
                    'average_down_to_down': 0,
                    'regular_press_count': 0,
                    'punctuations_press_count': 0,
                    'space_press_count': 0,
                    'special_press_count': 0,
                    'error_corrections': 0,
                    'uppercase_counter': 0,
                    'digraph_duration': 0,
                    'trigraph_duration': 0,
                    'mode_key': 0,
                    'idle_time': session.session_duration,
                    'unique_events': 0}
        return features


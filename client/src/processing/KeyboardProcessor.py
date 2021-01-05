from src.processing.DataProcessor import DataProcessor


class KeyboardProcessor(DataProcessor):
    def __init__(self, output_path):
        super().__init__(output_path)

    def process_data(self, data, session):
        KB = {}
        features = self.__init_features(session)
        previous_time = 0
        last_active_time = 0
        total_active_time = 0
        pressed_keys = set()  # the set that will save every key that is pressed
        for event in data:
            if event.Message == 256:  # key press
                if event.Key not in KB.keys():
                    KB[event.Key] = {'last_press_time': 0,
                                     'press_count': 0,
                                     'total_press_time': 0}
                if KB[event.Key]['last_press_time'] == 0:  # the first event sent when press occur
                    if len(pressed_keys) == 0:
                        last_active_time = event.Timestamp
                    pressed_keys.add(event.Key)
                    KB[event.Key]['last_press_time'] = event.Timestamp
                    if previous_time == 0:
                        previous_time = event.Timestamp
                    else:
                        features['average_down_to_down'] += event.Timestamp - previous_time

            elif event.Message == 257:  # key release
                pressed_keys.remove(event.Key)
                if len(pressed_keys) == 0:  # no more keys are pressed and we add the active time
                    total_active_time += event.Timestamp - last_active_time
                KB[event.Key]['total_press_time'] += event.Timestamp - KB[event.Key]['last_press_time']
                KB[event.Key]['press_count'] += 1
                KB[event.Key]['last_press_time'] = 0

                if chr(event.Ascii).isupper():
                    features['uppercase_counter'] += 1
                if chr(event.Ascii).isspace():
                    features['space_counter'] += 1
                if chr(event.Ascii).isalnum():
                    features['space_counter'] += 1

                if event.Key == 'Delete' or event.Key == 'Back':
                    features['error_corrections'] += 1

        total_press_count = 0
        features['mode_key'] = list(KB.keys())[0]
        mode_key_presses = KB[list(KB.keys())[0]]['press_count']
        for key in KB:
            features['average_press_duration'] += KB[key]['total_press_time'] / KB[key]['press_count']
            total_press_count += KB[key]['press_count']
            if KB[key]['press_count'] > mode_key_presses:
                mode_key_presses = KB[key]['press_count']
                features['mode_key'] = key

        features['typing_speed'] = total_press_count / session.session_duration
        features['average_press_duration'] /= len(KB)
        features['average_down_to_down'] /= total_press_count
        features['unique_events'] = len(KB)
        features['idle_time'] -= total_active_time

    def __init_features(self, session):
        features = {
            # 'typing_speed': 0,
            # 'average_press_duration': 0,
            # 'average_down_to_down': 0,
            # 'regular_press_count': 0,
            'punctuations_press_count': 0,
            # 'space_counter': 0,
            'special_press_count': 0,
            # 'error_corrections': 0,
            # 'uppercase_counter': 0,
            'digraph_duration': 0,
            'trigraph_duration': 0,
            # 'mode_key': 0,
            # 'idle_time': session.session_duration,
            # 'unique_events': 0
        }
        return features

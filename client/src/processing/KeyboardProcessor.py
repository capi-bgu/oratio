import json
from src.processing.DataProcessor import DataProcessor


class KeyboardProcessor(DataProcessor):
    def __init__(self, output_path):
        output_path += "\\keyboard"
        super().__init__(output_path)

    def process_data(self, data, session):
        print("start kb processing...")
        keys_info = {}
        features = self.__init_features(session)
        previous_time = 0
        pressed_keys = set()  # the set that will save every key that is pressed
        idle_time = 0
        for i, event in enumerate(data):
            if event.Message == 256:  # key press
                if event.KeyID not in keys_info.keys():
                    keys_info[event.KeyID] = {'last_press_time': 0,
                                              'press_count': 0,
                                              'total_press_time': 0}
                if keys_info[event.KeyID]['last_press_time'] == 0:  # the first event sent when press occur
                    keys_info[event.KeyID]['press_count'] += 1
                    pressed_keys.add(event.KeyID)
                    keys_info[event.KeyID]['last_press_time'] = event.Timestamp
                    if previous_time == 0:
                        previous_time = event.Timestamp
                    else:
                        features['average_down_to_down'] += event.Timestamp - previous_time
                        previous_time = event.Timestamp

                if event.Key == 'Delete' or event.Key == 'Back':
                    features['error_corrections'] += 1

            elif event.Message == 257:  # key release
                if event.KeyID in pressed_keys:
                    pressed_keys.remove(event.KeyID)
                    keys_info[event.KeyID]['total_press_time'] += event.Timestamp - keys_info[event.KeyID][
                        'last_press_time']
                    keys_info[event.KeyID]['last_press_time'] = 0

                    if chr(event.Ascii).isupper():
                        features['uppercase_counter'] += 1
                    if chr(event.Ascii).isspace():
                        features['space_counter'] += 1
                    if chr(event.Ascii).isalnum():
                        features['regular_press_count'] += 1

            if i == 0:  # if it's the first event
                time_interval = data[i].Timestamp - session.session_start_time
            else:
                if i == len(data) - 1:
                    time_interval = (session.session_start_time + session.session_duration) - data[i].Timestamp
                    if time_interval > 0.75:
                        idle_time += time_interval
                time_interval = data[i].Timestamp - data[i - 1].Timestamp  # A B C .
            if time_interval > 0.75:
                idle_time += time_interval
        if len(data) > 0:
            total_press_count = 0
            features['mode_key'] = list(keys_info.keys())[0]
            mode_key_presses = keys_info[list(keys_info.keys())[0]]['press_count']
            for key in keys_info:
                features['average_press_duration'] += keys_info[key]['total_press_time'] / keys_info[key]['press_count']
                total_press_count += keys_info[key]['press_count']
                if keys_info[key]['press_count'] > mode_key_presses:
                    mode_key_presses = keys_info[key]['press_count']
                    features['mode_key'] = key

            features['typing_speed'] = total_press_count / session.session_duration
            features['average_press_duration'] /= len(keys_info)
            features['average_down_to_down'] /= total_press_count
            features['unique_events'] = len(keys_info)
            features['idle_time'] = idle_time

        with open(f"{self.output_path}\\kb_features_s_{str(session.session_name)}.json", 'w+') as features_file:
            json.dump(features, features_file)
        print("end kb processing...")


    def __init_features(self, session):
        features = {
            'typing_speed': 0,
            'average_press_duration': 0,
            'average_down_to_down': 0,
            'regular_press_count': 0,
            'punctuations_press_count': 0,
            'space_counter': 0,
            'special_press_count': 0,
            'error_corrections': 0,
            'uppercase_counter': 0,
            'digraph_duration': 0,
            'trigraph_duration': 0,
            'mode_key': 0,
            'idle_time': session.session_duration,
            'unique_events': 0
        }
        return features

import string
import logging
from src.processing.DataProcessor import DataProcessor


class KeyboardProcessor(DataProcessor):
    MINIMUM_IDLE_TIME = 0.9

    def __init__(self):
        super().__init__()

    def process_data(self, data, session):
        logging.info("start kb processing...")
        keys_info = {}
        self.__init_features(session)
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
                        down_to_down = event.Timestamp - previous_time
                        if down_to_down < self.MINIMUM_IDLE_TIME:
                            self.features['average_down_to_down'] += down_to_down
                        previous_time = event.Timestamp

                if event.Key == 'Delete' or event.Key == 'Back':
                    self.features['error_corrections'] += 1

            elif event.Message == 257:  # key release
                if event.KeyID in pressed_keys:
                    pressed_keys.remove(event.KeyID)
                    keys_info[event.KeyID]['total_press_time'] += event.Timestamp - keys_info[event.KeyID][
                        'last_press_time']
                    keys_info[event.KeyID]['last_press_time'] = 0

                    if chr(event.Ascii).isalnum():
                        self.features['regular_press_count'] += 1
                    elif chr(event.Ascii) in string.punctuation:
                        self.features['punctuations_press_count'] += 1

                    if chr(event.Ascii).isupper():
                        self.features['uppercase_counter'] += 1
                    elif chr(event.Ascii).isspace():
                        self.features['space_counter'] += 1

            if i == 0:  # if it's the first event
                time_interval = data[i].Timestamp - session.start_time
            else:
                if i == len(data) - 1:
                    time_interval = (session.start_time + session.duration) - data[i].Timestamp
                    if time_interval > self.MINIMUM_IDLE_TIME:
                        idle_time += time_interval
                time_interval = data[i].Timestamp - data[i - 1].Timestamp
            if time_interval > self.MINIMUM_IDLE_TIME:
                idle_time += time_interval
        if len(keys_info) > 0:
            total_press_count = 0
            self.features['mode_key'] = list(keys_info.keys())[0]
            mode_key_presses = keys_info[list(keys_info.keys())[0]]['press_count']
            for key in keys_info:
                self.features['average_press_duration'] += keys_info[key]['total_press_time'] / keys_info[key][
                    'press_count']
                total_press_count += keys_info[key]['press_count']
                if keys_info[key]['press_count'] > mode_key_presses:
                    mode_key_presses = keys_info[key]['press_count']
                    self.features['mode_key'] = key

            self.features['typing_speed'] = total_press_count / session.duration
            self.features['average_press_duration'] /= len(keys_info)
            self.features['average_down_to_down'] /= total_press_count
            self.features['unique_events'] = len(keys_info)
            self.features['idle_time'] = idle_time
            active_time = session.duration - self.features['idle_time']
            if active_time != 0:
                self.features['active_typing_speed'] = total_press_count / active_time
        logging.info("end kb processing...")
        return self.features

    def __init_features(self, session):
        self.features = {
            'typing_speed': 0,
            'active_typing_speed': 0,
            'average_press_duration': 0,
            'average_down_to_down': 0,
            'regular_press_count': 0,
            'punctuations_press_count': 0,
            'space_counter': 0,
            'error_corrections': 0,
            'uppercase_counter': 0,
            'mode_key': 0,
            'idle_time': session.duration,
            'unique_events': 0
        }

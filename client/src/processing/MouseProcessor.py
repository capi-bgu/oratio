import os
import json
from src.processing.DataProcessor import DataProcessor


class MouseProcessor(DataProcessor):
    def __init__(self, output_path):
        output_path += "\\mouse"
        super().__init__(output_path)

    def process_data(self, data, session):
        print("start mouse processing...")
        features = self.__init_features(session)
        last_left_click_time = 0
        last_right_click_time = 0
        last_scrolling_segment = []
        last_message = 0
        last_mouse_scroll_direction = 0
        amount_of_scroll_segments = 0
        idle_time = 0
        for i, event in enumerate(data):
            if event.Message == 512:    # Mouse move
                # print("Mouse move")
                pass
            elif event.Message == 513:  # Left button press
                features['left_click_count'] += 1
                # TODO: this double click option counts 3 consecutive clicks as 2 double clicks.
                if len(data) > 2 and data[i - 2].Message == 513 and event.Timestamp - data[i - 2].Timestamp <= 0.5:
                    features['double_click_count'] += 1
                last_left_click_time = event.Timestamp
            elif event.Message == 514:  # Left button release
                features['left_click_duration'] += event.Timestamp - last_left_click_time
            elif event.Message == 516:  # Right button press
                features['right_click_count'] += 1
                last_right_click_time = event.Timestamp
            elif event.Message == 517:  # Right button release
                features['right_click_duration'] += event.Timestamp - last_right_click_time
            elif event.Message == 522:  # Mouse Scroll
                if last_mouse_scroll_direction != event.Wheel or last_message != 522:
                    if len(last_scrolling_segment) > 1:
                        # calculating the time it took to do the whole scroll session and divide by number of scrolls
                        features['scroll_speed'] += len(last_scrolling_segment) / (last_scrolling_segment[-1].Timestamp - last_scrolling_segment[0].Timestamp + 0.0001)
                        amount_of_scroll_segments += 1
                    last_scrolling_segment = [event]
                else:
                    last_scrolling_segment.append(event)
                last_mouse_scroll_direction = event.Wheel
            if i == 0:  # if it's the first event
                time_interval = data[i].Timestamp - session.session_start_time
            else:
                if i == len(data) - 1:
                    time_interval = (session.session_start_time + session.session_duration) - data[i].Timestamp
                    if time_interval > 0.5:
                        idle_time += time_interval
                time_interval = data[i].Timestamp - data[i - 1].Timestamp
            if time_interval > 0.5:
                idle_time += time_interval
            last_message = event.Message
        # if we still have a scrolling left, we add it
        if len(last_scrolling_segment) > 1:
            features['scroll_speed'] += len(last_scrolling_segment) / (
                        last_scrolling_segment[-1].Timestamp - last_scrolling_segment[0].Timestamp + 0.0001)
            amount_of_scroll_segments += 1

        if amount_of_scroll_segments > 0:
            features['scroll_speed'] /= amount_of_scroll_segments
        if len(data) > 0:
            features['idle_time'] = idle_time

        with open(f"{self.output_path}\\mouse_features_s_{str(session.session_name)}.json", 'w+') as features_file:
            json.dump(features, features_file)

        print("end mouse processing...")

    def __init_features(self, session):
        features = {
            'right_click_count': 0,
            'left_click_count': 0,
            'scroll_speed': 0,
            'double_click_count': 0,
            'cursor_x_distance': 0,
            'cursor_y_distance': 0,
            'average_cursor_x_speed': 0,
            'average_cursor_y_speed': 0,
            'average_cursor_x_angle': 0,
            'average_cursor_y_angle': 0,
            'cursor_distance_ratio': 0,
            'idle_time': session.session_duration,
            'right_click_duration': 0,
            'left_click_duration': 0,
        }
        return features

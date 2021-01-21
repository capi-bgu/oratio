import os
import json
from src.processing.DataProcessor import DataProcessor


class MouseProcessor(DataProcessor):
    def __init__(self):
        super().__init__()

    def process_data(self, data, session):
        print("start mouse processing...")
        self.__init_features(session)
        num_mouse_move = 0
        sum_mouse_x_speed = 0
        sum_mouse_y_speed = 0
        total_x_distance = 0
        total_y_distance = 0
        last_left_click_time = 0
        last_right_click_time = 0
        last_scrolling_segment = []
        last_message = 0
        last_mouse_scroll_direction = 0
        amount_of_scroll_segments = 0
        idle_time = 0
        last_mouse_event = None
        for i, event in enumerate(data):
            if event.Message == 512:    # Mouse move
                if last_mouse_event is not None:
                    total_x_distance += abs(event.Position[0] - last_mouse_event.Position[0])
                    total_y_distance += abs(event.Position[1] - last_mouse_event.Position[1])
                    sum_mouse_x_speed += total_x_distance / (1 + event.Timestamp - last_mouse_event.Timestamp)
                    sum_mouse_y_speed += total_y_distance / (1 + event.Timestamp - last_mouse_event.Timestamp)
                num_mouse_move += 1
                last_mouse_event = event
            elif event.Message == 513:  # Left button press
                self.features['left_click_count'] += 1
                # TODO: this double click option counts 3 consecutive clicks as 2 double clicks.
                if len(data) > 2 and data[i - 2].Message == 513 and event.Timestamp - data[i - 2].Timestamp <= 0.5:
                    self.features['double_click_count'] += 1
                last_left_click_time = event.Timestamp
            elif event.Message == 514:  # Left button release
                self.features['left_click_duration'] += event.Timestamp - last_left_click_time
            elif event.Message == 516:  # Right button press
                self.features['right_click_count'] += 1
                last_right_click_time = event.Timestamp
            elif event.Message == 517:  # Right button release
                self.features['right_click_duration'] += event.Timestamp - last_right_click_time
            elif event.Message == 522:  # Mouse Scroll
                if last_mouse_scroll_direction != event.Wheel or last_message != 522:
                    if len(last_scrolling_segment) > 1:
                        # calculating the time it took to do the whole scroll session and divide by number of scrolls
                        self.features['scroll_speed'] += len(last_scrolling_segment) / (
                                last_scrolling_segment[-1].Timestamp - last_scrolling_segment[0].Timestamp + 0.0001)
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
            self.features['scroll_speed'] += len(last_scrolling_segment) / (
                        last_scrolling_segment[-1].Timestamp - last_scrolling_segment[0].Timestamp + 0.0001)
            amount_of_scroll_segments += 1

        if amount_of_scroll_segments > 0:
            self.features['scroll_speed'] /= amount_of_scroll_segments
        if len(data) > 0:
            self.features['idle_time'] = idle_time
        self.features['cursor_x_distance'] = total_x_distance
        self.features['cursor_y_distance'] = total_y_distance
        self.features['average_speed_x'] = total_x_distance / session.session_duration
        self.features['average_speed_y'] = total_y_distance / session.session_duration
        active_time = session.session_duration - self.features['idle_time']
        if active_time > 0:
            self.features['average_active_speed_x'] = total_x_distance / active_time
            self.features['average_active_speed_y'] = total_y_distance / active_time
        if num_mouse_move > 0:
            self.features['average_momentary_speed_x'] = sum_mouse_x_speed / num_mouse_move
        if num_mouse_move > 0:
            self.features['average_momentary_speed_y'] = sum_mouse_y_speed / num_mouse_move
        print("end mouse processing...")
        return self.features

    def __init_features(self, session):
        self.features = {
            'right_click_count': 0,
            'left_click_count': 0,
            'scroll_speed': 0,
            'double_click_count': 0,
            'cursor_x_distance': 0,
            'cursor_y_distance': 0,
            'average_momentary_speed_x': 0,
            'average_momentary_speed_y': 0,
            'average_speed_x': 0,
            'average_speed_y': 0,
            'average_active_speed_x': 0,
            'average_active_speed_y': 0,
            'average_cursor_x_angle': 0,
            'average_cursor_y_angle': 0,
            'cursor_distance_ratio': 0,
            'idle_time': session.session_duration,
            'right_click_duration': 0,
            'left_click_duration': 0,
        }

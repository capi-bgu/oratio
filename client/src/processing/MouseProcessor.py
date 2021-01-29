import math
import numpy as np
from src.processing.DataProcessor import DataProcessor


class MouseProcessor(DataProcessor):
    MINIMUM_IDLE_TIME = 0.5

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
        num_consecutive_move = 0
        last_angle = None
        turn_angles = np.array([])
        all_angles = np.array([])
        last_mouse_event = None
        for i, event in enumerate(data):
            if event.Message == 512:  # Mouse move
                if last_mouse_event is not None:
                    dx = event.Position[0] - last_mouse_event.Position[0]
                    dy = event.Position[1] - last_mouse_event.Position[1]
                    total_x_distance += abs(dx)
                    total_y_distance += abs(dy)
                    # here we used signed because when we calculate the angle we care about the directions
                    velocity_x = abs(dx) / (0.001 + event.Timestamp - last_mouse_event.Timestamp)
                    velocity_y = abs(dy) / (0.001 + event.Timestamp - last_mouse_event.Timestamp)
                    sum_mouse_x_speed += velocity_x
                    sum_mouse_y_speed += velocity_y
                    if num_consecutive_move % 15 == 0:  # every number of consecutive mouse movements
                        angle = math.degrees(math.atan2(dy, dx))
                        angle = (angle + 360) % 360  # to make the angle between 0 and 360
                        all_angles = np.append(all_angles, angle)
                        if num_consecutive_move != 0 and last_angle != None:
                            # absolute value of their difference, then, if larger than 180, substract 360° and take
                            # the absolute value of the result.
                            difference = abs(angle - last_angle)
                            if difference > 180:
                                difference -= 360
                                difference = abs(difference)
                            if difference > 10:
                                turn_angles = np.append(turn_angles, difference)
                        last_angle = angle
                num_mouse_move += 1
                last_mouse_event = event
            elif event.Message == 513:  # Left button press
                self.features['left_click_count'] += 1
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
                                last_scrolling_segment[-1].Timestamp - last_scrolling_segment[0].Timestamp + 0.001)
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
                    if time_interval > self.MINIMUM_IDLE_TIME:
                        idle_time += time_interval
                time_interval = data[i].Timestamp - data[i - 1].Timestamp
            if time_interval > self.MINIMUM_IDLE_TIME:
                idle_time += time_interval
            last_message = event.Message
            # counting how many consecutive mouse movements we had
            if last_message != 512:
                num_consecutive_move = 0
            else:
                num_consecutive_move += 1
        # if we still have a scrolling left, we add it
        if len(last_scrolling_segment) > 1:
            self.features['scroll_speed'] += len(last_scrolling_segment) / (
                    last_scrolling_segment[-1].Timestamp - last_scrolling_segment[0].Timestamp + 0.001)
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
            self.features['average_momentary_speed_y'] = sum_mouse_y_speed / num_mouse_move
            # self.features['average_cursor_angle'] = sum_angle / num_mouse_move

            if len(turn_angles) > 0:
                self.features['average_cursor_angle'] = np.mean(turn_angles)
                self.features['std_cursor_angle'] = np.std(turn_angles)
                self.features['Turn_0_45'] = ((turn_angles >= 0) & (turn_angles < 45)).sum()
                self.features['Turn_45_90'] = ((turn_angles >= 45) & (turn_angles < 90)).sum()
                self.features['Turn_90_135'] = ((turn_angles >= 90) & (turn_angles < 135)).sum()
                self.features['Turn_135_180'] = ((turn_angles >= 135) & (turn_angles < 180)).sum()
            if len(all_angles) > 0:
                self.features['Direction_S'] = ((turn_angles >= 67.5) & (turn_angles < 112.5)).sum()
                self.features['Direction_SW'] = ((turn_angles >= 112.5) & (turn_angles < 157.5)).sum()
                self.features['Direction_W'] = ((turn_angles >= 157.5) & (turn_angles < 202.5)).sum()
                self.features['Direction_NW'] = ((turn_angles >= 202.5) & (turn_angles < 247.5)).sum()
                self.features['Direction_N'] = ((turn_angles >= 247.5) & (turn_angles < 292.5)).sum()
                self.features['Direction_NE'] = ((turn_angles >= 292.5) & (turn_angles < 337.5)).sum()
                self.features['Direction_E'] = (((turn_angles >= 337.5) & (turn_angles < 360)) |
                                                ((turn_angles < 22.5) & (turn_angles >= 0))).sum()
                self.features['Direction_SE'] = ((turn_angles >= 22.5) & (turn_angles < 67.5)).sum()

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
            'average_cursor_angle': 0,
            'std_cursor_angle': 0,
            'Turn_0_45': 0,
            'Turn_45_90': 0,
            'Turn_90_135': 0,
            'Turn_135_180': 0,
            'Direction_S': 0,
            'Direction_SW': 0,
            'Direction_W': 0,
            'Direction_NW': 0,
            'Direction_N': 0,
            'Direction_NE': 0,
            'Direction_E': 0,
            'Direction_SE': 0,
            'cursor_distance_ratio': 0,
            'idle_time': session.session_duration,
            'right_click_duration': 0,
            'left_click_duration': 0,
        }

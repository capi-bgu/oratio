import math
import logging
import numpy as np
from oratio.processing.DataProcessor import DataProcessor


class MouseProcessor(DataProcessor):
    MINIMUM_IDLE_TIME = 0.5

    def __init__(self):
        super().__init__()

    def process_data(self, data, session):
        logging.info("start mouse processing...")
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
        last_direction = ""
        last_mouse_event = None

        window_dx = 0
        window_dy = 0
        abs_window_dx = 0
        abs_window_dy = 0
        double_window_dx = 0
        double_window_dy = 0
        abs_double_window_dx = 0
        abs_double_window_dy = 0
        triple_window_dx = 0
        triple_window_dy = 0
        abs_triple_window_dx = 0
        abs_triple_window_dy = 0
        ratio_arr = []
        double_ratio_arr = []
        triple_ratio_arr = []
        WINDOW_SIZE = 20
        all_speeds = []

        for i, event in enumerate(data):
            if event.Message == 512:  # Mouse move
                if last_mouse_event is not None:
                    dx = event.Position[0] - last_mouse_event.Position[0]
                    dy = event.Position[1] - last_mouse_event.Position[1]
                    window_dx += dx
                    window_dy += dy
                    abs_window_dx += abs(dx)
                    abs_window_dy += abs(dy)
                    double_window_dx += dx
                    double_window_dy += dy
                    abs_double_window_dx += abs(dx)
                    abs_double_window_dy += abs(dy)
                    triple_window_dx += dx
                    triple_window_dy += dy
                    abs_triple_window_dx += abs(dx)
                    abs_triple_window_dy += abs(dy)
                    total_x_distance += abs(dx)
                    total_y_distance += abs(dy)
                    velocity_x = abs(dx) / (0.001 + event.Timestamp - last_mouse_event.Timestamp)
                    velocity_y = abs(dy) / (0.001 + event.Timestamp - last_mouse_event.Timestamp)
                    all_speeds.append(math.sqrt(velocity_x**2 + velocity_y**2))
                    sum_mouse_x_speed += velocity_x
                    sum_mouse_y_speed += velocity_y
                    if num_consecutive_move % WINDOW_SIZE == WINDOW_SIZE - 1:  # check if end of window
                        route = math.sqrt(abs_window_dx**2 + abs_window_dy**2)
                        fastest_route = math.sqrt(window_dx**2 + window_dy**2) + 0.001
                        ratio = route / fastest_route
                        ratio_arr.append(ratio)
                        abs_window_dx = 0
                        abs_window_dy = 0
                        if num_consecutive_move % (2*WINDOW_SIZE) == 2*WINDOW_SIZE - 1:
                            route = math.sqrt(abs_double_window_dx ** 2 + abs_double_window_dy ** 2)
                            fastest_route = math.sqrt(double_window_dx ** 2 + double_window_dy ** 2) + 0.001
                            double_ratio = route / fastest_route
                            double_ratio_arr.append(double_ratio)
                            double_window_dx = 0
                            double_window_dy = 0
                            abs_double_window_dx = 0
                            abs_double_window_dy = 0
                        if num_consecutive_move % (3*WINDOW_SIZE) == 3*WINDOW_SIZE - 1:
                            route = math.sqrt(abs_triple_window_dx ** 2 + abs_triple_window_dy ** 2)
                            fastest_route = math.sqrt(triple_window_dx ** 2 + triple_window_dy ** 2) + 0.001
                            triple_ratio = route / fastest_route
                            triple_ratio_arr.append(triple_ratio)
                            triple_window_dx = 0
                            triple_window_dy = 0
                            abs_triple_window_dx = 0
                            abs_triple_window_dy = 0
                        angle = math.degrees(math.atan2(window_dy, window_dx))
                        angle = (angle + 360) % 360  # to make the angle between 0 and 360
                        direction = self.__angle_to_direction(angle)
                        if direction != last_direction:
                            self.features[f'Direction_{direction}'] += 1
                            last_direction = direction
                        window_dx = 0
                        window_dy = 0
                        if num_consecutive_move != 0 and last_angle is not None:
                            # absolute value of their difference, then, if larger than 180, substract 360° and take
                            # the absolute value of the result.
                            difference = abs(angle - last_angle)
                            if difference > 180:
                                difference -= 360
                                difference = abs(difference)
                            if difference > 15:
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
                if last_left_click_time != 0:
                    self.features['left_click_duration'] += event.Timestamp - last_left_click_time
            elif event.Message == 516:  # Right button press
                self.features['right_click_count'] += 1
                last_right_click_time = event.Timestamp
            elif event.Message == 517:  # Right button release
                if last_right_click_time != 0:
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
                time_interval = data[i].Timestamp - session.start_time
            else:
                if i == len(data) - 1:
                    time_interval = (session.start_time + session.duration) - data[i].Timestamp
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
        self.features['average_speed_x'] = total_x_distance / session.duration
        self.features['average_speed_y'] = total_y_distance / session.duration
        active_time = session.duration - self.features['idle_time']
        if active_time > 0:
            self.features['average_active_speed_x'] = total_x_distance / active_time
            self.features['average_active_speed_y'] = total_y_distance / active_time
        if len(all_speeds) > 0:
            self.features['speed_std'] = np.std(all_speeds)
        if num_mouse_move > 0:
            self.features['average_momentary_speed_x'] = sum_mouse_x_speed / num_mouse_move
            self.features['average_momentary_speed_y'] = sum_mouse_y_speed / num_mouse_move
            if len(ratio_arr) > 0:
                self.features['Dist1'] = sum(ratio_arr) / len(ratio_arr)
            if len(double_ratio_arr) > 0:
                self.features['Dist2'] = sum(double_ratio_arr) / len(double_ratio_arr)
            if len(triple_ratio_arr) > 0:
                self.features['Dist3'] = sum(triple_ratio_arr) / len(triple_ratio_arr)

            if len(turn_angles) > 0:
                self.features['average_cursor_angle'] = np.mean(turn_angles)
                self.features['std_cursor_angle'] = np.std(turn_angles)
                self.features['Turn_0_45'] = int(((turn_angles >= 0) & (turn_angles < 45)).sum())
                self.features['Turn_45_90'] = int(((turn_angles >= 45) & (turn_angles < 90)).sum())
                self.features['Turn_90_135'] = int(((turn_angles >= 90) & (turn_angles < 135)).sum())
                self.features['Turn_135_180'] = int(((turn_angles >= 135) & (turn_angles < 180)).sum())

        logging.info("end mouse processing...")
        return self.features

    def __angle_to_direction(self, angle):
        if (angle >= 67.5) and (angle < 112.5):
            return "S"
        if (angle >= 112.5) and (angle < 157.5):
            return "SW"
        if (angle >= 157.5) and (angle < 202.5):
            return "W"
        if (angle >= 202.5) and (angle < 247.5):
            return "NW"
        if (angle >= 247.5) and (angle < 292.5):
            return "N"
        if (angle >= 292.5) and (angle < 337.5):
            return "NE"
        if (angle >= 337.5) and (angle < 360):
            return "E"
        if (angle < 22.5) and (angle >= 0):
            return "E"
        if (angle >= 22.5) and (angle < 67.5):
            return "SE"

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
            'speed_std': 0,
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
            'Dist1': 0,
            'Dist2': 0,
            'Dist3': 0,
            'idle_time': session.duration,
            'right_click_duration': 0,
            'left_click_duration': 0,
        }

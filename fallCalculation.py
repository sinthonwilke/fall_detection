import math


class fallCalculation:

    def __init__(self) -> None:
        pass

    def calculate_angle(self, point1, point2):
        angle_radians = math.atan2(point2['y'] - point1['y'], point2['x'] - point1['x'])
        angle_degrees = math.degrees(angle_radians)
        return angle_degrees

    def isBetween(self, input_angle, lower_bound, upper_bound):
        if lower_bound < input_angle < upper_bound:
            return True
        else:
            return False

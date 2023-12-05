import math


class fallCalculation:

    def __init__(self) -> None:
        self.ACEPTABLE_STANDING_DEGREES = (45, 145)

        self.min_height = float('inf')
        self.max_height = 0
        self.avg_height = 0

        self.head = None
        self.shoulder = None
        self.hip = None
        self.knee = None
        self.foot = None

    def calculate_degree(self, point1, point2):
        angle_radians = math.atan2(point2['y'] - point1['y'], point2['x'] - point1['x'])
        angle_degrees = math.degrees(angle_radians)
        return angle_degrees

    def calculate_distance(self, point1, point2):
        distance = math.sqrt((point2['x'] - point1['x'])**2 + (point2['y'] - point1['y'])**2)
        return distance

    def isBetween(self, input_angle, lower_bound, upper_bound):
        if lower_bound < abs(input_angle) < upper_bound:
            return True
        else:
            return False

    def isStanding(self):
        if self.isBetween(self.calculate_degree(self.head, self.foot), self.ACEPTABLE_STANDING_DEGREES[0], self.ACEPTABLE_STANDING_DEGREES[1]) and (self.getHeight() > self.max_height / 3):
            return True
        else:
            return False

    def setValue(self, landmarks=[]):
        self.head = landmarks[0]
        self.shoulder = landmarks[1]
        self.hip = landmarks[2]
        self.knee = landmarks[3]
        self.foot = landmarks[4]

    def getHeight(self):
        return self.calculate_distance(self.head, self.foot)

    def minHeight(self):
        calculate_distance = self.getHeight()
        if calculate_distance < self.min_height:
            self.min_height = calculate_distance
        return self.min_height

    def maxHeight(self):
        calculate_distance = self.getHeight()
        if calculate_distance > self.max_height:
            self.max_height = calculate_distance
        return self.max_height

    def avgHeight(self):
        calculate_distance = self.getHeight()
        self.avg_height = (self.avg_height + calculate_distance) / 2
        return self.avg_height

    # All the poses
    def pose0(self):  # Still lying down
        print('this function would be called when the person is still lying down')

    def pose1(self):  # Standing
        if (self.head['y'] < self.hip['y'] and self.hip['y'] < self.knee['y'] and self.knee['y'] < self.foot['y'] and self.isStanding()):
            return True
        else:
            return False

    def pose2(self):  # 6tall
        if (self.head['y'] > self.shoulder['y'] and self.shoulder['y'] > self.hip['y'] and self.hip['y'] > self.knee['y'] and self.knee['y'] > self.foot['y'] and self.isStanding()):
            return True
        else:
            return False

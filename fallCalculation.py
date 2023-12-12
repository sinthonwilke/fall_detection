import math
import time


class fallCalculation:

    def __init__(self) -> None:
        self.ACEPTABLE_STANDING_DEGREES = (45, 135)
        self.ACEPTABLE_STANDING_DEGREES2 = (70, 110)
        self.ACEPTABLE_LAYING_DEGREE = ((-30, 30), (-150, 150))
        self.min_height = float('inf')
        self.max_height = 0
        self.avg_height = 0

        self.head = None
        self.shoulder = None
        self.hip = None
        self.knee = None
        self.foot = None

        self.fallTime = time.time()
        self.standToFallTime = time.time()
        self.lastStandToFallTime = float('inf')
        self.totalStandToFall_time = float('inf')
        self.totalStandToFall_status = True
        self.hadFallen = False

    def calculate_degree(self, point1, point2):
        angle_radians = math.atan2(
            point2['y'] - point1['y'], point2['x'] - point1['x'])
        angle_degrees = math.degrees(angle_radians)
        return angle_degrees

    def calculate_distance(self, point1, point2):
        distance = math.sqrt(
            (point2['x'] - point1['x'])**2 + (point2['y'] - point1['y'])**2)
        return distance

    def isBetween(self, input_angle, lower_bound, upper_bound):
        if lower_bound < abs(input_angle) < upper_bound:
            return True
        else:
            return False

    def isBetween2(self, input_angle, lower_bound, upper_bound):
        if -180 < input_angle < lower_bound or upper_bound < input_angle < 180:
            return True
        else:
            return False

    def isStanding(self):
        if self.isBetween(self.calculate_degree(self.head, self.hip), self.ACEPTABLE_STANDING_DEGREES[0], self.ACEPTABLE_STANDING_DEGREES[1]) and self.isBetween(self.calculate_degree(self.hip, self.knee), self.ACEPTABLE_STANDING_DEGREES2[0], self.ACEPTABLE_STANDING_DEGREES2[1]):
            return True
        else:
            return False

    def isLaying(self):
        if self.isBetween(self.calculate_degree(self.head, self.foot), self.ACEPTABLE_LAYING_DEGREE[0][0], self.ACEPTABLE_LAYING_DEGREE[0][1]) or self.isBetween2(self.calculate_degree(self.head, self.foot), self.ACEPTABLE_LAYING_DEGREE[1][0], self.ACEPTABLE_LAYING_DEGREE[1][1]):
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
    def pose0(self):  # Lying down
        if self.isLaying():
            return True
        else:
            return False

    def pose1(self):  # Standing
        if (self.head['y'] < self.hip['y'] and self.hip['y'] < self.knee['y'] and self.knee['y'] < self.foot['y'] and self.isStanding()):
            return True
        else:
            return False

    def resetFall_time(self):
        self.fallTime = time.time()

    def getFall_time(self):
        elapsed_time = time.time() - self.fallTime
        return elapsed_time

    def resetStandToFall_time(self):
        self.standToFallTime = time.time()

    def setLastStandToFall_time(self, time):
        self.lastStandToFallTime = time

    def getLastStandToFall_time(self):
        return self.lastStandToFallTime

    def getStandToFall_time(self):
        elapsed_time = time.time() - self.standToFallTime
        return elapsed_time

    def setTotalStandToFall_time(self):
        self.totalStandToFall_time = self.getStandToFall_time() - \
            self.getLastStandToFall_time()

    def getTotalStandToFall_time(self):
        return self.totalStandToFall_time

    def getTotalStandToFall_status(self):
        return self.totalStandToFall_status

    def setTotalStandToFall_status(self, status):
        self.totalStandToFall_status = status

    def setHadFallen(self, status):
        self.hadFallen = status

    def getHadFallen(self):
        return self.hadFallen

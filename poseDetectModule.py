import re
import cv2
import mediapipe


class poseDetect:
    def __init__(self):
        self.min_detection_confidence = 0.2
        self.min_tracking_confidence = 0.2

        self.mp_pose = mediapipe.solutions.pose
        self.mp_drawing = mediapipe.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=self.min_detection_confidence,
            min_tracking_confidence=self.min_tracking_confidence,
        )

        self.frame = None
        self.pose_landmarks = None

        self.color = {
            'red': (0, 0, 255),
            'green': (0, 255, 0),
            'blue': (255, 0, 0),
        }

    def detect(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        processFrame = self.pose.process(rgb_frame)
        if (processFrame.pose_landmarks):
            self.frame = frame
            self.pose_landmarks = processFrame.pose_landmarks
            return True
        return False

    def get_landmarks(self):
        return self.pose_landmarks

    def draw_landmarks(self):
        for id, landmark in enumerate(self.pose_landmarks.landmark):
            h, w, c = self.frame.shape
            cx, cy = int(landmark.x * w), int(landmark.y * h)
            text = f'id: {id}'
            cv2.putText(self.frame, text, (cx, cy + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.50, self.color['red'], 1)
        self.mp_drawing.draw_landmarks(self.frame, self.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

    def draw_bbox(self, text=False, color='green', margin=0):
        bbox = self.calculate_bbox(margin)
        if bbox:
            cv2.rectangle(self.frame, bbox[0], bbox[1], self.color[color], 2)
            if text:
                cv2.putText(self.frame, text, (bbox[0][0], bbox[0][1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color[color], 2)

    def calculate_bbox(self, margin=0):
        if self.pose_landmarks is not None:
            h, w, _ = self.frame.shape
            all_x = [int(lm.x * w) for lm in self.pose_landmarks.landmark]
            all_y = [int(lm.y * h) for lm in self.pose_landmarks.landmark]
            bbox_min = (max(min(all_x) - margin, 0), max(min(all_y) - margin, 0))
            bbox_max = (min(max(all_x) + margin, w), min(max(all_y) + margin, h))
            return bbox_min, bbox_max
        else:
            return False

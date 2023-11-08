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

        self.pose_landmarks = None

        self.color = {
            'red': (0, 0, 255),
            'green': (0, 255, 0),
            'blue': (255, 0, 0),
        }

    def detect(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        processFrame = self.pose.process(rgb_frame)
        self.pose_landmarks = processFrame.pose_landmarks

        if self.pose_landmarks:
            for id, landmark in enumerate(processFrame.pose_landmarks.landmark):
                h, w, c = frame.shape
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                cv2.circle(frame, (cx, cy), 10, (255, 0, 0), cv2.FILLED)

    def draw_landmarks(self, frame):
        self.mp_drawing.draw_landmarks(frame, self.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

    def draw_bbox(self, frame, text=False, color='green', margin=0):

        bbox = self.calculate_bbox(frame, margin)
        if bbox:
            cv2.rectangle(frame, bbox[0], bbox[1], self.color[color], 2)
            if text:
                cv2.putText(frame, text, (bbox[0][0], bbox[0][1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color[color], 2)

    def calculate_bbox(self, frame, margin=0):
        if self.pose_landmarks is not None:
            h, w, _ = frame.shape

            all_x = [int(lm.x * w) for lm in self.pose_landmarks.landmark]
            all_y = [int(lm.y * h) for lm in self.pose_landmarks.landmark]

            bbox_min = (max(min(all_x) - margin, 0), max(min(all_y) - margin, 0))
            bbox_max = (min(max(all_x) + margin, w), min(max(all_y) + margin, h))

            return bbox_min, bbox_max
        else:
            return False

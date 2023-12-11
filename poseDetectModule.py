import cv2
import mediapipe


class poseDetect:
    def __init__(self):
        self.model_complexity = 1
        self.min_detection_confidence = 0.5
        self.min_tracking_confidence = 0.5

        self.mp_pose = mediapipe.solutions.pose
        self.mp_drawing = mediapipe.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(
            model_complexity=self.model_complexity,
            min_detection_confidence=self.min_detection_confidence,
            min_tracking_confidence=self.min_tracking_confidence,
        )

        self.frame = None
        self.pose_landmarks = None

    def detect(self, frame):
        processFrame = self.pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if (processFrame.pose_landmarks):
            self.frame = frame
            self.pose_landmarks = processFrame.pose_landmarks
            return True
        return False

    def get_landmarks(self):
        return self.pose_landmarks

    def get_needed_landmarks(self):
        head_landmark = self.pose_landmarks.landmark[0]

        left_shoulder = self.pose_landmarks.landmark[11]
        right_shoulder = self.pose_landmarks.landmark[12]

        left_hip = self.pose_landmarks.landmark[23]
        right_hip = self.pose_landmarks.landmark[24]

        left_knee = self.pose_landmarks.landmark[25]
        right_knee = self.pose_landmarks.landmark[26]

        left_foot = self.pose_landmarks.landmark[27]
        right_foot = self.pose_landmarks.landmark[28]

        head = {'x': head_landmark.x, 'y': head_landmark.y}
        shoulder = {'x': (left_shoulder.x + right_shoulder.x) / 2, 'y': (left_shoulder.y + right_shoulder.y) / 2}
        hip = {'x': (left_hip.x + right_hip.x) / 2, 'y': (left_hip.y + right_hip.y) / 2}
        knee = {'x': (left_knee.x + right_knee.x) / 2, 'y': (left_knee.y + right_knee.y) / 2}
        foot = {'x': (left_foot.x + right_foot.x) / 2, 'y': (left_foot.y + right_foot.y) / 2}

        landmarks = [head, shoulder, hip, knee, foot]

        h, w, _ = self.frame.shape
        for i in range(len(landmarks) - 1):
            start_point = (int(landmarks[i]['x'] * w), int(landmarks[i]['y'] * h))
            end_point = (int(landmarks[i + 1]['x'] * w), int(landmarks[i + 1]['y'] * h))

            cv2.line(self.frame, start_point, end_point, (255, 0, 0), 2)
            cv2.circle(self.frame, start_point, 5,  (255, 0, 0), cv2.FILLED)

        foot_point = (int(landmarks[-1]['x'] * w), int(landmarks[-1]['y'] * h))
        cv2.circle(self.frame, foot_point, 5,  (255, 0, 0), cv2.FILLED)

        return landmarks

    def draw_landmarks(self, fullDraw=True):
        if fullDraw:
            self.mp_drawing.draw_landmarks(self.frame, self.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

    def draw_id_landmarks(self, specificLandmark=[]):
        h, w, _ = self.frame.shape

        if specificLandmark == []:
            for id in range(33):
                specificLandmark.append(id)

        for id in specificLandmark:
            cx, cy = int(
                self.pose_landmarks.landmark[id].x * w), int(self.pose_landmarks.landmark[id].y * h)
            text = f'id: {id}'
            cv2.putText(self.frame, text, (cx, cy + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (255, 0, 0), 1)

    def draw_bbox(self, text=False, color=(0, 255, 0), margin=0):
        bbox = self.calculate_bbox(margin)
        if bbox:
            cv2.rectangle(self.frame, bbox[0], bbox[1], color, 2)
            if text:
                cv2.putText(self.frame, text, (bbox[0][0], bbox[0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    def calculate_bbox(self, margin=0):
        h, w, _ = self.frame.shape
        all_x = [int(lm.x * w) for lm in self.pose_landmarks.landmark]
        all_y = [int(lm.y * h) for lm in self.pose_landmarks.landmark]
        bbox_min = (max(min(all_x) - margin, 0), max(min(all_y) - margin, 0))
        bbox_max = (min(max(all_x) + margin, w), min(max(all_y) + margin, h))
        return bbox_min, bbox_max

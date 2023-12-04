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
        self.color = {
            'red': (0, 0, 255),
            'green': (0, 255, 0),
            'blue': (255, 0, 0),
            'yellow': (255, 255, 0),
            'cyan': (0, 255, 255),
            'magenta': (255, 0, 255),
            'white': (255, 255, 255),
            'orange': (255, 165, 0),
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

    def get_needed_landmarks(self):
        head_landmark = self.pose_landmarks.landmark[0]
        head = {
            'x': head_landmark.x,
            'y': head_landmark.y,
            # 'z': head_landmark.z,
            # 'visibility': head_landmark.visibility,
        }

        left_shoulder = self.pose_landmarks.landmark[11]
        right_shoulder = self.pose_landmarks.landmark[12]
        shoulder = {
            'x': (left_shoulder.x + right_shoulder.x) / 2,
            'y': (left_shoulder.y + right_shoulder.y) / 2,
            # 'z': (left_shoulder.z + right_shoulder.z) / 2,
            # 'visibility': (left_shoulder.visibility + right_shoulder.visibility) / 2
        }

        left_hip = self.pose_landmarks.landmark[23]
        right_hip = self.pose_landmarks.landmark[24]
        hip = {
            'x': (left_hip.x + right_hip.x) / 2,
            'y': (left_hip.y + right_hip.y) / 2,
            # 'z': (left_hip.z + right_hip.z) / 2,
            # 'visibility': (left_hip.visibility + right_hip.visibility) / 2
        }

        left_knee = self.pose_landmarks.landmark[25]
        right_knee = self.pose_landmarks.landmark[26]
        knee = {
            'x': (left_knee.x + right_knee.x) / 2,
            'y': (left_knee.y + right_knee.y) / 2,
            # 'z': (left_knee.z + right_knee.z) / 2,
            # 'visibility': (left_knee.visibility + right_knee.visibility) / 2
        }

        left_foot = self.pose_landmarks.landmark[31]
        right_foot = self.pose_landmarks.landmark[32]
        foot = {
            'x': (left_foot.x + right_foot.x) / 2,
            'y': (left_foot.y + right_foot.y) / 2,
            # 'z': (left_foot.z + right_foot.z) / 2,
            # 'visibility': (left_foot.visibility + right_foot.visibility) / 2
        }

        h, w, _ = self.frame.shape

        head_point = (int(head['x'] * w), int(head['y'] * h))
        shoulder_point = (int(shoulder['x'] * w), int(shoulder['y'] * h))
        hip_point = (int(hip['x'] * w), int(hip['y'] * h))
        knee_point = (int(knee['x'] * w), int(knee['y'] * h))
        foot_point = (int(foot['x'] * w), int(foot['y'] * h))

        cv2.line(self.frame, head_point, shoulder_point, self.color['red'], 2)
        cv2.line(self.frame, shoulder_point, hip_point, self.color['green'], 2)
        cv2.line(self.frame, hip_point, knee_point, self.color['blue'], 2)
        cv2.line(self.frame, knee_point, foot_point, self.color['yellow'], 2)
        cv2.circle(self.frame, head_point, 5, self.color['cyan'], cv2.FILLED)
        cv2.circle(self.frame, shoulder_point, 5, self.color['cyan'], cv2.FILLED)
        cv2.circle(self.frame, hip_point, 5, self.color['cyan'], cv2.FILLED)
        cv2.circle(self.frame, knee_point, 5, self.color['cyan'], cv2.FILLED)
        cv2.circle(self.frame, foot_point, 5, self.color['cyan'], cv2.FILLED)

        returnValue = {
            'head': head_point,
            'shoulder': shoulder_point,
            'hip': hip_point,
            'knee': knee_point,
            'foot': foot_point,
        }

        return returnValue

    def draw_landmarks(self, fullDraw=True):
        if fullDraw:
            self.mp_drawing.draw_landmarks(
                self.frame, self.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

    def draw_id_landmarks(self, specificLandmark=[]):
        h, w, _ = self.frame.shape

        if specificLandmark == []:
            for id in range(33):
                specificLandmark.append(id)

        for id in specificLandmark:
            cx, cy = int(
                self.pose_landmarks.landmark[id].x * w), int(self.pose_landmarks.landmark[id].y * h)
            text = f'id: {id}'
            cv2.putText(self.frame, text, (cx, cy + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.50, self.color['red'], 1)

    def draw_bbox(self, text=False, color='green', margin=0):
        bbox = self.calculate_bbox(margin)
        if bbox:
            cv2.rectangle(self.frame, bbox[0], bbox[1], self.color[color], 2)
            if text:
                cv2.putText(self.frame, text, (bbox[0][0], bbox[0][1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color[color], 2)

    def calculate_bbox(self, margin=0):
        h, w, _ = self.frame.shape
        all_x = [int(lm.x * w) for lm in self.pose_landmarks.landmark]
        all_y = [int(lm.y * h) for lm in self.pose_landmarks.landmark]
        bbox_min = (max(min(all_x) - margin, 0),
                    max(min(all_y) - margin, 0))
        bbox_max = (min(max(all_x) + margin, w),
                    min(max(all_y) + margin, h))
        return bbox_min, bbox_max
